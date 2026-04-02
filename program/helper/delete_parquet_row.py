#!/usr/bin/env python3
"""
Safely delete the LAST or SECOND LAST row of a parquet file with manual confirmation.

Process:
1. Load current parquet
2. Ask user which row to delete (last / second_last)
3. Show the target row
4. Show tail of modified dataframe
5. Ask user to confirm replacement
"""

import sys
import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.expand_frame_repr", False)


# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]


def delete_row(parquet_path: Path) -> None:

    if not parquet_path.exists():
        print(f"❌ File not found: {parquet_path}")
        sys.exit(1)

    print("\n=== LOAD CURRENT PARQUET ===")
    df = pd.read_parquet(parquet_path, engine="pyarrow")

    if len(df) < 1:
        print("❌ DataFrame is empty.")
        sys.exit(1)

    print(f"Total rows BEFORE : {len(df)}")

    # --------------------------------------------------
    # Ask user which row to delete
    # --------------------------------------------------
    print("\nSelect row to delete:")
    print("1 → LAST row")
    print("2 → SECOND LAST row")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        target_index = df.index[-1]
        label = "LAST ROW"
    elif choice == "2":
        if len(df) < 2:
            print("❌ Not enough rows for second last deletion.")
            sys.exit(1)
        target_index = df.index[-2]
        label = "SECOND LAST ROW"
    else:
        print("❌ Invalid choice.")
        sys.exit(1)

    # --------------------------------------------------
    # Show row to delete
    # --------------------------------------------------
    target_row = df.loc[[target_index]]

    print(f"\n=== ROW TO BE DELETED ({label}) ===")
    print(target_row)

    # --------------------------------------------------
    # Create modified dataframe
    # --------------------------------------------------
    df_modified = df.drop(index=target_index)

    print("\n=== MODIFIED DATA (TAIL) ===")
    print(df_modified.tail(5))
    print(f"\nTotal rows AFTER  : {len(df_modified)}")

    # --------------------------------------------------
    # Confirm replacement
    # --------------------------------------------------
    confirm = input(
        "\n⚠️  Confirm replace original file? Type 'YES' to proceed: "
    ).strip()

    if confirm != "YES":
        print("❌ Operation cancelled. Original file NOT changed.")
        return

    # --------------------------------------------------
    # Write back safely
    # --------------------------------------------------
    df_modified.to_parquet(parquet_path, engine="pyarrow", index=True)

    print("\n✅ File replaced successfully.")
    print(f"Updated file: {parquet_path}")


if __name__ == "__main__":

    FILE_PATH = (
        ROOT_DIR
        / "data"
        / "parquet"
        / "capital"
        / "system_01.parquet"
        # / "__global_capital.parquet"
    )

    delete_row(FILE_PATH)