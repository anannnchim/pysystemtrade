import pandas as pd
import matplotlib.pyplot as plt

from sysdata.data_blob import dataBlob
from sysproduction.data.capital import dataCapital
from sysproduction.data.positions import diagPositions

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
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
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 VIX_mini.parquet"
    # a = pd.read_parquet(path)
    # print(a)

    # Contract price
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/system_01.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 MUMMY.parquet"
    # a = pd.read_parquet(path)
    # print(a)


    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/SILVER.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/SOYMEAL.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/strategy_positions/system_01 JGB-SGX-mini.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/contract_positions/JGB-SGX-mini#20251200.parquet"
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/#20260300.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/contract_positions/JGB-SGX-mini#20260300.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@SILVER#20260300.parquet"
    a = pd.read_parquet(path).tail(20)
    print(a)
    # a.plot()
    # plt.show()

    '''
    Spread 
    1. Config: 0.064 (Rob change to 0.048)
    2. Parquet min: 0.07 
    3. Live (21.43): AUG,SEP = 0.02,0.04 19.44
    
 
    '''
    # /Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 MUMMY.parquet
    # # # # # Note - Delete some row
    # file_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 VIX_mini.parquet"
    # df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    # df = df.iloc[:-1] # Delete the last two rows
    # df.to_parquet(file_path, index=True, engine="pyarrow")
    # print(df)

