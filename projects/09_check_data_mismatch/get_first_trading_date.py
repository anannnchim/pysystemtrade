#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sysdata.sim.db_futures_sim_data import dbFuturesSimData

if __name__ == '__main__':
    data = dbFuturesSimData()
    instruments = data.get_instrument_list()
    print(instruments)

    start_dates = {}

    for instr in instruments:
        try:
            px = data.get_backadjusted_futures_price(instr)

            # Handle DataFrame vs Series and clean it up
            if isinstance(px, pd.DataFrame):
                # take the first column if a DataFrame is returned
                if px.shape[1] == 0:
                    start_dates[instr] = None
                    continue
                px = px.iloc[:, 0]

            px = px.dropna().sort_index()

            # Start date = first valid index (if any)
            start_dates[instr] = px.index[0] if len(px) else None

        except Exception as e:
            start_dates[instr] = None
            print(f"[{instr}] error: {e}")

    # Pretty print as a Series sorted by date
    s = pd.Series(start_dates, name="start_date").sort_values(kind="mergesort")
    print(s)
