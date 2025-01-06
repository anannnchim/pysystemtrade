import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Adjust pandas options to display all rows and columns
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

    # Note - FX (daily)
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    print(a)
    """
    2024-12-24 23:00:00  0.624065
    2024-12-26 23:00:00  0.623665
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
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN.parquet")
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
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    # print(a)

    # PLOT
    # a.plot()
    # plt.show()