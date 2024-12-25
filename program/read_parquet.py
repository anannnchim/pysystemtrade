import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines
    pd.set_option('display.max_rows', 100)  # Adjust for rows if needed (20 is just an example)

    # Note - FX (daily)
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    print(a)

    # Note - Adjusted price (hourly)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN.parquet")
    # print(a)

    # Note - Contract price
    # (Day)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN_mini#20250300.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN#20250300.parquet")
    # print(a)


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
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN_mini.parquet")
    # print(a)

    # 4. Adjusted price
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    # print(a)

    # PLOT
    # a.plot()
    # plt.show()