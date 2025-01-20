
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', 2)  # Show all rows
pd.set_option('display.expand_frame_repr', None)  # Prevent wrapping to new lines

if __name__ == '__main__':

    import pandas as pd
    import pickle

    print("A. Global Capital--------------------------------")
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/__global_capital.parquet")
    print(a)

    print("B. system_01 ---------------------------------------")
    b = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/system_01.parquet")
    print(b)

    print("C. Optimal position --------------------------------")
    c = pd.read_parquet("/data/parquet/optimal_positions/system_01 ETHER-micro.parquet")
    print(c)

    # Save as df in program/verify_system_f1_csv
    df = pd.concat([a, b, c],axis=False)
    df.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/verify_system_f1_csv/df.csv")

    print("D. Backtesting data ------------------------------")
    file_path = '/private/backtests/system_01/20250120_115349_backtest.pck'
    with open(file_path, 'rb') as file:
        backtest_data = pickle.load(file)
    for i, key in enumerate(backtest_data.keys()):
        print(f"{i}: {key}")

    # Select number
    numbers = [3, 5, 10,11, 14, 15, 66, 81, 83 ]

    for i in numbers:
        specific_key = list(backtest_data.keys())[i]
        specific_value = backtest_data[specific_key]
        print(f" -------------- Key: {specific_key} --------------------------")
        print(f"Value: {specific_value}")

