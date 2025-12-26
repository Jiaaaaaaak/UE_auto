from __future__ import annotations

from pathlib import Path
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from core.selectors import (
    sales_download_button,
    customers_download_button,
)
from core.file_utils import csv_to_xlsx_only, sanitize_filename

BASE_URL = "https://merchants.ubereats.com/manager/home"
REPORT_ROOT = Path("reports")
REPORT_PATHS = {
    "sales": "/analytics/sales-v2",
    "customers": "/analytics/customers",
}


# ---------- URL ----------

def build_report_url(store_id: str, report_key: str, start: str, end: str) -> str:
    return (
        f"{BASE_URL}/{store_id}{REPORT_PATHS[report_key]}"
        f"?dateRange=custom&start={start}&end={end}"
    )



def goto_report_page(page: Page, url: str) -> None:
    # ① 只等 DOM 出來（不要等 network）
    page.goto(url, wait_until="domcontentloaded")

    # ② 給 React 一點時間初始化
    page.wait_for_timeout(1500)

    # ③ 等「至少一顆下載按鈕出現」
    page.wait_for_selector(
        "button:has-text('下載')",
        timeout=30_000
    )


# ---------- 下載核心（保證會動） ----------

def _download_csv(page: Page, btn) -> Path:
    btn.wait_for(state="visible", timeout=30_000)

    # 確保在畫面內
    btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    # 強制點擊，避免 overlay / animation
    with page.expect_download(timeout=60_000) as download_info:
        btn.click(force=True)

    download = download_info.value
    return Path(download.path())


# ---------- Sales（一定要分開 reload） ----------

def download_sales_reports(
    page: Page,
    url: str,
    store_name: str,
    preset_key: str,
    start: str,
    end: str,
) -> None:
    # ① 銷售額
    goto_report_page(page, url)

    try:
        csv_path = _download_csv(page, sales_download_button(page, 0))
    except PlaywrightTimeoutError:
        print(f"⚠️ 銷售額下載失敗：{store_name}")
    else:
        _finalize_report(
            csv_path,
            store_name,
            "sales_amount",
            preset_key,
            start,
            end,
        )

    # ② 轉換率（重新進頁面，避免 SPA state 殘留）
    goto_report_page(page, url)

    try:
        csv_path = _download_csv(page, sales_download_button(page, 1))
    except PlaywrightTimeoutError:
        print(f"⚠️ 轉換率下載失敗：{store_name}")
    else:
        _finalize_report(
            csv_path,
            store_name,
            "sales_conversion",
            preset_key,
            start,
            end,
        )


# ---------- Customers ----------

def download_customers_report(
    page: Page,
    url: str,
    store_name: str,
    preset_key: str,
    start: str,
    end: str,
) -> None:
    goto_report_page(page, url)

    try:
        csv_path = _download_csv(page, customers_download_button(page))
    except PlaywrightTimeoutError:
        print(f"⚠️ Customers 下載失敗：{store_name}")
        return

    _finalize_report(
        csv_path,
        store_name,
        "customers",
        preset_key,
        start,
        end,
    )


# ---------- 儲存與轉檔 ----------

def _finalize_report(
    csv_path: Path,
    store_name: str,
    report_key: str,
    preset_key: str,
    start: str,
    end: str,
) -> None:
    safe_store = sanitize_filename(store_name)
    safe_report = sanitize_filename(report_key)
    safe_preset = sanitize_filename(preset_key)

    out_dir = REPORT_ROOT / safe_store / safe_report
    out_dir.mkdir(parents=True, exist_ok=True)

    xlsx_name = f"{safe_store}_{safe_report}_{safe_preset}_{start}_{end}.xlsx"
    xlsx_path = out_dir / xlsx_name

    csv_to_xlsx_only(csv_path, xlsx_path)

    print(f"✅ 已下載：{xlsx_path}")



# # core/navigation.py
# from __future__ import annotations

# from dataclasses import dataclass
# from pathlib import Path

# from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

# from core.selectors import (
#     sales_download_button,
#     customers_download_button,
# )
# from core.file_utils import csv_to_xlsx_only, sanitize_filename

# BASE_URL = "https://merchants.ubereats.com/manager/home"
# REPORT_ROOT = Path("reports")




# def build_report_url(store_id: str, report_path: str, start: str, end: str) -> str:
#     return f"{BASE_URL}/{store_id}{report_path}?dateRange=custom&start={start}&end={end}"


# def goto_report_page(page: Page, url: str) -> None:
#     page.goto(url, wait_until="domcontentloaded")

# # NOTE:
# # DownloadMeta is reserved for future async / pipeline usage
# @dataclass(frozen=True)
# class DownloadMeta:
#     store_name: str
#     report_key: str
#     preset_key: str
#     start: str
#     end: str



# def download_report_as_xlsx(page: Page, meta: DownloadMeta) -> Path:
#     """
#     下載報表（通常會是 CSV）→ 轉成 XLSX → 刪除 CSV
#     最終只回傳 XLSX 路徑
#     """
#     safe_store = sanitize_filename(meta.store_name)
#     safe_report = sanitize_filename(meta.report_key)
#     safe_preset = sanitize_filename(meta.preset_key)

#     store_dir = REPORT_ROOT / safe_store / safe_report
#     store_dir.mkdir(parents=True, exist_ok=True)

#     btn = download_button(page)

#     try:
#         btn.wait_for(timeout=60_000)
#         with page.expect_download(timeout=60_000) as download_info:
#             btn.click()
#         download = download_info.value
#     except PlaywrightTimeoutError:
#         raise RuntimeError(f"下載逾時：{meta.store_name} | {meta.report_key} | {meta.preset_key}")

#     # 先用官方檔名存成 CSV（中繼）
#     suggested = sanitize_filename(download.suggested_filename)
#     csv_path = store_dir / suggested
#     download.save_as(csv_path)

#     # 最終檔名（明確）
#     # 例：小伍手路鍋_sales_last_month_2025-11-01_2025-11-30.xlsx
#     xlsx_name = f"{safe_store}_{safe_report}_{safe_preset}_{meta.start}_{meta.end}.xlsx"
#     xlsx_path = store_dir / xlsx_name

#     final_path = csv_to_xlsx_only(csv_path, xlsx_path)
#     return final_path
