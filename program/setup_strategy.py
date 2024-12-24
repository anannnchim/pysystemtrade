import pandas as pd

if __name__ == '__main__':

    # 1. Global capital
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/strategy_1.parquet")
    # print(a)

    b = pd.read_parquet(
        "/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/strategy_1.parquet")
    print(b)
