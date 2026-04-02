#!/usr/bin/env python3

"""
Interactive parquet editor (safe version)

Features:
1. Show last 5 rows (all columns)
2. Let user select column
3. Let user select row (from last 5)
4. Modify value
5. Show diff
6. Confirm before overwrite
"""

import sys
import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]


# --------------------------------------------------
# Helper
# --------------------------------------------------
def parse_value(val: str):
    """
    Try to convert input to correct dtype
    """
    if val.lower() == "none":
        return None
    try:
        return int(val)
    except:
        try:
            return float(val)
        except:
            return val


# --------------------------------------------------
# Main logic
# --------------------------------------------------
def modify_parquet(parquet_path: Path):

    if not parquet_path.exists():
        print(f"❌ File not found: {parquet_path}")
        sys.exit(1)

    print("\n=== LOAD PARQUET ===")
    df = pd.read_parquet(parquet_path, engine="pyarrow")

    if df.empty:
        print("❌ DataFrame is empty")
        sys.exit(1)

    print(f"Total rows: {len(df)}")

    # --------------------------------------------------
    # Show last 5 rows
    # --------------------------------------------------
    print("\n=== LAST 5 ROWS ===")
    last_df = df.tail(5).copy()
    print(last_df)

    # --------------------------------------------------
    # Show columns
    # --------------------------------------------------
    print("\n=== COLUMNS ===")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    col_choice = input("\nSelect column index: ").strip()

    if not col_choice.isdigit() or int(col_choice) >= len(df.columns):
        print("❌ Invalid column")
        sys.exit(1)

    col_name = df.columns[int(col_choice)]

    # --------------------------------------------------
    # Select row (within last 5)
    # --------------------------------------------------
    print("\nSelect row from LAST 5 (0 = oldest, 4 = newest)")
    row_choice = input("Enter row index (0-4): ").strip()

    if not row_choice.isdigit():
        print("❌ Invalid row")
        sys.exit(1)

    row_choice = int(row_choice)

    if row_choice < 0 or row_choice >= len(last_df):
        print("❌ Row out of range")
        sys.exit(1)

    # Map to real index
    target_index = last_df.index[row_choice]

    old_value = df.loc[target_index, col_name]

    print("\n=== CURRENT VALUE ===")
    print(f"Index: {target_index}")
    print(f"Column: {col_name}")
    print(f"Old value: {old_value}")

    # --------------------------------------------------
    # Modify value
    # --------------------------------------------------
    new_val_raw = input("\nEnter new value (or press Enter to cancel): ").strip()

    if new_val_raw == "":
        print("❌ No change made")
        return

    new_value = parse_value(new_val_raw)

    # --------------------------------------------------
    # Preview change
    # --------------------------------------------------
    print("\n=== PREVIEW CHANGE ===")
    print(f"{old_value}  --->  {new_value}")

    confirm = input("\nConfirm change? Type 'YES': ").strip()

    if confirm != "YES":
        print("❌ Cancelled")
        return

    # Apply change
    df.loc[target_index, col_name] = new_value

    # --------------------------------------------------
    # Final confirmation
    # --------------------------------------------------
    print("\n=== FINAL CHECK (LAST 5 ROWS) ===")
    print(df.tail(5))

    confirm2 = input("\n⚠️  Overwrite parquet file? Type 'YES': ").strip()

    if confirm2 != "YES":
        print("❌ Not saved")
        return

    # --------------------------------------------------
    # Save
    # --------------------------------------------------
    df.to_parquet(parquet_path, engine="pyarrow", index=True)

    print("\n✅ Saved successfully")
    print(f"Path: {parquet_path}")


# --------------------------------------------------
# Entry
# --------------------------------------------------
if __name__ == "__main__":

    print("\nEnter parquet path (relative to ROOT_DIR or full path):")
    user_input = input("> ").strip()

    # Support both absolute and relative
    path = Path(user_input)

    if not path.is_absolute():
        path = ROOT_DIR / path

    modify_parquet(path)