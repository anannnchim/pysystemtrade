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

    """
    2025-03-24 20:00:00     NaN   1.0851  1.0851       20250300         20250600       20250600
    2025-03-24 23:00:00     NaN   1.0857  1.0857       20250300         20250600       20250600
    
    
    2009-06-12 02:00:00  1.6184
    2009-06-12 03:00:00  1.6194
    2009-06-12 04:00:00  1.6151
    2009-06-12 05:00:00  1.6084
    2009-06-12 06:00:00  1.6185
    ...                     ...
    2025-03-24 17:00:00  1.0881
    2025-03-24 18:00:00  1.0881
    2025-03-24 19:00:00  1.0881
    2025-03-24 20:00:00  1.0881
    2025-03-24 23:00:00  1.0881
    
    [92458 rows x 1 columns]
    """

    # Multiple price
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/COPPER-micro#20250900.parquet"
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/VIX_mini.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/COPPER-micro.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 BBCOMM.parquet"

    a = pd.read_parquet(path)
    print(a)

    '''
    Spread 
    1. Config: 0.064 (Rob change to 0.048)
    2. Parquet min: 0.07 
    3. Live (21.43): AUG,SEP = 0.02,0.04 19.44
    
 
    '''

    # # # # # Note - Delete some row
    # file_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 VIX_mini.parquet"
    # df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    # df = df.iloc[:-2] # Delete the last two rows
    # df.to_parquet(file_path, index=True, engine="pyarrow")
    # print(df)

