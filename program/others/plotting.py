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
# data = csvFuturesSimData()

# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/system_01/config.yaml"
# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_new_config.yaml"
# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_config.yaml"
# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_new_config.yaml"
CONFIG_PATH = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/diversified_program_config.yaml")

config = Config(CONFIG_PATH)
s = futures_system(config=config, data=data)
start_date = "2025-01-01"

if __name__ == '__main__':



    # for instrument in s.get_instrument_list():
    #     a = s.accounts.get_buffered_position(instrument).tail(5)
    #     print(a)

    # print(s.config.get_element("capital_multiplier"))
    # s.config.capital_multiplier = {
    #     "func": "syscore.capital.fixed_capital"
    # }
    # print(s.config.get_element("capital_multiplier"))
    # # Output: {'func': 'syscore.capital.fixed_capital'}

    # s.config.start_date = "2023-06-01"
    # print(s.config.get_element("start_date"))

    # input("This is stats in percentage.")
    # print(s.accounts.portfolio().percent.stats())
    #
    # input("This is Annual data table")
    # df = pd.DataFrame({
    #     "Gross": s.accounts.portfolio().gross.annual.percent,
    #     "Costs": s.accounts.portfolio().costs.annual.percent,
    #     "Net": s.accounts.portfolio().net.annual.percent
    # }); print(df)
    #
    # df.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/csv/return.csv")

    # input("This is annual average return and costs")
    # print(df['Gross'].mean())
    # print(df['Costs'].mean())
    # print(df['Net'].mean())


    # df = pd.read_csv()

    # # Note - Check adjusted price
    # for instru in s.get_instrument_list():
    #     prices = data.daily_prices(instru)
    #     # prices = prices.loc[start_date:]
    #     plt.figure(figsize=(12, 6))
    #     prices.plot(title=f"Daily Prices for {instru}")
    #     plt.xlabel("Date")
    #     plt.ylabel("Price")
    #     plt.grid(True)
    #     plt.legend([instru])
    #     plt.tight_layout()
    #     plt.show()
    #
    # # Note - Performance of portfolio
    #
    prices = s.accounts.portfolio().percent.curve()
    prices = prices.loc[start_date:]
    plt.figure(figsize=(12, 6))
    prices.plot(title=f"Portfolio TWR")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend(["%Return"])
    plt.tight_layout()
    plt.show()
    #
    #
    # Note - Check individual performance
    # for instru in s.get_instrument_list():
    #     prices = s.accounts.portfolio()[instru].percent.curve()
    #     # prices = prices.loc[start_date:]
    #     plt.figure(figsize=(12, 6))
    #     prices.plot(title=f"Daily Prices for {instru}")
    #     plt.xlabel("Date")
    #     plt.ylabel("Price")
    #     plt.grid(True)
    #     plt.legend([instru])
    #     plt.tight_layout()
    #     plt.show()

