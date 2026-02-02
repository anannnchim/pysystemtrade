#!/usr/bin/env python3
"""
Interactive capital checker for pysystemtrade.

Data source:
- data/parquet/capital/__global_capital.parquet
- data/parquet/capital/system_01.parquet

Features:
- No absolute paths
- Interactive CLI
- Select global or system capital
- Back / exit supported
- Safe (read-only)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.expand_frame_repr", False)

PARQUET_ENGINE = "pyarrow"

# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CAPITAL_DIR = PROJECT_ROOT / "data" / "parquet" / "capital"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def ask(prompt: str, allow_empty=False):
    value = input(prompt).strip()
    if value == "" and not allow_empty:
        return None
    return value


def load_and_show(file_path: Path, title: str, tail_n: int = 50):
    if not file_path.exists():
        print(f"\n❌ File not found:\n{file_path}")
        return

    df = pd.read_parquet(file_path, engine=PARQUET_ENGINE)

    print(f"\n===== DATA (tail {tail_n}) =====")
    print(df.tail(tail_n))

    print("\n===== PLOT =====")
    df.plot(title=title)
    plt.show()


# --------------------------------------------------
# Menu
# --------------------------------------------------
def select_capital_type():
    print(
        """
Select capital data:
1) Global capital
2) System capital (system_01)
b) back
q) exit
"""
    )
    return ask("Choice: ")


# --------------------------------------------------
# Main workflow
# --------------------------------------------------
def main():
    print("\n=== CHECK CAPITAL TOOL ===")

    while True:
        choice = select_capital_type()

        if choice in ("q", None):
            print("✅ Exit.")
            return

        if choice == "b":
            continue

        if choice == "1":
            file_path = CAPITAL_DIR / "__global_capital.parquet"
            load_and_show(
                file_path=file_path,
                title="Global Capital",
                tail_n=50,
            )

        elif choice == "2":
            file_path = CAPITAL_DIR / "system_01.parquet"
            load_and_show(
                file_path=file_path,
                title="System 01 Capital",
                tail_n=50,
            )

        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
