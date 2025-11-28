from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yaml

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

# ===== Defaults (edit for click-to-run) =====
DEFAULT_CONFIG = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/12_check_asset_performance/asset_class.yaml"
DEFAULT_ASSET_MAP = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/12_check_asset_performance/asset_class_map.yaml"
DEFAULT_DATA = "db"          # "csv" or "db"

# INPUT: Select data and system
# data = csvFuturesSimData()
data = dbFuturesSimData()
s = futures_system(config=Config(DEFAULT_CONFIG), data=data)

if __name__ == '__main__':

    # --- Get instrument list ---
    instrument_list = data.get_instrument_list()

    # --- Input: start date string ---
    start_date_str = input(
        "Enter start date (YYYY-MM-DD) for performance calculation "
        "(press Enter to use full history): "
    ).strip()

    if start_date_str:
        start_date = pd.to_datetime(start_date_str)
    else:
        start_date = None
        start_date_str = "START"  # label for plots

    # --- Load asset class map ---
    with open(DEFAULT_ASSET_MAP, "r") as f:
        asset_map = yaml.safe_load(f)

    # --- Build instrument -> asset class / subclass mapping ---
    instrument_asset_class = {}
    instrument_subclass = {}

    for asset_class, value in asset_map.items():
        if isinstance(value, dict):
            # value is {subclass: [inst, ...], ...}
            for subclass, inst_list in value.items():
                if not inst_list:
                    continue
                for inst in inst_list:
                    instrument_asset_class[inst] = asset_class
                    instrument_subclass[inst] = f"{asset_class}:{subclass}"
        else:
            # value is [inst, ...]
            inst_list = value or []
            for inst in inst_list:
                instrument_asset_class[inst] = asset_class
                # subclass may not exist here; leave blank

    # --- Calculate time-weighted return per instrument since start date ---
    instrument_return = {}

    for instrument in instrument_list:

        # Get daily price
        px = data.daily_prices(instrument_code=instrument)
        if px is None or len(px) == 0:
            continue

        # Ensure pandas Series
        if isinstance(px, pd.DataFrame):
            px = px.iloc[:, 0]

        px = pd.Series(px).dropna()
        if px.empty:
            continue

        # Filter start date
        if start_date is not None:
            px = px[px.index >= start_date]
        if len(px) < 2:
            # Not enough data since start date
            continue

        # Time-weighted return from price since start date:
        # TWR = price_end / price_start - 1
        twr = px.iloc[-1] / px.iloc[0] - 1.0

        instrument_return[instrument] = twr

    # --- Build instrument-level summary table ---
    if instrument_return:
        inst_rows = []
        for inst, twr in instrument_return.items():
            inst_rows.append({
                "Instrument": inst,
                "AssetClass": instrument_asset_class.get(inst, ""),
                "SubClass": instrument_subclass.get(inst, ""),
                "TWR": twr,
            })

        inst_df = pd.DataFrame(inst_rows)
        inst_df = inst_df.sort_values("TWR", ascending=False)

        inst_df_pretty = inst_df.copy()
        inst_df_pretty["TWR"] = inst_df_pretty["TWR"].map(lambda x: f"{x:.2%}")
        print("\n=== Instrument performance since {} ===".format(start_date_str))
        print(inst_df_pretty.to_string(index=False))
    else:
        print("No instruments with sufficient price data since {}.".format(start_date_str))

    # --- Aggregate to asset class level ---
    asset_class_return = {}

    for asset_class in asset_map.keys():
        # Instruments in this class that we have returns for
        inst_in_class = [
            inst for inst, cls in instrument_asset_class.items()
            if cls == asset_class and inst in instrument_return
        ]
        if not inst_in_class:
            continue

        vals = [instrument_return[inst] for inst in inst_in_class]
        asset_class_return[asset_class] = sum(vals) / len(vals)   # equal-weight

    if asset_class_return:
        ac_series = pd.Series(asset_class_return).sort_values(ascending=False)
        ac_df = ac_series.rename("TWR").reset_index().rename(columns={"index": "AssetClass"})
        ac_df_pretty = ac_df.copy()
        ac_df_pretty["TWR"] = ac_df_pretty["TWR"].map(lambda x: f"{x:.2%}")

        print("\n=== Asset class performance since {} ===".format(start_date_str))
        print(ac_df_pretty.to_string(index=False))
    else:
        print("\nNo asset class aggregates available (no instruments with data).")

    # --- Aggregate to subclass level ---
    subclass_return = {}

    all_subclasses = set(instrument_subclass.values())
    for subclass_label in all_subclasses:
        inst_in_sub = [
            inst for inst, sub in instrument_subclass.items()
            if sub == subclass_label and inst in instrument_return
        ]
        if not inst_in_sub:
            continue

        vals = [instrument_return[inst] for inst in inst_in_sub]
        subclass_return[subclass_label] = sum(vals) / len(vals)   # equal-weight

    if subclass_return:
        sub_series = pd.Series(subclass_return).sort_values(ascending=False)
        sub_df = sub_series.rename("TWR").reset_index().rename(columns={"index": "SubClass"})
        sub_df_pretty = sub_df.copy()
        sub_df_pretty["TWR"] = sub_df_pretty["TWR"].map(lambda x: f"{x:.2%}")

        print("\n=== Sub-asset class performance since {} ===".format(start_date_str))
        print(sub_df_pretty.to_string(index=False))
    else:
        print("\nNo sub-asset class aggregates available.")

    # --- Vertical bar charts ---

    # Asset class bar chart
    if asset_class_return:
        plt.figure(figsize=(10, 5))
        ac_series.mul(100).plot(kind="bar")
        plt.title("Performance by Asset Class since {}".format(start_date_str))
        plt.xlabel("Asset Class")
        plt.ylabel("Return (%)")
        plt.grid(axis="y")
        plt.tight_layout()
        plt.show()

    # Subclass bar chart
    if subclass_return:
        plt.figure(figsize=(12, 6))
        sub_series.mul(100).plot(kind="bar")
        plt.title("Performance by Sub-asset Class since {}".format(start_date_str))
        plt.xlabel("Sub-asset Class")
        plt.ylabel("Return (%)")
        plt.grid(axis="y")
        plt.tight_layout()
        plt.show()
