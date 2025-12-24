# core/file_utils.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd


ENCODINGS_TO_TRY: list[str] = ["utf-8", "utf-8-sig", "cp950", "big5"]


def sanitize_filename(name: str) -> str:
    """
    Windows 檔名不可含: \ / : * ? " < > |
    """
    bad = '\\/:*?"<>|'
    for ch in bad:
        name = name.replace(ch, "_")
    return name.strip()


def csv_to_xlsx_only(csv_path: Path, xlsx_path: Path) -> Path:
    """
    CSV → DataFrame（自動嘗試編碼）→ XLSX
    成功後刪除 CSV（只留 XLSX）
    """
    last_error: Exception | None = None

    for enc in ENCODINGS_TO_TRY:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            xlsx_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_excel(xlsx_path, index=False)

            # 只留 xlsx
            csv_path.unlink(missing_ok=True)

            return xlsx_path
        except Exception as e:
            last_error = e

    raise RuntimeError(f"CSV 轉 XLSX 失敗：{csv_path}，最後錯誤：{last_error}")


def merge_xlsx_to_summary(
    xlsx_files: Iterable[Path],
    out_path: Path,
    extra_columns: Optional[dict[str, str]] = None,
) -> Path:
    """
    合併多個 xlsx 成一份 summary。
    - extra_columns：可額外加欄位（例如 store/report）
    """
    frames: list[pd.DataFrame] = []

    for f in xlsx_files:
        if not f.exists():
            continue
        df = pd.read_excel(f)
        df["__source_file"] = f.name
        frames.append(df)

    if not frames:
        raise RuntimeError(f"找不到可合併的 xlsx：{out_path.parent}")

    merged = pd.concat(frames, ignore_index=True)

    if extra_columns:
        for k, v in extra_columns.items():
            merged[k] = v

    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_excel(out_path, index=False)
    return out_path
