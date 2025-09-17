# Plurk-Backup-Master
⚡ Still working as of November 2024 ⚡  截至 2024 年 11 月仍在工作 ⚡

Easily download all Plurks images, messages and replies posted by a specific Plurks user (including images and messages in the replies below) from plurk.com
輕鬆下載特定 Plurks 用戶發布的所有 Plurks 圖像,訊息和回复 

## Screenshot 螢幕截圖:
![1](https://github.com/user-attachments/assets/91ac9c4f-1701-4eb3-8e32-b48544d7eff9)


## Getting Started 前置作業 

### Install Python 3.11+ 安裝Python 3.11+
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

There are three ways to download a user's Plurks (images, messages and replies):

有三種方式可下載使用者的 Plurk（包含圖像、訊息與回覆）：

1) Graphical interface (recommended for most users) / 圖形介面（大多數使用者推薦）

   - Run the GUI that provides a simple form, progress bar and status badges:

     執行圖形化介面，介面包含簡單的表單、進度條與狀態徽章：

      python ui_app.py

   - Fill in the API credentials and the Plurk usernames to back up, then click **Start Backup / 開始備份**.

     在介面中填入 API 金鑰與欲備份的 Plurk 使用者名稱，然後按下 **Start Backup / 開始備份**。

2) Command-line with usernames (non-interactive) / 命令列指定使用者（非互動）

   - Provide one or more usernames as command-line arguments. This is useful for scripting or running in a terminal:

     在命令列中提供一個或多個使用者名稱，可用於腳本化或在終端機中執行：

      python main.py username1 username2 username3

   - Example:

     範例：

      python main.py alice bob charlie

   - `username` is the `user account` in the URL `http://www.plurk.com/user_account`.

     `username` 是出現在 `http://www.plurk.com/user_account` 中的使用者帳號。

3) Run `main.py` directly (interactive prompt) / 直接執行 `main.py`（互動式）

   - Run the script without arguments and it will prompt you to enter one or more usernames:

     不帶參數執行腳本，程式會提示您輸入一個或多個使用者名稱：

      python main.py

   - On Windows you can also run the file directly (e.g., double-click `main.py` in Explorer) but note that a console window is required to provide input and to see progress. Running from a terminal is recommended so you can see any prompts or messages.

     在 Windows 中也可以直接執行檔案（例如在檔案總管中雙擊 `main.py`），但需要有主控台視窗來提供輸入並檢視進度。建議在終端機中執行以便看到提示與輸出資訊。

Notes / 注意事項:

- The script reads API credentials from a `.env` file (see above). If credentials are missing, `main.py` will interactively prompt you to enter them and offer to save them to a local `.env` file.

  腳本會從 `.env` 檔案讀取 API 金鑰（見上文）。若金鑰缺失，`main.py` 將互動式提示您輸入，並可選擇將其儲存到本地 `.env` 檔案。

- Use the GUI (`python ui_app.py`) if you prefer a visual workflow and progress indicators. The CLI mode (`python main.py username...`) is great for automation and scripts. The interactive run is convenient for quick, one-off archives.

  若偏好視覺化操作與進度顯示，請使用 GUI（`python ui_app.py`）。若要自動化或在腳本中使用，請採用 CLI（`python main.py username...`）。不帶參數直接執行的互動模式適合快速的單次備份。

- Replace `username1`, `username2`, etc., with the Plurk usernames whose images and messages you want to download.

  將 `username1`、`username2` 等替換為欲下載圖像與訊息的 Plurk 使用者帳號。

  
## Acknowledgment 致謝 

Most of this project is based on the original Plurk Crawler by [freelze](https://github.com/freelze). I express my sincere thanks to freelze for their contribution to the Plurk Crawler project.

本專案大部分基於 [freelze](https://github.com/freelze) 原始的 Plurk Crawler。我衷心感謝 freelze 對 Plurk Crawler 專案的貢獻。

I edited the code using ChatGPT so that the script can now download all images, messages, and replies (including images and messages in the replies below) not just only download images in the Plurk Crawler.

我使用 ChatGPT 編輯了程式碼，讓腳本現在可以下載所有文字訊息和圖片，包括回覆中的圖片和文字訊息，而不僅僅是 Plurk Crawler 中的圖片。

## Disclaimer 免責聲明 (Disclaimer)

I want to clarify that I do not own any of the code in this project. This project is based on the original Plurk Crawler by [freelze](https://github.com/freelze), and ChatGPT enhances it.

我想澄清的是，我並不擁有本專案中的任何程式碼。這個專案大部分基於 [freelze](https://github.com/freelze) 的原始 Plurk Crawler，我使用 ChatGPT /GitHub Copilot 編輯。