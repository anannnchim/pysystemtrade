#!/usr/bin/env python3
"""
Safely delete the SECOND LAST row of a parquet file with manual confirmation.

Process:
1. Load current parquet
2. Show the target row to be deleted
3. Show tail of modified dataframe
4. Ask user to confirm replacement
"""

import sys
import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.expand_frame_repr", False)


def delete_second_last_row(parquet_path: str) -> None:
    parquet_path = Path(parquet_path)

    if not parquet_path.exists():
        print(f"❌ File not found: {parquet_path}")
        sys.exit(1)

    print("\n=== LOAD CURRENT PARQUET ===")
    df = pd.read_parquet(parquet_path, engine="pyarrow")

    if len(df) < 2:
        print("❌ DataFrame has fewer than 2 rows. Cannot delete second last row.")
        sys.exit(1)

    print(f"Total rows BEFORE : {len(df)}")

    # --------------------------------------------------
    # Identify row to delete
    # --------------------------------------------------
    target_index = df.index[-2]
    target_row = df.loc[[target_index]]

    print("\n=== ROW TO BE DELETED (SECOND LAST ROW) ===")
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

    # --------------------------------------------------
    # EDIT FILE PATH HERE
    # --------------------------------------------------
    FILE_PATH = (
        "/Users/nanthawat/PycharmProjects/pysystemtrade/"
        "data/parquet/capital/__global_capital.parquet"
    )

    delete_second_last_row(FILE_PATH)
