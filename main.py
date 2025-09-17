import os
import sys
import time
import asyncio
from dotenv import load_dotenv
from plurk_oauth import PlurkAPI
from plurk_crawler import process_user

# Load Environment Variables
load_dotenv()

# Read credentials from environment; if missing, prompt the user and optionally save to .env
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

def prompt_for_missing_env():
    global consumer_key, consumer_secret, access_token, access_token_secret
    changed = False
    if not consumer_key:
        consumer_key = input("Enter CONSUMER_KEY: ").strip()
        changed = True
    if not consumer_secret:
        consumer_secret = input("Enter CONSUMER_SECRET: ").strip()
        changed = True
    if not access_token:
        access_token = input("Enter ACCESS_TOKEN (optional - press Enter to skip): ").strip() or None
        changed = True
    if not access_token_secret:
        access_token_secret = input("Enter ACCESS_TOKEN_SECRET (optional - press Enter to skip): ").strip() or None
        changed = True

    if changed:
        save = input("Save these values to a local .env file for future runs? [y/N]: ").strip().lower()
        if save == 'y':
            with open('.env', 'a', encoding='utf-8') as f:
                if consumer_key:
                    f.write(f"CONSUMER_KEY={consumer_key}\n")
                if consumer_secret:
                    f.write(f"CONSUMER_SECRET={consumer_secret}\n")
                if access_token:
                    f.write(f"ACCESS_TOKEN={access_token}\n")
                if access_token_secret:
                    f.write(f"ACCESS_TOKEN_SECRET={access_token_secret}\n")
            print("Saved to .env")

prompt_for_missing_env()

async def main():
    plurk = PlurkAPI(consumer_key, consumer_secret)
    plurk.authorize(access_token, access_token_secret)

    if len(sys.argv) == 1:
        user_names_list = input("Please enter at least one username OR several usernames with space separated:")
        user_names_list = user_names_list.split()
    else:
        user_names_list = sys.argv[1:]
    #async with aiomultiprocess.Pool() as pool:
    await asyncio.gather(*[process_user(plurk, user_name) for user_name in user_names_list])
  
if __name__ == "__main__":
    t1 = time.time()
    asyncio.run(main())
    print("============================\nTotal time: {}\n".format(time.time() - t1))
