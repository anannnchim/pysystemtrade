#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

pd.set_option("display.max_columns", None)
plt.rcParams["figure.figsize"] = (12, 6)

# ===== Config & systems =====
CONFIG_PATH = "/projects/config/single_config.yaml"
config = Config(CONFIG_PATH)

s_csv = futures_system(config=config, data=csvFuturesSimData())
s_db  = futures_system(config=config,  data=dbFuturesSimData())

# ===== Helper to fetch a price series =====
def get_price_series(sys_obj, instrument: str) -> pd.Series:
    """
    Try common accessors for a daily price series in pysystemtrade stacks.
    Returns a clean pandas.Series (indexed by date).
    """
    candidates = [
        lambda: sys_obj.rawdata.daily_prices(instrument),
        lambda: sys_obj.rawdata.get_daily_prices(instrument),
        lambda: sys_obj.rawdata.get_instrument_price_series(instrument),
        lambda: sys_obj.rawdata.get_prices_for_instrument(instrument),
    ]
    for getter in candidates:
        try:
            ser = getter()
            if isinstance(ser, pd.Series) and not ser.empty:
                return ser.dropna()
        except Exception:
            continue
    raise AttributeError(f"Could not fetch daily price series for '{instrument}'.")


"""
1. We must check start, end date: put the aligned period to config
2. Check Performance for each one. 
3. Check Cost for each one. 
"""
if __name__ == '__main__':
    # 1) Print DF and plot price from different sources, also print (start/end date for both)
    instr = input("Instrument code to compare (e.g., 'EUR_micro'): ").strip()

    # Fetch price series
    price_csv = get_price_series(s_csv, instr).rename("csv_price")
    price_db  = get_price_series(s_db,  instr).rename("db_price")

    # Print coverage for each source
    print("\n=== Source coverage ===")
    print(f"CSV: start={price_csv.index.min()}  end={price_csv.index.max()}  count={len(price_csv)}")
    print(f"DB : start={price_db.index.min()}  end={price_db.index.max()}  count={len(price_db)}")

    # Align on common dates for fair comparison
    df = pd.concat([price_csv, price_db], axis=1, join="inner").sort_index()
    print("\n=== Aligned (common dates) ===")
    print(f"Common window: {df.index.min()} -> {df.index.max()}  (n={len(df)})")

    # Print the DataFrame (head/tail to avoid huge dumps)
    print("\nHead:")
    print(df.head(10))
    print("\nTail:")
    print(df.tail(10))

    # Plot both prices on the same chart
    ax = df[["csv_price", "db_price"]].plot(title=f"{instr} — CSV vs DB price")
    ax.set_xlabel("Date"); ax.set_ylabel("Price"); ax.grid(True)
    plt.tight_layout(); plt.show()

    # Optional: export the aligned DF
    save = input("\nExport aligned price DF to CSV? [y/N]: ").strip().lower()
    if save in ("y", "yes"):
        out_path = f"./{instr}_csv_vs_db_aligned_prices.csv"
        df.to_csv(out_path, index=True)
        print(f"Saved -> {out_path}")
