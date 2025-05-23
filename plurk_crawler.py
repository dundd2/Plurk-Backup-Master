import os
import re
import sys
import time
import calendar
import base36
import aiohttp
import asyncio
import aiomultiprocess
from functools import partial
from plurk_oauth import PlurkAPI
from time import gmtime, strftime
from dotenv import load_dotenv
from utils import url_exists, download_image, url_validation_pattern as url_validation_regex

# Load environment variables
load_dotenv()

# Get Plurk API credentials from environment variables
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

async def getPublicPlurks(plurk, _id, time_Offset):
    try:
        rawJson = await asyncio.to_thread(partial(plurk.callAPI,
                                                  '/APP/Timeline/getPublicPlurks',
                                                  {'user_id': _id, 'offset': time_Offset, 'limit': 30,
                                                   'favorers_detail': False, 'limited_detail': False, 'replurkers_detail': False}))
        return rawJson['plurks']
    except Exception as e:
        print(f"An error occurred while fetching public plurks: {e}")
        return []

async def parsePostsJob(plurk, i, owner_id, userName, lowStandardFav):
    image_path = f'./{userName}/'
    thisPostMediaCount = 0
    async with aiohttp.ClientSession() as session:
        if i['owner_id'] != owner_id:
            return

        if i['favorite_count'] > lowStandardFav:
            await getResponsesJob(plurk, session, i['plurk_id'], owner_id, userName)

        owner_id_str = str(owner_id)
        base36_plurk_id = str(base36.dumps(i['plurk_id']))

        splitStr = i['posted'].split()
        abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        fileNameTime = splitStr[3] + '_' + str(abbr_to_num[splitStr[2]]) + '_' + splitStr[1]

        _list = i['content'].split()
        tasks = []
        for content in _list:
            if content.startswith('href'):
                content = content[:-1]
                supported_format = ['jpg', 'png', 'gif', 'mp4', 'webp', 'bmp', 'svg']
                if content[-3:] in supported_format:
                    if re.match(url_validation_regex, str(content[6:])) is None:
                        continue
                    if not await url_exists(session, str(content[6:])):  # Changed urlExists to url_exists
                        continue
                    thisPostMediaCount += 1
                    imageNameWithoutPath = f"{fileNameTime}-plurk-{base36_plurk_id}-{thisPostMediaCount}-{owner_id_str}.{content[-3:]}"
                    image_name = image_path + imageNameWithoutPath
                    if os.path.isfile(image_name):
                        print(f"[✗] {imageNameWithoutPath} was already downloaded.")
                        continue
                    print(f'[✓] downloading {imageNameWithoutPath}')
                    tasks.append(download_image(session, str(content[6:]), image_name))
            else:
                # Saving text content
                text_content = content.strip()
                with open(f"{image_path}{fileNameTime}-plurk-{base36_plurk_id}-text.txt", "a", encoding="utf-8") as text_file:
                    text_file.write(text_content + "\n")
        await asyncio.gather(*tasks)

