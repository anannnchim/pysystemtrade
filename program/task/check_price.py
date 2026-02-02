#!/usr/bin/env python3
"""
Interactive price checker for pysystemtrade parquet data.

Features:
- No absolute paths
- Instrument-based selection
- Supports:
    1) futures_contract_prices
    2) futures_adjusted_prices
    3) futures_multiple_prices
- Contract month normalization (YYYYMM -> YYYYMM00)
- Hour data shows tail(200), others tail(20)
- Back / exit supported at every step
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
DATA_DIR = PROJECT_ROOT / "data" / "parquet"


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def ask(prompt: str, allow_empty=False):
    value = input(prompt).strip()
    if value == "" and not allow_empty:
        return None
    return value


def normalize_contract_month(contract_month: str) -> str:
    """
    Ensure contract month follows pysystemtrade format: YYYYMM00
    Accepts:
        - YYYYMM
        - YYYYMM00
    """
    contract_month = contract_month.strip()

    if len(contract_month) == 8 and contract_month.isdigit():
        return contract_month

    if len(contract_month) == 6 and contract_month.isdigit():
        return contract_month + "00"

    raise ValueError(
        f"Invalid contract month format: {contract_month}. "
        "Use YYYYMM or YYYYMM00"
    )


def load_and_show(file_path: Path, title: str, tail_n: int = 20):
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
# Menus
# --------------------------------------------------
def select_price_type():
    print(
        """
Select price type:
1) futures_contract_prices
2) futures_adjusted_prices
3) futures_multiple_prices
b) back
q) exit
"""
    )
    return ask("Choice: ")


def select_contract_frequency():
    print(
        """
Select contract frequency:
1) Hour
2) Day
3) All
b) back
q) exit
"""
    )
    return ask("Choice: ")


# --------------------------------------------------
# Main workflow
# --------------------------------------------------
def main():
    print("\n=== CHECK PRICE TOOL ===")

    while True:
        instrument = ask(
            "\nEnter instrument code (e.g. JGB-SGX-mini) or press Enter to exit: ",
            allow_empty=True,
        )

        if instrument == "":
            print("✅ Exit.")
            return

        while True:
            price_type = select_price_type()

            if price_type in ("q", None):
                return
            if price_type == "b":
                break

            # ===============================
            # Futures contract prices
            # ===============================
            if price_type == "1":
                base_dir = DATA_DIR / "futures_contract_prices"

                raw_contract_month = ask(
                    "\nEnter contract month (e.g. 202603 or 20260300) or 'b': "
                )

                if raw_contract_month in ("b", "q", None):
                    continue

                try:
                    contract_month = normalize_contract_month(raw_contract_month)
                except ValueError as e:
                    print(f"❌ {e}")
                    continue

                while True:
                    freq = select_contract_frequency()

                    if freq == "q":
                        return
                    if freq == "b":
                        break

                    if freq == "1":  # Hour
                        file_path = (
                            base_dir
                            / f"Hour@{instrument}#{contract_month}.parquet"
                        )
                        load_and_show(
                            file_path,
                            f"{instrument} Hour {contract_month}",
                            tail_n=200,
                        )

                    elif freq == "2":  # Day
                        file_path = (
                            base_dir
                            / f"Day@{instrument}#{contract_month}.parquet"
                        )
                        load_and_show(
                            file_path,
                            f"{instrument} Day {contract_month}",
                            tail_n=20,
                        )

                    elif freq == "3":  # All
                        file_path = (
                            base_dir
                            / f"{instrument}#{contract_month}.parquet"
                        )
                        load_and_show(
                            file_path,
                            f"{instrument} All {contract_month}",
                            tail_n=20,
                        )
                    else:
                        print("❌ Invalid choice.")

            # ===============================
            # Adjusted prices
            # ===============================
            elif price_type == "2":
                file_path = (
                    DATA_DIR
                    / "futures_adjusted_prices"
                    / f"{instrument}.parquet"
                )
                load_and_show(
                    file_path,
                    f"{instrument} (Adjusted Price)",
                    tail_n=20,
                )

            # ===============================
            # Multiple prices
            # ===============================
            elif price_type == "3":
                file_path = (
                    DATA_DIR
                    / "futures_multiple_prices"
                    / f"{instrument}.parquet"
                )
                load_and_show(
                    file_path,
                    f"{instrument} (Multiple Price)",
                    tail_n=20,
                )

            else:
                print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
