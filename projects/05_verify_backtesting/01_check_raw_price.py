"""
1. Check raw data alginment
"""

import pandas as pd
from matplotlib import pyplot as plt

# INPUT
symbol = "CAD10"
# start_date = "2003-01-01"
# end_date = "2022-01-01"


if __name__ == '__main__':

    # Load the data
    csvpath = f"/Users/nanthawat/PycharmProjects/pysystemtrade/data/futures/adjusted_prices_csv/{symbol}.csv"
    parquetpath = f"/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/{symbol}.parquet"
    csvPrice = pd.read_csv(csvpath)
    parquetPrice = pd.read_parquet(parquetpath)

    # Convert datetime and set as index
    csvPrice['DATETIME'] = pd.to_datetime(csvPrice['DATETIME'])
    csvPrice.set_index('DATETIME', inplace=True)
    parquetPrice.index = pd.to_datetime(parquetPrice.index)

    # Rename for consistency
    csvPrice.rename(columns={'price': 'CSV Price'}, inplace=True)
    parquetPrice.rename(columns={'price': 'Parquet Price'}, inplace=True)

    # Filter by date range (Optional)
    # csvPrice = csvPrice.loc[start_date:end_date]
    # parquetPrice = parquetPrice.loc[start_date:end_date]

    # Plot prices
    plt.figure(figsize=(14, 6))
    csvPrice.plot(ax=plt.gca(), label="CSV Price")
    parquetPrice.plot(ax=plt.gca(), label="Parquet Price")
    plt.title(f"{symbol} - CSV vs Parquet Price")
    plt.ylabel("Price")
    plt.xlabel("DateTime")
    plt.legend()
    plt.grid(True)
    plt.show()
