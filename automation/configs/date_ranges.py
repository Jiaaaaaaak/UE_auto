# configs/date_ranges.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, Tuple, Literal


PresetType = Literal[
    "last_n_days",
    "this_month",
    "last_month",
    "custom",
]


@dataclass(frozen=True)
class DatePreset:
    key: str
    type: PresetType
    value: int | None = None
    start: str | None = None
    end: str | None = None


def resolve_date_range(preset: DatePreset) -> Tuple[str, str]:
    """
    回傳 ISO 格式日期字串 (YYYY-MM-DD, YYYY-MM-DD)
    """
    today = date.today()

    if preset.type == "last_n_days":
        if preset.value is None:
            raise ValueError("last_n_days 需要 value")
        start = today - timedelta(days=preset.value - 1)
        end = today

    elif preset.type == "this_month":
        start = today.replace(day=1)
        end = today

    elif preset.type == "last_month":
        first_day_this_month = today.replace(day=1)
        end = first_day_this_month - timedelta(days=1)
        start = end.replace(day=1)

    elif preset.type == "custom":
        if not preset.start or not preset.end:
            raise ValueError("custom 需要 start / end")
        return preset.start, preset.end

    else:
        raise ValueError(f"未知的 preset type: {preset.type}")

    return start.isoformat(), end.isoformat()


# 👉 唯一對外的 registry
DATE_PRESET_REGISTRY: Dict[str, DatePreset] = {
    "last_7_days": DatePreset(
        key="last_7_days",
        type="last_n_days",
        value=7,
    ),
    "this_month": DatePreset(
        key="this_month",
        type="this_month",
    ),
    "last_month": DatePreset(
        key="last_month",
        type="last_month",
    ),
    "custom_2024_01": DatePreset(
        key="custom_2024_01",
        type="custom",
        start="2024-01-01",
        end="2024-01-31",
    ),
}
