"""
2. Check if there is any mismatch of price from different data source
- We check price alginment and statistic.
"""
import pandas as pd
from matplotlib import pyplot as plt
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
db = dbFuturesSimData()
csv = csvFuturesSimData()

# INPUT
symbol = "CAD10"
# start_date = "2003-01-01"
# end_date = "2022-01-01"


if __name__ == '__main__':

    parquetPrice = db.daily_prices(symbol)
    csvPrice = csv.daily_prices(symbol)

    # Filter by date range (Optional)
    # csvPrice = csvPrice.loc[start_date:end_date]
    # parquetPrice = parquetPrice.loc[start_date:end_date]

    # # Calculate daily returns
    csvRet = csvPrice.pct_change()
    parquetRet =  parquetPrice.pct_change()

    # Align returns on the same dates
    returns = pd.concat([csvRet, parquetRet], axis=1).dropna()

    # Print standard deviations
    print("Mean of Daily Returns:")
    print(returns.mean()*256)

    print("Standard Deviation of Daily Returns:")
    print(returns.std()*16)

    print("Annual Sharpe Ratio")
    print( (returns.mean()*256)/ (returns.std()*16))

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

    # Plot returns
    plt.figure(figsize=(14, 6))
    returns.plot(ax=plt.gca())
    plt.title(f"{symbol} - Daily Returns Comparison")
    plt.ylabel("Daily Return")
    plt.xlabel("DateTime")
    plt.legend()
    plt.grid(True)
    plt.show()
