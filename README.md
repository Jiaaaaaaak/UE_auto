# UE Automate – Uber Eats 商家後台自動化（Playwright + uv）

這是一個使用 **Playwright（Python）** 搭配 **Persistent Context** 的自動化專案，用來在 **Uber Eats 商家後台** 中，自動完成以下工作：

* 使用既有登入狀態（Google OAuth，一次人工登入）
* 自動點擊側邊欄（成效 → 銷售額）
* 切換日期區間
* 擷取畫面上的數據
* 匯出成 CSV（或後續擴充）

> ⚠️ 本專案屬於「**瀏覽器自動化（Browser Automation）**」，不是 API 爬蟲。

---

## 一、系統需求（Prerequisites）

請先確認你的環境符合以下條件：

* Python **3.10 以上**（建議 3.11 / 3.12）
* 已安裝 **uv**
* 已安裝 Git
* 作業系統：Windows / macOS / Linux 皆可

檢查版本：

```bash
python --version
uv --version
```

---

## 二、專案結構說明

```text
UE_automate/
├── .venv/                     # uv 建立的虛擬環境（不進 git）
├── user_data/                 # Playwright Persistent Context（登入狀態，不進 git）
├── reports/                   # 下載的報表（程式自動建立）
├── automation/
│   ├── main.py                # ⭐ 主流程（日期輪詢＋下載）
│   └── core/
│       ├── browser.py         # Persistent Context 啟動
│       ├── navigation.py      # URL 組裝 + 下載報表
│       ├── date_ranges.py     # ⭐ 日期邏輯（昨天 / 上週 / 上月）
│       └── storage.py         #（可選，之後整理檔案用）
├── requirements.txt
├── .gitignore
└── README.md

```

---

## 三、第一次在新電腦的安裝 SOP（必看）

### Step 1️⃣ clone 專案

```bash
git clone <你的 repo URL>
cd UE_automate
```

---

### Step 2️⃣ 使用 uv 建立虛擬環境

```bash
uv venv .venv
```

啟用虛擬環境：

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

看到前面出現 `(.venv)` 即代表成功。

---

### Step 3️⃣ 安裝 Python 套件

```bash
uv pip install -r requirements.txt
```

---

### Step 4️⃣ 安裝 Playwright 瀏覽器（非常重要）

```bash
playwright install
```

> ⚠️ 每一台新電腦都必須執行一次

---

### Step 5️⃣ 驗證環境

```bash
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

若輸出 `OK`，代表環境完成。

---

## 四、第一次登入（只做一次）

本專案**不自動化 Google 登入流程**，而是使用 Playwright 的 **Persistent Context**。

### 操作方式

1. 確保 `headless=False`
2. 執行主程式

```bash
python automation/main.py
```

3. 瀏覽器會打開 Uber Eats 商家後台
4. **請手動使用 Google 帳號登入**
5. 成功進入後台後，關閉瀏覽器

👉 登入狀態會被保存在 `user_data/` 資料夾中
👉 **之後不需要再登入**

---

## 五、之後的日常使用（全自動）

只要確保：

* `user_data/` 還存在
* 沒被 Uber Eats / Google 強制登出

即可直接執行：

```bash
.venv\Scripts\activate   # Windows
python automation/main.py
```

或（macOS / Linux）：

```bash
source .venv/bin/activate
python automation/main.py
```

---

## 六、重要注意事項（請務必閱讀）

### ⚠️ 1. user_data/ = 你的身分

* 不要 commit
* 不要傳給別人
* 不要同時被兩個程式使用

---

### ⚠️ 2. 同一時間只能跑一個實例

同一個 `user_data/`：

* ❌ 不能平行執行
* ❌ 不能多開

---

### ⚠️ 3. 被登出怎麼辦？

* 刪除 `user_data/`
* 再跑一次主程式
* 重新手動登入一次即可

---

## 七、為什麼要用 uv？

* 比 pip + venv 快很多
* 鎖定環境一致性
* 換電腦可快速重建

常用指令對照：

| 傳統                              | uv                                 |
| ------------------------------- | ---------------------------------- |
| python -m venv .venv            | uv venv .venv                      |
| pip install -r requirements.txt | uv pip install -r requirements.txt |

---

## 八、常見問題（FAQ）

### Q1：換一台電腦還要重裝嗎？

✅ **要**，請重新執行：

* `uv venv .venv`
* `uv pip install -r requirements.txt`
* `playwright install`

---

### Q2：為什麼不用 Selenium？

Playwright：

* 對 SPA / React 更穩
* selector 更好用
* 原生支援 Persistent Context

---

### Q3：可以 headless 跑嗎？

* 第一次登入：❌ 不建議
* 日常自動化：✅ 可以

---

## 九、定位說明（很重要）

這個專案是：

> **企業後台瀏覽器自動化工程**

不是：

* API 爬蟲
* requests 抓資料
* 逆向私有 API

---

## 十、下一步可擴充方向

* 排程（Windows Task Scheduler / cron）
* 匯出 Excel
* 存入資料庫
* 登入存活檢查
* 異常通知（Line / Email）

---

如果你是第一次接手這個專案：

👉 **請從「第三章」開始照著做**

---

✦ 本 README 為專案標準操作文件，請勿將 `user_data/` 上傳至任何公開平台。
