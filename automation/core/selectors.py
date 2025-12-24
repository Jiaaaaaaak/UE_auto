# core/selectors.py
from __future__ import annotations

from playwright.sync_api import Locator, Page


def download_button(page: Page) -> Locator:
    """
    Uber Eats 後台常見「下載」按鈕定位。
    - 避免 strict mode：只取可見的第一顆
    - 避免 class / data-baseweb 這種不穩定定位
    """
    # 可能是「下載」或「Download 下載」等，先用 has-text 包住
    return page.locator("button:has-text('下載')").locator(":visible").first
