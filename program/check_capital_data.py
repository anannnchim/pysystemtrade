import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sysdata.sim.db_futures_sim_data import dbFuturesSimData

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    print("1. Global Capital--------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/__global_capital.parquet")
    a.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/verify_system_f1_csv/a.csv")
    print(a)

    print("2. system_01 --------------------------------")
    b = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/system_01.parquet")
    b.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/verify_system_f1_csv/b.csv")
    print(b)

    print("3. Optimal position --------------------------------")
    c = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 ETHER-micro.parquet")
    print(c)
    c.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/verify_system_f1_csv/c.csv")


    print("4. Contract position --------------------------------")
    # d = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/contract_positions/ETHER-micro#20250200.parquet")
    # d.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/verify_system_f1_csv/d.csv")
    # print(d)

    print("5. Strategy position --------------------------------")
    # e = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/strategy_positions/system_01 ETHER-micro.parquet")
    # e.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/verify_system_f1_csv/e.csv")
    # print(e)


    # print("6. Backtesting data ------------------------------")
    # file_path = '/Users/nanthawat/PycharmProjects/pysystemtrade/private/backtests/system_01/20250120_115349_backtest.pck'
    # with open(file_path, 'rb') as file:
    #     backtest_data = pickle.load(file)
    # print(backtest_data.keys())


