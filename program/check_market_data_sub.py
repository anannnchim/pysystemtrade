from sysbrokers.IB.ib_capital_data import ibCapitalData
from sysdata.data_blob import dataBlob
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
import pandas as pd
from ib_insync import *

# Pandas settings for full display
# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.max_rows', None)  # Show all rows
# pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    # 1. Make connection
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=1)

    # 2. Define the futures contracts to check
    futures_contracts = [
        Future(symbol='YC', lastTradeDateOrContractMonth='202503', exchange='CBOT', currency='USD'),
        Future(symbol='V2TX', lastTradeDateOrContractMonth='202503', exchange='EUREX', currency='EUR'),
        Future(symbol='TSEMOTHR', lastTradeDateOrContractMonth='202503', exchange='OSE.JPN', currency='JPY'),
        Future(symbol='CGZ', lastTradeDateOrContractMonth='202503', exchange='CDE', currency='CAD'),
        Future(symbol='AIGCI', lastTradeDateOrContractMonth='202503', exchange='CBOT', currency='USD'),
        Future(symbol='MCL', lastTradeDateOrContractMonth='202504', exchange='NYMEX', currency='USD'),
        Future(symbol='EBM', lastTradeDateOrContractMonth='202503', exchange='MATIF', currency='EUR'),
        Future(symbol='MHG', lastTradeDateOrContractMonth='202503', exchange='COMEX', currency='USD'),

        # False
        Future(symbol='RS', lastTradeDateOrContractMonth='202512', exchange='ICECA', currency='CAD'),

    ]

    for contract in futures_contracts:
        print(f"\nChecking market data for {contract.symbol}...")

        # 3. Request market data
        ticker = ib.reqMktData(contract, '', False, False)
        ib.sleep(2)  # Allow time for data to populate

        # 4. Determine market data availability
        if ticker.last:
            print(f"{contract.symbol} - Real-time price: {ticker.last}")
        elif ticker.close:
            print(f"{contract.symbol} - Delayed price (from closing data): {ticker.close}")
        else:
            print(f"{contract.symbol} - No market data available. You may need a subscription.")

        # 5. Request historical data if we have at least delayed data
        if ticker.last or ticker.close:
            bars = ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='30 D',  # Adjust duration (e.g., '30 D' for 30 days)
                barSizeSetting='1 hour',  # Adjust bar size (e.g., '1 hour', '1 day')
                whatToShow='TRADES',  # Can be 'TRADES', 'BID', 'ASK', etc.
                useRTH=True  # Set to False to include outside regular trading hours
            )

            # Convert to DataFrame and print
            df = util.df(bars)
            print(f"\nHistorical data for {contract.symbol}:")
            print(df)
        else:
            print(f"Skipping historical data request for {contract.symbol} due to missing market data.")

    # Disconnect
    ib.disconnect()


    """
    - Keep checking all the data
    - Enable delay market sub 
    by https://www.ibkrguides.com/traderworkstation/receive-delayed-market-data.htm#:~:text=You%20can%20elect%20to%20receive,the%20prompts%20in%20Global%20Configuration.
    
    """