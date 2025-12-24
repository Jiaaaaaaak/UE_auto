🚀 UE_auto — Uber Eats 商家後台自動化

自動化操作 Uber Eats 商家後台，使用 Python Playwright + Persistent Context，自動完成登入後下載報表流程。

⭐ 核心特色

以 Playwright Persistent Context 保存登入狀態

自動切換日期區間

擷取並下載資料（CSV、後續可擴充）

適合排程與定時執行

📌 需求環境

Python 3.10+

Git

uv for virtualenv 管理

支援 OS：Windows / macOS / Linux

基本檢查指令：

python --version
uv --version

📁 專案結構
UE_auto/
├─ .venv/                 # 虛擬環境（不推送）
├─ user_data/             # Playwright登入狀態
├─ reports/               # 下載報表
├─ automation/            # 自動化邏輯
│  ├─ main.py             # 主要流程
│  ├─ core/
│     ├─ browser.py       # 啟動 Playwright
│     ├─ navigation.py    # 導航與下載
│     ├─ date_ranges.py   # 日期運算
│     └─ storage.py       # 檔案儲存
├─ requirements.txt
├─ .gitignore
└─ README.md

🚀 開始步驟
1️⃣ clone專案
git clone <repo_url>
cd UE_auto

2️⃣ 建立虛擬環境

使用 uv：

uv venv .venv


啟用：

Windows：

.venv\Scripts\activate


macOS / Linux：

source .venv/bin/activate

3️⃣ 安裝套件
uv pip install -r requirements.txt

4️⃣ 安裝 Playwright 瀏覽器
playwright install


✅ 每台機器需要執行一次

🔐 第一次登入

本專案不自動化 Google 登入流程。
請：

確保 headless=False

執行：

python automation/main.py


手動登入 Google 帳號

成功後關閉瀏覽器

登入狀態會保存在 user_data/

✅ 日常執行

如已登入：

python automation/main.py


可結合排程 (cron, Windows Task Scheduler) 自動執行。