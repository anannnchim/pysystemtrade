import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# =========================
# CONFIG / DATA SELECTION
# =========================
data = csvFuturesSimData()
# data = dbFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/new_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/single_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/static_three.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/AFTS_four.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v2.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v2.yaml")

s = futures_system(config=config, data=data)

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# =========================
# HELPERS
# =========================
def coerce_to_series(obj, name=None):
    """
    Coerce obj to a pandas Series when possible:
      - If DataFrame: use first column if 1-column; else row-wise mean.
      - If Series: return as-is.
      - If scalar: return None (handled separately).
    Ensures numeric dtype and optional rename.
    """
    if isinstance(obj, pd.DataFrame):
        if obj.shape[1] == 1:
            ser = obj.iloc[:, 0]
        else:
            # Multiple columns: use row-wise mean as a robust default
            ser = obj.mean(axis=1)
    elif isinstance(obj, pd.Series):
        ser = obj
    else:
        return None  # scalar or unsupported type

    ser = pd.to_numeric(ser, errors="coerce")
    if name:
        ser = ser.rename(name)
    return ser

def to_aligned_series(obj, index, name):
    """
    Return a Series aligned to `index`.
      - If scalar -> constant Series over index.
      - If Series/DataFrame -> coerce to Series and reindex.
    """
    ser = coerce_to_series(obj, name=name)
    if ser is not None:
        return ser.reindex(index)
    # Scalar path
    return pd.Series(np.full(len(index), float(obj)), index=index, name=name)

def plot_series(obj, title, ylabel):
    """
    Plot either a Series/DataFrame (coerced to Series if needed),
    or draw a horizontal line for scalar values.
    """
    ser = coerce_to_series(obj)
    plt.figure(figsize=(10, 5))
    if ser is not None:
        ser.plot(linewidth=2)
        plt.xlabel("Date")
    else:
        # Scalar
        plt.axhline(float(obj), linestyle="--", linewidth=2)
        plt.xlabel("")
    plt.title(title, fontsize=14, fontweight="bold")
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

def print_stats(obj, name):
    """
    Pretty-print stats for Series/DataFrame (coerced) or scalar.
    Avoids formatting a pandas Series with a float format spec.
    """
    print(f"\n{name}")
    print("-" * len(name))

    ser = coerce_to_series(obj)
    if ser is not None:
        desc = ser.describe().round(4)
        print(desc)
        mean_val = float(ser.mean())
        print(f"Mean: {mean_val:.4f}")
    else:
        # Scalar
        print(f"Value: {float(obj):.4f}")

def plot_risk_comparison(realised_obj, static_value, abs_sum_obj):
    """
    Combine risks into a single comparison plot.
      realised_obj: Series/DataFrame for realised risk (%)
      static_value: scalar (%) – current annualised risk incl. correlation
      abs_sum_obj: scalar or Series/DataFrame (%) – abs sum risk (no corr/IDM)
    """
    realised = coerce_to_series(realised_obj, name="Realised (2m rolling)")
    if realised is None or realised.empty:
        raise ValueError("Realised risk must be a non-empty time series.")

    idx = realised.index
    static_s = to_aligned_series(static_value, idx, "Static current risk")
    abs_sum_s = to_aligned_series(abs_sum_obj, idx, "Abs sum risk (no corr/IDM)")

    df = pd.concat([realised, static_s, abs_sum_s], axis=1)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(ax=ax, linewidth=2)
    ax.set_title("Portfolio Risk Comparison", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualised Risk (%)")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="best")
    # Optional date formatting (comment out if not needed)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    plt.tight_layout()
    plt.show()

    # Compact summary
    latest = df.tail(1).T.rename(columns=lambda _: "Latest")
    summary = pd.concat(
        [df.mean().round(4).rename("Mean"),
         df.median().round(4).rename("Median")],
        axis=1
    )
    print("\n=== Risk Summary (% annualised) ===")
    print(pd.concat([summary, latest], axis=1).round(4))

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    # 1) Realised risk: 2-month rolling (%)
    realised_obj = s.accounts.portfolio().percent.rolling_ann_std()
    print_stats(realised_obj, "Realised Risk (2m rolling)")
    plot_series(realised_obj, "Realised Risk (2-Month Rolling)", "Annualised Std (%)")

    # 2) Static Current Annualised Risk (%) – include correlation
    static_curr = s.portfolio.get_portfolio_risk_for_original_positions() * 100
    print_stats(static_curr, "Static Current Annualised Risk")
    plot_series(static_curr, "Static Current Annualised Risk", "Risk (%)")

    # 3) Abs sum risk (no correlation and IDM) – could be scalar or series/dataframe
    abs_sum_obj = s.portfolio.get_sum_annualised_risk_for_original_positions() * 100
    print_stats(abs_sum_obj, "Abs Sum Risk (No Correlation, IDM approx)")
    plot_series(abs_sum_obj, "Absolute Sum Risk", "Risk (%)")

    # 4) Single comparison plot
    plot_risk_comparison(realised_obj, static_curr, abs_sum_obj)
