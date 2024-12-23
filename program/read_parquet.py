import pandas as pd

from sysinit.futures.barchart_futures_contract_prices import strip_file_names

if __name__ == '__main__':
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    print(a)
    import matplotlib.pyplot as plt
    a.plot()
    plt.show()