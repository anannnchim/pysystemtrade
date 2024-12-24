import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Note - FX (daily)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    # print(a)

    # Note - Adjusted price (hourly)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    # print(a)

    # Note - Contract price
    # (Day)
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN_mini#20250300.parquet")
    print(a)

    # (CORN_min) -hour
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN_mini#20250300.parquet")
    # print(a)

    # (Hour)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
    # print(a)

    # Note - Multiple price
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN_mini.parquet")
    # print(a)

    # PLOT
    a.plot()
    plt.show()