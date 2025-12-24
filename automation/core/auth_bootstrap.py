# core/auth_bootstrap.py
from playwright.sync_api import Page


def manual_login_once(page: Page) -> None:
    page.goto(
        "https://merchants.ubereats.com/manager/home",
        wait_until="domcontentloaded",
    )

    input("👉 請完成登入後按 Enter")

    print("✅ 登入狀態已儲存到 user_data")
