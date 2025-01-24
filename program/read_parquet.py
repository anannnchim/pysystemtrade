import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Adjust pandas options to display all rows and columns
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@ETHER-micro#20250200.parquet")
    print(a)
    a.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/output_csv/price.csv")