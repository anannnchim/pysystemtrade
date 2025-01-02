import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    # Note - FX (daily)
    print("1. Global Capital--------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet")
    print(a)

    print("2. Strategy_1 --------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/strategy_1.parquet")
    print(a)

