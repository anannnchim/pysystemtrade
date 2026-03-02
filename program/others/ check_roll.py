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

data = csvFuturesSimData()
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
config = Config(CONFIG_PATH)
s = futures_system(config=config, data=data)
start_date = "2021-01-01"

if __name__ == '__main__':
    a = data.get_rolls_per_year("CRUDE_W")
    print(a)
    # sample