import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

# === CONFIG ===
BASE_DIR = Path("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spreads")
PARQUET_ENGINE = "pyarrow"


def load_and_plot(instrument_code: str):
    """
    Load parquet file for the given instrument code and plot it.
    """
    file_path = BASE_DIR / f"{instrument_code}.parquet"

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    df = pd.read_parquet(file_path, engine=PARQUET_ENGINE)

    print("\n===== DATA =====")
    print(df)

    print("\n===== PLOT =====")
    df.plot(title=instrument_code)
    plt.show()


def main():
    while True:
        instrument = input(
            "\nEnter instrument code (e.g. GOLD_micro) or press Enter to exit: "
        ).strip()

        if instrument == "":
            print("✅ Exiting program.")
            break

        load_and_plot(instrument)


if __name__ == "__main__":
    main()
