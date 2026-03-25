import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = PROJECT_ROOT / "data" / "parquet" / "spreads"

PARQUET_ENGINE = "pyarrow"


def get_spread_column(df: pd.DataFrame):

    if "spread" in df.columns:
        return "spread"

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        return numeric_cols[0]

    raise ValueError("No numeric column found")


# ---------- OUTLIER FILTER ----------
def remove_outliers_iqr(series):

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    filtered = series[(series >= lower) & (series <= upper)]

    return filtered


# ---------- STATS ----------
def show_spread_stats(df, col):

    s = df[col].dropna()

    # remove outliers
    s_filtered = remove_outliers_iqr(s)

    mean_raw = s.mean()
    mean_filtered = s_filtered.mean()
    median = s.median()

    stats = pd.DataFrame({
        "mean_raw": [mean_raw],
        "mean_no_outlier": [mean_filtered],
        "median": [median],
        "min": [s.min()],
        "max": [s.max()],
        "half_spread": [mean_filtered / 2],
        "half_spread_med": [median / 2],
    })

    print("\n===== SPREAD STATS =====")
    print(stats)

# ---------- PLOTS ----------
def plot_spread(df, col, instrument):

    s = df[col].dropna()
    s_filtered = remove_outliers_iqr(s)

    # line
    plt.figure()
    s.plot(title=f"{instrument} spread")
    plt.show()

    # box raw
    plt.figure()
    plt.boxplot(s)
    plt.title(f"{instrument} boxplot raw")
    plt.show()

    # box filtered
    plt.figure()
    plt.boxplot(s_filtered)
    plt.title(f"{instrument} boxplot no outlier")
    plt.show()


def load_and_plot(instrument_code):

    file_path = BASE_DIR / f"{instrument_code}.parquet"

    if not file_path.exists():
        print("file not found")
        return

    df = pd.read_parquet(file_path, engine=PARQUET_ENGINE)

    print("\n===== DATA =====")
    print(df)

    col = get_spread_column(df)

    show_spread_stats(df, col)

    plot_spread(df, col, instrument_code)


def main():

    while True:

        instrument = input(
            "\nEnter instrument code: "
        ).strip()

        if instrument == "":
            break

        load_and_plot(instrument)


if __name__ == "__main__":
    main()