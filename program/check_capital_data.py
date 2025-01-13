import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sysdata.sim.db_futures_sim_data import dbFuturesSimData

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    # Note - FX (daily)
    print("1. Global Capital--------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/__global_capital.parquet")
    print(a)

    print("2. Strategy_1 --------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/strategy_1.parquet")
    print(a)

    # print("3. Backtesting data ------------------------------")
    # file_path = '/Users/nanthawat/PycharmProjects/pysystemtrade/private/backtests/strategy_1/20250102_110049_backtest.pck'
    # with open(file_path, 'rb') as file:
    #     backtest_data = pickle.load(file)
    # print(backtest_data)

    print("4. Optimal position --------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/optimal_positions/strategy_1 CORN.parquet")
    print(a)

    print("5. Contract position --------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/contract_positions/CORN#20251200.parquet")
    print(a)

    print("5. Strategy position --------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/strategy_positions/strategy_1 CORN.parquet")
    print(a)

