from core.browser import BrowserManager

STORE_NAME = "日植"   # ← 你要測的店
USER_DATA_DIR = f"user_data/{STORE_NAME}"

def main():
    browser_manager = BrowserManager(
        user_data_dir=USER_DATA_DIR,
        headless=False,
    )

    context = browser_manager.start()
    page = context.new_page()

    # 只打開後台首頁，不跑任何下載
    page.goto("https://merchants.ubereats.com/manager/home")

    print("👉 請用眼睛確認：")
    print("1. 是否已登入")
    print(f"2. 左上角顯示的商店是否是：{STORE_NAME}")
    print("3. 若不是，請手動切換一次商店")

    # 不關閉，讓你操作
    page.wait_for_timeout(60_000)


if __name__ == "__main__":
    main()
