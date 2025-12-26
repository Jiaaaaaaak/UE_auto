from __future__ import annotations
from playwright.sync_api import Page, Locator


def sales_download_button(page: Page, index: int) -> Locator:
    """
    Sales 頁下載按鈕
    index:
      0 = 銷售額
      1 = 轉換率
    ⚠️ 前提：頁面已 reload + networkidle
    """
    return page.get_by_role("button", name="下載").nth(index)


def customers_download_button(page: Page) -> Locator:
    """
    Customers 頁下載按鈕
    - 明確指定第二顆
    """
    return page.get_by_role("button", name="下載").nth(1)

# # core/selectors.py
# from __future__ import annotations
# from playwright.sync_api import Page, Locator


# def sales_download_button(page: Page, index: int) -> Locator:
#     """
#     sales 頁面下載按鈕
#     index:
#       0 = 銷售額摘要
#       1 = 轉換率 / 明細
#     """
#     return (
#         page.locator("button:has-text('下載')")
#         .locator(":visible")
#         .nth(index)
#     )


# def customers_download_button(page: Page) -> Locator:
#     """
#     customers 頁面下載按鈕
#     - 此頁面有兩顆下載
#     - 明確指定使用第二顆
#     """
#     return (
#         page.locator("button:has-text('下載')")
#         .locator(":visible")
#         .nth(1)
#     )
