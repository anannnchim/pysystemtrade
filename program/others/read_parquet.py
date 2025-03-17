import pandas as pd
import matplotlib.pyplot as plt

from sysdata.data_blob import dataBlob
from sysproduction.data.capital import dataCapital

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

if __name__ == '__main__':

    # Note - Print data

    # # Global capital
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet"
    # a = pd.read_parquet(path)
    # print(a)
    #
    # # System capital
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/system_01.parquet"
    # a = pd.read_parquet(path)
    # print(a)

    # Optimal position
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 EUR_micro.parquet"
    a = pd.read_parquet(path)
    print(a)




    # # # Note - Delete some row
    # file_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 EUR_micro.parquet"
    # df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    # df = df.drop(df.index[-1]) # Delete second last row
    # df.to_parquet(file_path, index=True, engine="pyarrow")
    # print(df)


    """
    CORN_mini
                                lower_position  upper_position  reference_price reference_contract
    2025-03-17 10:57:26.314853       -0.123642         0.01819            467.5           20250700
    
    EUR_micro
    2025-03-13 11:56:02.973765        1.553525        1.851572           1.0942           20250600
    2025-03-14 11:56:40.512994        1.383174        1.681186           1.0909           20250600
    2025-03-17 10:57:26.362744        0.516076        0.635585           1.0936           20250600
    
    MUMMY
                            lower_position  upper_position  reference_price reference_contract
    2025-03-17 10:57:26.384612       -0.117616       -0.004179            659.0           20250600

    
    VIX_mini
                            lower_position  upper_position  reference_price reference_contract
2025-03-17 10:57:26.402730       -0.327128       -0.164958             20.4           20250600

"""

    # data_capital = dataCapital(dataBlob())
