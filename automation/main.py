# automation/main.py
from __future__ import annotations

from pathlib import Path

from core.browser import BrowserManager
from core.navigation import (
    DownloadMeta,
    build_report_url,
    goto_report_page,
    download_report_as_xlsx,
)
from core.file_utils import merge_xlsx_to_summary, sanitize_filename

from configs.stores import STORES
from configs.defaults import DEFAULT_DATE_PRESETS
from configs.reports_types import REPORT_TYPES
from configs.date_ranges import (
    DATE_PRESET_REGISTRY,
    resolve_date_range,
    DatePreset,
)


def main() -> None:
    browser = BrowserManager(
        user_data_dir="user_data",
        download_dir="tmp_downloads",  # 只是給 Playwright 用，實際我們自己 save_as
        headless=False,
    )

    context = browser.start()
    page = context.new_page()


    # 收集每家店/每種報表下載到的 xlsx（用來做 summary）
    downloaded_index: dict[tuple[str, str], list[Path]] = {}

    for store in STORES:
        store_name: str = store["name"]
        store_id: str = store["store_id"]

        preset_keys = store.get("date_presets", DEFAULT_DATE_PRESETS)

        for preset_key in preset_keys:
            preset = DATE_PRESET_REGISTRY[preset_key]
            start, end = resolve_date_range(preset)

            for report in REPORT_TYPES:
                report_key: str = report["key"]
                report_path: str = report["path"]

                url = build_report_url(store_id, report_path, start, end)
                print(f"▶ {store_name} | {report_key} | {preset_key} | {start}~{end}")

                goto_report_page(page, url)

                meta = DownloadMeta(
                    store_name=store_name,
                    report_key=report_key,
                    preset_key=preset_key,
                    start=start,
                    end=end,
                )

                xlsx_path = download_report_as_xlsx(page, meta)
                print(f"✅ 完成：{xlsx_path}")

                downloaded_index.setdefault((store_name, report_key), []).append(xlsx_path)

    # === 合併 summary（每家店 × 每種報表各一份）===
    for (store_name, report_key), files in downloaded_index.items():
        safe_store = sanitize_filename(store_name)
        safe_report = sanitize_filename(report_key)

        out_path = Path("reports") / safe_store / safe_report / f"{safe_store}_{safe_report}_SUMMARY.xlsx"
        summary = merge_xlsx_to_summary(
            files,
            out_path,
            extra_columns={"store": store_name, "report": report_key},
        )
        print(f"📊 Summary 產出：{summary}")


if __name__ == "__main__":
    main()
