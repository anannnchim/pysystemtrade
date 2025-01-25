"""
Reponsible for:
1. Generate order
2.
"""

import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")

data = csvFuturesSimData()

s = futures_system(config=config)

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    s.portfolio.capital_multiplier()  # Ratio between actual account value over initial capital
    s.accounts.get_actual_capital()

    df = pd.DataFrame({
        "S50": s.portfolio.get_actual_position("S50"),
        "USD": s.portfolio.get_actual_position("USD"),
        "GF10": s.portfolio.get_actual_position("GF10")
    })
    print(df)