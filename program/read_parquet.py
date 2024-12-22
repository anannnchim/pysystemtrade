import pandas as pd

if __name__ == '__main__':
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    print(a)
    import matplotlib.pyplot as plt
    a.plot()
    plt.show()