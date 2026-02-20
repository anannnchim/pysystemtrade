#!/usr/bin/env python3
"""
modify_contract_position.py

Append (date, position) to a contract_positions parquet file
without breaking its schema (date may be an index or a column).

Best practice:
- Detect schema
- Append in the same format
- Atomic overwrite (temp -> replace)
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

PARQUET_ENGINE = "pyarrow"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.expand_frame_repr", False)


def append_contract_position(file_path: str, date_str: str, position: float, allow_overwrite_same_date: bool = False):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_parquet(path, engine=PARQUET_ENGINE)

    new_dt = pd.to_datetime(date_str)

    # ------------------------------------------------------------
    # Case A: date is stored as DatetimeIndex (common in time series)
    # ------------------------------------------------------------
    if isinstance(df.index, pd.DatetimeIndex) and "date" not in df.columns:
        # duplicate handling
        if (new_dt in df.index) and not allow_overwrite_same_date:
            raise ValueError(f"Date already exists in index: {new_dt} (set allow_overwrite_same_date=True to overwrite)")

        # append / overwrite
        df2 = df.copy()
        df2.loc[new_dt, "position"] = float(position)
        df2 = df2.sort_index()

        # atomic write (keep index!)
        tmp = path.with_suffix(path.suffix + ".tmp")
        df2.to_parquet(tmp, engine=PARQUET_ENGINE, index=True)
        tmp.replace(path)

        print("Appended successfully (DatetimeIndex schema).")
        print(df2.tail())
        return

    # ------------------------------------------------------------
    # Case B: date is stored as a 'date' column
    # ------------------------------------------------------------
    if "date" in df.columns:
        df2 = df.copy()
        df2["date"] = pd.to_datetime(df2["date"], errors="coerce")

        # duplicate handling
        if (df2["date"] == new_dt).any() and not allow_overwrite_same_date:
            raise ValueError(f"Date already exists in column 'date': {new_dt} (set allow_overwrite_same_date=True to overwrite)")

        # if overwriting allowed: drop existing same date first
        if allow_overwrite_same_date:
            df2 = df2[df2["date"] != new_dt]

        new_row = pd.DataFrame({"date": [new_dt], "position": [float(position)]})
        df2 = pd.concat([df2, new_row], ignore_index=True).sort_values("date")

        # atomic write (no index)
        tmp = path.with_suffix(path.suffix + ".tmp")
        df2.to_parquet(tmp, engine=PARQUET_ENGINE, index=False)
        tmp.replace(path)

        print("Appended successfully ('date' column schema).")
        print(df2)
        return

    # ------------------------------------------------------------
    # Unknown schema
    # ------------------------------------------------------------
    raise ValueError(
        "Unknown parquet schema. Expected either:\n"
        "- DatetimeIndex + 'position' column, OR\n"
        "- 'date' and 'position' columns.\n"
        f"Got columns={list(df.columns)} index_type={type(df.index)}"
    )


if __name__ == "__main__":
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/contract_positions/IRON#20260400.parquet"

    # your provided data
    date = "2026-02-20 10:46:57.455980"
    position = 0.0

    append_contract_position(file_path, date, position)