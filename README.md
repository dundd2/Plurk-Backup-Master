# Plurk-Backup-Master
⚡ Still working as of November 2024 ⚡  截至 2024 年 11 月仍在工作 ⚡

Easily download all Plurks images, messages and replies posted by a specific Plurks user (including images and messages in the replies below) from plurk.com
輕鬆下載特定 Plurks 用戶發布的所有 Plurks 圖像,訊息和回复 

## Screenshot 螢幕截圖:
![1](https://github.com/user-attachments/assets/91ac9c4f-1701-4eb3-8e32-b48544d7eff9)


## V1.1 28/NOV/2024 Changes Made 更新內容 

1. Code Structure Changes 程式碼結構變更:
   - Separated utility functions into utils.py
   - Improved code organization and modularity
   - Removed duplicate functions

2. Performance Improvements 效能改進:
   - Optimized async/await implementation
   - Better error handling in URL validation
   - Improved session management

3. Features Added 新增功能:
   - Added text content saving for both plurks and responses
   - Better file naming convention for saved content
   - Enhanced logging of download status

4. Bug Fixes 錯誤修正:
   - Fixed URL validation regex pattern
   - Improved error handling in API calls
   - Fixed duplicate downloads issues
   - Better handling of timeouts and connection errors

5. File Organization 檔案組織:
   - Moved from single file to modular structure
   - Created a separate utility module
   - Better separation of concerns


## Acknowledgment 致謝 

Most of this project is based on the original Plurk Crawler by [freelze](https://github.com/freelze). I express my sincere thanks to freelze for their contribution to the Plurk Crawler project.

本專案大部分基於 [freelze](https://github.com/freelze) 原始的 Plurk Crawler。我衷心感謝 freelze 對 Plurk Crawler 專案的貢獻。

I edited the code using ChatGPT so that the script can now download all images, messages, and replies (including images and messages in the replies below) not just only download images in the Plurk Crawler.

我使用 ChatGPT 編輯了程式碼，讓腳本現在可以下載所有文字訊息和圖片，包括回覆中的圖片和文字訊息，而不僅僅是 Plurk Crawler 中的圖片。

## Disclaimer 免責聲明 (Disclaimer)

I want to clarify that I do not own any of the code in this project. This project is based on the original Plurk Crawler by [freelze](https://github.com/freelze), and ChatGPT enhances it.

我想澄清的是，我並不擁有本專案中的任何程式碼。這個專案大部分基於 [freelze](https://github.com/freelze) 的原始 Plurk Crawler，我使用 ChatGPT /GitHub Copilot 編輯。

## Getting Started 前置作業 

### Install Python 3.12+ 安裝 Python 3.12+ 
### Clone the repository 下載程式碼 

    git clone https://github.com/dundd2/Plurk-Backup-Master.git

### Open a terminal or command prompt 開啟終端機或命令提示字元 

### Install Python dependencies: 安裝 Python 相關套件 

    pip install -r requirements.txt

### Register for a Plurk account 註冊 Plurk 帳號:
https://www.plurk.com/signup

### Apply for API service 申請 API 服務: 
http://www.plurk.com/PlurkApp/

Please refer to Dada’s teaching text: https://dada.tw/2011/10/28/426/

請參考 dada 的教學文: https://dada.tw/2011/10/28/426/ 

Get 取得 
+ App Key
+ App Secret
+ Access Token
+ Access Token Secret

### Rename .env.example to .env and update the credentials accordingly. 
### 修改檔名，將 .env.example 檔案重新命名為 .env 

### Update the keys in the .env file 修改 .env 檔案的金鑰 :

+ CONSUMER_KEY=***你的App Key放這裡 your App Key here***
+ CONSUMER_SECRET=***你的App Secret放這裡 your App Secret here*** 
+ ACCESS_TOKEN=***你的Access Token放這裡 your Access Token here***
+ ACCESS_TOKEN_SECRET=***你的Access Token Secret放這裡 your Access Token Secret here***

# Run the script: 執行程式

    python main.py username1 username2 username3

`username` 就是網址 http://www.plurk.com/使用者帳號 的 `使用者帳號` 
`username` is the `user account` in the URL http://www.plurk.com/user_account

Replace username1, username2, etc., with the Plurk usernames whose images and messages you want to download.
