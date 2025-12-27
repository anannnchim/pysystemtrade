import os
from datetime import datetime
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt

from sysdata.sim.db_futures_sim_data import dbFuturesSimData
# from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.dates as mdates  # (kept in case you use it later)

# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/private_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/system_f1_config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/config.yaml")
s = futures_system(config=config, data=data)

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

"""
1. Check IDM overtime
2. Correlation matrix -> CSV
"""
if __name__ == '__main__':

    # 1) IDM overtime
    a = s.portfolio.get_instrument_diversification_multiplier()  # Estimated IDM
    print(a)
    a.plot()
    plt.show()
    print(a.mean())

    # 2) Correlation
    corr_obj = s.portfolio.get_instrument_correlation_matrix().corr_list[-1]
    print(corr_obj)

    # Convert to numpy array (you said you have a way; .values usually works)
    # Fallbacks included to be safe across versions
    if hasattr(corr_obj, "values"):
        corr_arr = corr_obj.values
    elif hasattr(corr_obj, "corr"):
        corr_arr = corr_obj.corr
    else:
        corr_arr = corr_obj  # assume it's already array-like

    labels = s.get_instrument_list()
    corr_df = pd.DataFrame(corr_arr, index=labels, columns=labels)

    # Save to CSV
    out_dir = "/Users/nanthawat/PycharmProjects/pysystemtrade/output"
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_path = os.path.join(out_dir, f"correlation_matrix_{ts}.csv")
    corr_df.to_csv(out_path, float_format="%.6f")

    print("\n=== Correlation matrix (latest) ===")
    print(corr_df)
    print(f"\n✅ Saved CSV: {out_path}")