async def getResponsesJob(plurk, session, pID, owner_id, userName):
    owner_id_str = str(owner_id)
    image_path = f'./{userName}/'
    base36_plurk_id = str(base36.dumps(pID))
    res_raw_json = await getResponses(plurk, pID)
    response_count = 0
    thisPostMediaCount = 0

    tasks = []
    for j in res_raw_json['responses']:
        response_count += 1
        splitStr = j['posted'].split()
        abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
        fileNameTime = splitStr[3] + '_' + str(abbr_to_num[splitStr[2]]) + '_' + splitStr[1]
        content_str = j['content']
        match = re.findall(r"href=\S+", content_str)
        matchList = []
        for matchCase in match:
            matchCase = matchCase[:-1]
            matchCase = matchCase[6:]
            matchList.append(matchCase)
        for responseLink in matchList:
            supported_format = ['jpg', 'png', 'gif', 'mp4', 'webp', 'bmp', 'svg']
            if responseLink[-3:] in supported_format:
                if re.match(url_validation_regex, responseLink) is None:
                    print(f"Invalid URL: {responseLink}")
                    continue
                if not await url_exists(session, responseLink):  # Changed urlExists to url_exists
                    print(f"URL does not exist: {responseLink}")
                    continue
                thisPostMediaCount += 1
                imageNameWithoutPath = f"{fileNameTime}-plurk-{base36_plurk_id}-{thisPostMediaCount}-response-{response_count}-{owner_id_str}.{responseLink[-3:]}"
                image_name = image_path + imageNameWithoutPath
                if os.path.isfile(image_name):
                    print(f"[✗] {imageNameWithoutPath} was already downloaded.")
                    continue
                print(f'[✓] downloading {imageNameWithoutPath}')
                tasks.append(download_image(session, responseLink, image_name))
        
        # Saving text content
        text_content = j['content'].strip()
        with open(f"{image_path}{fileNameTime}-plurk-{base36_plurk_id}-response-{response_count}-text.txt", "a", encoding="utf-8") as text_file:
            text_file.write(text_content + "\n")
            
    await asyncio.gather(*tasks)

            
async def getResponses(plurk, pID):
    try:
        rawJson = await asyncio.to_thread(partial(plurk.callAPI,
                                                  '/APP/Responses/get',
                                                  {'plurk_id': pID}))
        return rawJson
    except Exception as e:
        print(f"An error occurred while fetching responses: {e}")
        return {}

                        
async def getPublicPlurks(plurk, _id, time_Offset, limit=30):
    try:
        rawJson = await asyncio.to_thread(partial(plurk.callAPI,
                                                  '/APP/Timeline/getPublicPlurks',
                                                  {'user_id': _id, 'offset': time_Offset, 'limit': limit,
                                                   'favorers_detail': False, 'limited_detail': False, 'replurkers_detail': False}))
        return rawJson['plurks']
    except Exception as e:
        print(f"An error occurred while fetching public plurks: {e}")
        return []
        
async def process_user(plurk, user_name):
    public_profile = plurk.callAPI('/APP/Profile/getPublicProfile', {'user_id': user_name})
    if public_profile is None:
        print(f'User {user_name} Not Found!')
        return

    user_id = public_profile['user_info']['id']
    path = f'./{user_name}'
    
    if not os.path.exists(path):
        os.mkdir(path)
    timeOffset = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

    # store json_data
    json_data_queue = asyncio.Queue()

    async def producer():
        nonlocal timeOffset
        while True:
            json_data = await getPublicPlurks(plurk, user_id, timeOffset)
            if len(json_data) == 0:
                await json_data_queue.put(None) 
                break
            await json_data_queue.put(json_data)
            splitStr = json_data[-1]['posted'].split()
            abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
            timeOffset = f"{splitStr[3]}-{abbr_to_num[splitStr[2]]}-{splitStr[1]}T{splitStr[4]}"

    async def consumer():
        lowStandardFav = -1
        async with aiomultiprocess.Pool() as pool:
            while True:
                json_data = await json_data_queue.get()
                if json_data is None:  
                    break
                tasks = [pool.apply(parsePostsJob, (plurk, i, user_id, user_name, lowStandardFav)) for i in json_data]
                await asyncio.gather(*tasks)

    producer_task = asyncio.create_task(producer())
    await consumer()
            
async def main():
    plurk = PlurkAPI(CONSUMER_KEY, CONSUMER_SECRET)
    plurk.authorize(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    if len(sys.argv) == 1:
        userNamesList = input("Please enter at least one username OR several usernames with space separated:")
        userNamesList = userNamesList.split()
    else:
        userNamesList = sys.argv[1:]
    async with aiomultiprocess.Pool() as pool:
        await asyncio.gather(*[process_user(plurk, user_name) for user_name in userNamesList])
  
if __name__ == "__main__":
    t1 = time.time()
    asyncio.run(main())
    print("============================\nTotal time: {}\n".format(time.time() - t1))
