from __future__ import annotations

import argparse
import sys

from core.browser import BrowserManager
from core.navigation import (
    build_report_url,
    download_sales_reports,
    download_customers_report,
)
from configs.stores import STORES
from configs.date_ranges import DATE_PRESET_REGISTRY, resolve_date_range


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Uber Eats 報表自動下載（一次只跑一間商店）"
    )
    parser.add_argument(
        "--store",
        required=True,
        help="商店名稱（需與 configs/stores.py 中的 name 完全一致）",
    )
    return parser.parse_args()


def find_store(store_name: str) -> dict:
    for store in STORES:
        if store["name"] == store_name:
            return store
    raise ValueError(f"找不到商店：{store_name}")


def main() -> None:
    args = parse_args()

    try:
        store = find_store(args.store)
    except ValueError as e:
        print(f"❌ {e}")
        print("👉 可用商店清單：")
        for s in STORES:
            print(f" - {s['name']}")
        sys.exit(1)

    store_name = store["name"]
    store_id = store["store_id"]
    safe_store_key = store_name.replace(" ", "_")
    user_data_dir = f"user_data/{safe_store_key}"
    print(f"\n🏪 目標商店：{store_name}")

    # ======================
    # 啟動 Persistent Context（只能一次）
    # ======================
    browser_manager = BrowserManager(
        user_data_dir=user_data_dir,
        download_dir="reports",
        headless=False,
    )

    context = browser_manager.start()
    page = context.new_page()
   
    try:
        preset_keys = store.get("date_presets")
        if isinstance(preset_keys, str):
            preset_keys = [preset_keys]

        if not preset_keys:
            raise ValueError(f"{store_name} 未設定 date_presets")

        for preset_key in preset_keys:
            preset = DATE_PRESET_REGISTRY[preset_key]
            start, end = resolve_date_range(preset)

            print(f"  📅 區間：{preset_key} | {start} ~ {end}")

            # ---------- Sales ----------
            sales_url = build_report_url(
                store_id=store_id,
                report_key="sales",
                start=start,
                end=end,
            )

            download_sales_reports(
                page=page,
                url=sales_url,
                store_name=store_name,
                preset_key=preset_key,
                start=start,
                end=end,
            )

            # ---------- Customers ----------
            customers_url = build_report_url(
                store_id=store_id,
                report_key="customers",
                start=start,
                end=end,
            )

            download_customers_report(
                page=page,
                url=customers_url,
                store_name=store_name,
                preset_key=preset_key,
                start=start,
                end=end,
            )

    finally:
        # ❗ 不 stop browser，保留登入
        print("\n✅ 報表下載完成（單一商店）")


if __name__ == "__main__":
    main()
