import pandas as pd
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

if __name__ == '__main__':

    # Contract price
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@JGB-SGX-mini#20260300.parquet"
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@JGB-SGX-mini#20260300.parquet"
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_contract_prices/JGB-SGX-mini#20260300.parquet"

    # adjusted_price
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_adjusted_prices/JGB-SGX-mini.parquet"

    # multiple_price
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/futures_multiple_prices/JGB-SGX-mini.parquet"
    file_path = "/home/anan/AnanProjects/pysystemtrade/data/parquet/contract_positions/IRON#20260500.parquet"

    df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    print(df)
    # df.plot()
    # plt.show()