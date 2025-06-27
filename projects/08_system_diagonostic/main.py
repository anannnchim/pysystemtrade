import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# INPUT: Select data and system
data = csvFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_new_config.yaml")

s = futures_system(config=config, data=data)

if __name__ == '__main__':
    plt.figure(figsize=(12, 6))  # Optional: Set the chart size

    for instr in s.get_instrument_list():
        curve = s.accounts.pandl_for_instrument(instr).percent.curve()
        plt.plot(curve, label=instr)

    plt.title("P&L Percentage Curve by Instrument")
    plt.xlabel("Date")
    plt.ylabel("P&L %")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

