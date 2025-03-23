import pandas as pd
import matplotlib.pyplot as plt

from sysdata.data_blob import dataBlob
from sysproduction.data.capital import dataCapital

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

if __name__ == '__main__':

    # Note - Print data

    # Global capital
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet"
    # a = pd.read_parquet(path)
    # print(a)
    #
    # # System capital
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/system_01.parquet"
    # a = pd.read_parquet(path)
    # print(a)

    # Optimal position
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spreads/VIX_mini.parquet"
    # a = pd.read_parquet(path)
    # print(a)

    # Contract price
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 VIX_mini.parquet"
    a = pd.read_parquet(path)
    print(a)

    # Multiple price
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/VIX_mini.parquet"
    # a = pd.read_parquet(path)
    # print(a)

    # # # Note - Delete some row
    # file_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 EUR_micro.parquet"
    # df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    # df = df.drop(df.index[-1]) # Delete second last row
    # df.to_parquet(file_path, index=True, engine="pyarrow")
    # print(df)

