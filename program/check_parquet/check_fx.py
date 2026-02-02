#!/usr/bin/env python3
"""
Interactive FX spot price checker for pysystemtrade.

Data source:
- data/parquet/spotfx_prices/{FX_PAIR}.parquet

Examples:
- GBPUSD.parquet
- EURUSD.parquet

Features:
- No absolute paths
- Interactive CLI
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
FX_DIR = PROJECT_ROOT / "data" / "parquet" / "spotfx_prices"


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
# Main workflow
# --------------------------------------------------
def main():
    print("\n=== CHECK FX SPOT PRICE TOOL ===")

    while True:
        fx_pair = ask(
            "\nEnter FX pair (e.g. GBPUSD, EURUSD) or press Enter to exit: ",
            allow_empty=True,
        )

        if fx_pair == "":
            print("✅ Exit.")
            return

        fx_pair = fx_pair.upper()

        file_path = FX_DIR / f"{fx_pair}.parquet"

        load_and_show(
            file_path=file_path,
            title=f"{fx_pair} Spot FX Price",
            tail_n=50,
        )


if __name__ == "__main__":
    main()
