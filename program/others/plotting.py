import os
from datetime import datetime
import pandas as pd
from ib_insync import IB
from program.googlesheet.update_system_gg import update_market_monitoring, update_portfolio_monitoring, \
    update_accounting_ib, update_system_verification, update_system_diagnostic
from program.helper.run_scripts import run_scripts
from sysdata.config.configdata import Config
from sysdata.config.production_config import get_production_config
from sysdata.parquet.parquet_access import ParquetAccess
from sysdata.parquet.parquet_capital import parquetCapitalData
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData

data = dbFuturesSimData()
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/system_01/config.yaml"
config = Config(CONFIG_PATH)
s = futures_system(config=config, data=data)

if __name__ == '__main__':

    for instru in s.get_instrument_list():
        prices = data.daily_prices(instru)
        plt.figure(figsize=(12, 6))
        prices.plot(title=f"Daily Prices for {instru}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend([instru])
        plt.tight_layout()
        plt.show()