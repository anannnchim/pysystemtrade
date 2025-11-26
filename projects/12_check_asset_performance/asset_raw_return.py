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

    # --- Build per-instrument time-weighted index from price ---
    instrument_index = {}  # instrument -> index series (starts at 1.0)

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

        # Filter start date (optional)
        # px = px[px.index >= "2010-01-01"]

        # Time-weighted index from price (start at 1.0)
        idx = px / px.iloc[0]
        idx = idx.dropna()
        if idx.empty:
            continue

        instrument_index[instrument] = idx

    # --- Load asset class map ---
    with open(DEFAULT_ASSET_MAP, "r") as f:
        asset_map = yaml.safe_load(f)

    # --- Group based on asset class (top-level) ---
    asset_class_twr = {}  # class -> TWR % series

    for asset_class, value in asset_map.items():

        # value can be list of instruments or dict of subclasses
        if isinstance(value, dict):
            instruments = []
            for sub_list in value.values():
                if sub_list:
                    instruments.extend(sub_list)
        else:
            instruments = value or []

        # Keep only instruments we actually have data for
        instruments = [inst for inst in instruments if inst in instrument_index]
        if not instruments:
            continue

        # Align indices and take equal-weight average (equal initial capital)
        df_idx = pd.DataFrame({inst: instrument_index[inst] for inst in instruments})
        df_idx = df_idx.dropna(how="all")
        if df_idx.empty:
            continue

        class_index = df_idx.mean(axis=1, skipna=True)

        # Convert index (1.0 start) to TWR % curve (0% start)
        class_twr = (class_index - 1.0) * 100.0
        asset_class_twr[asset_class] = class_twr

    # --- Group based on subclass (Class:SubClass) ---
    subclass_twr = {}  # "Class:SubClass" -> TWR % series

    for asset_class, value in asset_map.items():
        if not isinstance(value, dict):
            continue

        for subclass, instruments in value.items():
            instruments = instruments or []
            instruments = [inst for inst in instruments if inst in instrument_index]
            if not instruments:
                continue

            df_idx = pd.DataFrame({inst: instrument_index[inst] for inst in instruments})
            df_idx = df_idx.dropna(how="all")
            if df_idx.empty:
                continue

            sub_index = df_idx.mean(axis=1, skipna=True)

            # Convert index to TWR %
            sub_twr = (sub_index - 1.0) * 100.0
            label = f"{asset_class}:{subclass}"
            subclass_twr[label] = sub_twr

    # --- PLOT ---

    # Plot by asset class
    if asset_class_twr:
        plt.figure(figsize=(10, 5))
        for label, twr in asset_class_twr.items():
            twr.plot(label=label)
        plt.title("RAW PRICE Time-weighted Return by Asset Class (TWR, %)")
        plt.xlabel("Date")
        plt.ylabel("TWR (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Plot by subclass
    if subclass_twr:
        plt.figure(figsize=(10, 5))
        for label, twr in subclass_twr.items():
            twr.plot(label=label)
        plt.title("RAW PRICE Time-weighted Return by Subclass (TWR, %)")
        plt.xlabel("Date")
        plt.ylabel("TWR (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
