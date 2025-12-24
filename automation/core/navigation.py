# core/navigation.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from core.selectors import download_button
from core.file_utils import csv_to_xlsx_only, sanitize_filename

BASE_URL = "https://merchants.ubereats.com/manager/home"
REPORT_ROOT = Path("reports")


def build_report_url(store_id: str, report_path: str, start: str, end: str) -> str:
    return f"{BASE_URL}/{store_id}{report_path}?dateRange=custom&start={start}&end={end}"


def goto_report_page(page: Page, url: str) -> None:
    page.goto(url, wait_until="domcontentloaded")


@dataclass(frozen=True)
class DownloadMeta:
    store_name: str
    report_key: str
    preset_key: str
    start: str
    end: str


def download_report_as_xlsx(page: Page, meta: DownloadMeta) -> Path:
    """
    下載報表（通常會是 CSV）→ 轉成 XLSX → 刪除 CSV
    最終只回傳 XLSX 路徑
    """
    safe_store = sanitize_filename(meta.store_name)
    safe_report = sanitize_filename(meta.report_key)
    safe_preset = sanitize_filename(meta.preset_key)

    store_dir = REPORT_ROOT / safe_store / safe_report
    store_dir.mkdir(parents=True, exist_ok=True)

    btn = download_button(page)

    try:
        btn.wait_for(timeout=60_000)
        with page.expect_download(timeout=60_000) as download_info:
            btn.click()
        download = download_info.value
    except PlaywrightTimeoutError:
        raise RuntimeError(f"下載逾時：{meta.store_name} | {meta.report_key} | {meta.preset_key}")

    # 先用官方檔名存成 CSV（中繼）
    suggested = sanitize_filename(download.suggested_filename)
    csv_path = store_dir / suggested
    download.save_as(csv_path)

    # 最終檔名（明確）
    # 例：小伍手路鍋_sales_last_month_2025-11-01_2025-11-30.xlsx
    xlsx_name = f"{safe_store}_{safe_report}_{safe_preset}_{meta.start}_{meta.end}.xlsx"
    xlsx_path = store_dir / xlsx_name

    final_path = csv_to_xlsx_only(csv_path, xlsx_path)
    return final_path
