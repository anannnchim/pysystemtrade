import pandas as pd

from sysbrokers.IB.ib_Fx_prices_data import ibFxPricesData
from sysbrokers.IB.ib_futures_contract_price_data import ibFuturesContractPriceData
from sysdata.data_blob import dataBlob
from sysbrokers.IB.ib_connection import connectionIB

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines


if __name__ == '__main__':

    # conn = connectionIB(client_id=1,
    #                     ib_ipaddress="127.0.0.1",
    #                     ib_port=4002,  # 7496, 4001 for live, 4002 for sim ,7497 for tws sim
    #                     account="DU7559791")  #U12379349, U19256092, DU7559791
    #
    # # Note 1: Get FX price: This one get the daily data [correct]
    # a = ibFxPricesData(conn, dataBlob())
    # print(a.get_fx_prices("AUDUSD"))



    """
    FROM IB
    2024-12-16 23:00:00    0.637070
    2024-12-17 23:00:00    0.633725
    2024-12-18 23:00:00    0.621745
    2024-12-19 23:00:00    0.623790
    2024-12-20 23:00:00    0.625095
    2024-12-23 23:00:00    0.624850
    2024-12-24 23:00:00    0.623695
    2024-12-26 23:00:00    0.622050
    2024-12-27 23:00:00    0.621515
    2024-12-30 23:00:00    0.624155 << Not stable
    
    FROM CURRENT (Correct) GMT +12 
    2024-12-16 23:00:00  0.637070
    2024-12-17 23:00:00  0.633725
    2024-12-18 23:00:00  0.621745
    2024-12-19 23:00:00  0.623790
    2024-12-20 23:00:00  0.625095
    2024-12-23 23:00:00  0.624850
    2024-12-24 23:00:00  0.623695
    2024-12-26 23:00:00  0.622050
    2024-12-27 23:00:00  0.621515
    2024-12-30 23:00:00  0.624145 < not stable 
    
    GMT +0, 
    2024-12-16 23:00:00  0.637070
    2024-12-17 23:00:00  0.633725
    2024-12-18 23:00:00  0.621745
    2024-12-19 23:00:00  0.623790
    2024-12-20 23:00:00  0.625095
    2024-12-23 23:00:00  0.624850
    2024-12-24 23:00:00  0.623695
    2024-12-26 23:00:00  0.622050
    2024-12-27 23:00:00  0.621515
    2024-12-30 23:00:00  0.624145 <<< not stable since it's today.
    
    
    *** Note
    1. Since today is 30, then data is not finalize when we updating, we will get the un-final price for today. 
    
    -> Check if tmr the 30 date data will b updated to the correct one or not. 
    """

    # Note: 2: My current FX data
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet"
    df = pd.read_parquet(path)
    print(df)


    # NOTE Delete 3 row and save
    # df = df[:-10]
    # print(df)
    # df.to_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet", index=True)



    # Note: Will try to update data





    # Note 2: Get contract price (this not working): need to check dataBlob or broker_futures_instrument
    # from sysobjects.contracts import futuresContract
    # from sysbrokers.IB.ib_futures_contract_price_data import ibFuturesContractPriceData
    # from sysdata.data_blob import dataBlob
    # ibfuturesdata = ibFuturesContractPriceData(conn, dataBlob())
    # a= ibfuturesdata.get_list_of_instrument_codes_with_merged_price_data()  # returns list of instruments defined in [futures config file](/sysbrokers/IB/ibConfigFutures.csv)
    # ibfuturesdata.contract_dates_with_price_data_for_instrument_code("EDOLLAR")  # returns list of contract dates
    # ibfuturesdata.get_prices_for_contract_object(
    #     futuresContract("EDOLLAR", "201203"))  # returns OHLC price and volume data
    # print(a)

