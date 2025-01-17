import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Adjust pandas options to display all rows and columns
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

    # Note - FX (daily)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    # print(a)
    """
    2025-01-02 23:00:00  0.621690 , 0.6203
    2025-01-03 23:00:00  0.620800, 0.6212
    2025-01-06 23:00:00  0.622820 , 0.6243 
    2025-01-07 23:00:00  0.626445,  0.6265
    """

    # Note - Adjusted price (hourly)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN.parquet")
    # print(a)

    # Note - Contract price
    # (Day)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN_mini#20250300.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/futures_contract_prices/CORN_mini#20250300.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
    # print(a)


    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/MXP#20250300.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/futures_contract_prices/Hour@MXP#20250300.parquet")
    # print(a)
    """
    2024-12-23 23:00:00  0.04898  0.04904  0.04861  0.04879  20881.0
    2024-12-24 23:00:00  0.04886  0.04895  0.04877  0.04885   8997.0
    
    
    Possible solution
    
    0. Fix bc-utils
    1. Check IB connection: by get_fx_from_ib and doc IB.md https://github.com/robcarver17/pysystemtrade/blob/develop/docs/IB.md
    2. Fix sampling config set to Hour (delete data from csv, convert to parquet, update historical prices. 
    3. Fix timezone in pysystem or IB gateway.
    
    """

    # (CORN_min) -hour
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN_mini#20250300.parquet")
    # print(a)

    # (Hour)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
    # print(a)

    # Note - Multiple price (hourly data)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN_mini.parquet")
    # print(a)

    # Daily
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN#20251200.parquet")
    # print(a)

    # Note - Flow

    # 1. Contract price
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN_mini#20250300.parquet")
    # print(a)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN_mini#20250300.parquet")
    # print(a)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250500.parquet")
    # print(a)

    # 2. Roll calendars csv
    # a = pd.read_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/roll_calendars/CORN_mini.csv")
    # print(a)

    # 3. multiple price parquet
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/futures_multiple_prices/CORN_mini.parquet")
    # print(a)

    # 4. Adjusted price
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN#20251200.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN#20251200.parquet")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN#20251200.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN.parquet")
    print(a)
    """
    1571.0 + 2077.0 + 1555.0 +  1157.0 +1704.0 +1956.0
    Corn 2025/12 MIXED 
    2025-01-10 18:00:00  449.25  449.50  447.25  448.50   5856.0
    2025-01-10 19:00:00  448.50  450.50  448.25  449.50   4002.0
    2025-01-10 23:00:00  445.75  452.75  445.75  449.50  39574.0
    """

    """
    CORN 2025/12 DAY
    2025-01-08 06:00:00  446.25  447.50  443.50  445.00  21178.0
    2025-01-09 06:00:00  444.00  447.25  443.50  447.00  21042.0
    2025-01-10 06:00:00  446.00  452.75  445.75  450.25  80527.0
    2025-01-10 23:00:00  445.75  452.75  445.75  449.50  39574.0
    """
    """
    HOUR
    2025-01-10 17:00:00  447.00  452.75  447.00  449.25   21636
    2025-01-10 18:00:00  449.25  449.50  447.25  448.50    5856
    2025-01-10 19:00:00  448.50  450.50  448.25  449.50    4002
    """
    """
    Multiple price 
                      CARRY CARRY_CONTRACT  ...  FORWARD FORWARD_CONTRACT
index                                       ...                          
2022-11-28 02:00:00  617.50       20230900  ...      NaN         20241200
2022-11-28 03:00:00     NaN       20230900  ...      NaN         20241200
2022-11-28 04:00:00  617.50       20230900  ...      NaN         20241200
2022-11-28 05:00:00  618.00       20230900  ...      NaN         20241200
2022-11-28 06:00:00  621.50       20230900  ...      NaN         20241200
...                     ...            ...  ...      ...              ...
2025-01-13 16:00:00  453.50       20250900  ...    456.5         20261200
2025-01-13 17:00:00  454.75       20250900  ...    457.5         20261200
2025-01-13 18:00:00  456.00       20250900  ...    458.0         20261200
2025-01-13 19:00:00  456.00       20250900  ...    458.0         20261200
2025-01-13 23:00:00  456.00       20250900  ...    458.0         20261200

Adjusted price
                      price
index                      
2022-11-28 02:00:00  693.25
2022-11-28 03:00:00  693.25
2022-11-28 04:00:00  692.75
2022-11-28 05:00:00  693.25
2022-11-28 06:00:00  693.50
...                     ...
2025-01-13 16:00:00  455.25
2025-01-13 17:00:00  456.00
2025-01-13 18:00:00  456.75
2025-01-13 19:00:00  456.50
2025-01-13 23:00:00  456.50
    """


    # PLOT
    # a.plot()
    # plt.show()