from sysbrokers.IB.ib_capital_data import ibCapitalData
from sysdata.data_blob import dataBlob
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':
    # Note: 1. IB in_sync
    # 1. Make connection
    from ib_insync import *

    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=33)

    # 2.2 FUTURES

    # 2. Define the futures contract
    mxp_future = Future(symbol='MET', lastTradeDateOrContractMonth='202502', exchange='CME', currency='USD')

    # 3. Request historical data
    bars = ib.reqHistoricalData(
        mxp_future,
        endDateTime='',
        durationStr='30 D',  # Adjust duration (e.g., '30 D' for 30 days)
        barSizeSetting='1 hour',  # Adjust bar size (e.g., '1 hour', '1 day')
        whatToShow='TRADES',  # Can be 'TRADES', 'BID', 'ASK', etc.
        useRTH=False  # Set to False to include outside regular trading hours
    )
    #
    # 4. Convert to DataFrame and print
    df = util.df(bars)
    print(df)

    # # 3.1 Ge tick data
    # ticker = ib.reqMktData(mxp_future)
    # # 4. Wait for market data to populate
    # ib.sleep(2)  # Give it a couple of seconds to fetch data
    # # 5. Print current data
    # print(f"Last Price: {ticker.last}")
    # print(f"Bid Price: {ticker.bid}")
    # print(f"Ask Price: {ticker.ask}")
    # print(f"Volume: {ticker.volume}")


    """
    UTC format (UTC) time
    228 2024-12-30 15:00:00  0.04833  0.04833  0.04806  0.04815   6295.0  0.048199      1254
    229 2024-12-30 16:00:00  0.04815  0.04816  0.04797  0.04801   7119.0  0.048064      1123
    230 2024-12-30 17:00:00  0.04802  0.04811  0.04785  0.04791   5443.0  0.047980       945
    231 2024-12-30 18:00:00  0.04792  0.04801  0.04784  0.04785   3670.0  0.047927       894
    232 2024-12-30 19:00:00  0.04786  0.04786  0.04781  0.04783    765.0  0.047837       158

    Instrument timezone (CT format) or instrument timezone 
    229 2024-12-30 10:00:00-06:00  0.04815  0.04816  0.04797  0.04801   7119.0  0.048064      1123
    230 2024-12-30 11:00:00-06:00  0.04802  0.04811  0.04785  0.04791   5443.0  0.047980       945
    231 2024-12-30 12:00:00-06:00  0.04792  0.04801  0.04784  0.04785   3670.0  0.047927       894
    232 2024-12-30 13:00:00-06:00  0.04786  0.04786  0.04781  0.04782    841.0  0.047837       171
    """
     # We can set timezone in IB config setting TWS or gateway.