#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

SPREAD_PATH = Path("/home/anan/AnanProjects/pysystemtrade/data/parquet/spreads")

TARGET_DATE = pd.Timestamp("2026-01-01")


def check_file(file_path):
    instrument = file_path.stem

    try:
        df = pd.read_parquet(file_path)

        # assume standard format (you confirmed already)
        series = df.iloc[:, 0] if isinstance(df, pd.DataFrame) else df

        index = series.index

        has_date = TARGET_DATE in index

        min_date = index.min()
        max_date = index.max()

        return {
            "instrument": instrument,
            "has_date": has_date,
            "min_date": min_date,
            "max_date": max_date,
        }

    except Exception as e:
        return {
            "instrument": instrument,
            "error": str(e),
        }


def main():
    files = list(SPREAD_PATH.glob("*.parquet"))

    missing = []
    present = []

    for f in files:
        result = check_file(f)

        if "error" in result:
            print(f"[ERROR] {result['instrument']}: {result['error']}")
            continue

        if result["has_date"]:
            present.append(result)
        else:
            missing.append(result)

    # -----------------------------
    # Summary
    # -----------------------------
    print("\n========== SUMMARY ==========")
    print(f"Total instruments: {len(files)}")
    print(f"Have 2026-01-01: {len(present)}")
    print(f"Missing 2026-01-01: {len(missing)}")

    # -----------------------------
    # Missing list
    # -----------------------------
    print("\n========== MISSING ==========")
    for r in missing:
        print(f"{r['instrument']}: range [{r['min_date']} → {r['max_date']}]")

    # -----------------------------
    # Present list (optional)
    # -----------------------------
    print("\n========== PRESENT ==========")
    for r in present[:10]:
        print(f"{r['instrument']}: range [{r['min_date']} → {r['max_date']}]")

    if len(present) > 10:
        print("...")

    print("\n========= DONE =========")


if __name__ == "__main__":
    main()