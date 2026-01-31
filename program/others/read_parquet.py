import pandas as pd
import matplotlib.pyplot as plt

from sysdata.data_blob import dataBlob
from sysproduction.data.capital import dataCapital
from sysproduction.data.positions import diagPositions

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

if __name__ == '__main__':


    # # # # # Note - Delete some row
    # file_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet"
    # df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    # df = df.iloc[:-1] # Delete the last two rows
    # df.to_parquet(file_path, index=True, engine="pyarrow")
    # print(df)

    # Note - Delate second last row in capital

    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@PLAT#20261000.parquet"
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_adjusted_prices/PLAT.parquet"
    # file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_multiple_prices/PLAT.parquet"
    # file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_contract_prices/Dayay@EUR_micro#20260300.parquet"

    df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    print(df)
    df.plot()
    plt.show()