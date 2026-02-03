
#!/usr/bin/env python3
"""
Interactive optimal position checker for pysystemtrade.

Data source:
- data/parquet/optimal_positions/
    - system_01 AUD_micro.parquet
    - system_01 CORN_mini.parquet
    - ...

Features:
- No absolute paths
- Interactive CLI
- Select system + instrument
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
OPTIMAL_POS_DIR = PROJECT_ROOT / "data" / "parquet" / "optimal_positions"


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
def select_system():
    print(
        """
Select system:
1) system_01
b) back
q) exit
"""
    )
    return ask("Choice: ")


# --------------------------------------------------
# Main workflow
# --------------------------------------------------
def main():
    print("\n=== CHECK OPTIMAL POSITION TOOL ===")

    while True:
        system_choice = select_system()

        if system_choice in ("q", None):
            print("✅ Exit.")
            return

        if system_choice == "b":
            continue

        if system_choice == "1":
            system_code = "system_01"
        else:
            print("❌ Invalid choice.")
            continue

        # -------------------------------
        # Instrument selection
        # -------------------------------
        while True:
            instrument = ask(
                "\nEnter instrument code (e.g. AUD_micro, CORN_mini) or 'b': "
            )

            if instrument in ("q", None):
                return

            if instrument == "b":
                break

            file_path = OPTIMAL_POS_DIR / f"{system_code} {instrument}.parquet"

            load_and_show(
                file_path=file_path,
                title=f"Optimal Position | {system_code} | {instrument}",
                tail_n=50,
            )


if __name__ == "__main__":
    main()
