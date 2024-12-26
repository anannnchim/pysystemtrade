from sysbrokers.IB.ib_Fx_prices_data import ibFxPricesData
from sysbrokers.IB.ib_futures_contract_price_data import ibFuturesContractPriceData
from sysdata.data_blob import dataBlob
from sysbrokers.IB.ib_connection import connectionIB


if __name__ == '__main__':

    conn = connectionIB(client_id=1,
                        ib_ipaddress="127.0.0.1",
                        ib_port=4002, # 7496, 4001 for live, 4002 for sim ,7497 for tws sim
                        account="DU7559791")  #U12379349, U19256092, DU7559791

    # Note 1: Get FX price
    # a = ibFxPricesData(conn, dataBlob())
    # print(a.get_fx_prices("AUDUSD"))


    # Note 2: Get contract price (this not working): need to check dataBlob or broker_futures_instrument
    from sysobjects.contracts import futuresContract
    from sysbrokers.IB.ib_futures_contract_price_data import ibFuturesContractPriceData
    from sysdata.data_blob import dataBlob
    ibfuturesdata = ibFuturesContractPriceData(conn, dataBlob())
    a= ibfuturesdata.get_list_of_instrument_codes_with_merged_price_data()  # returns list of instruments defined in [futures config file](/sysbrokers/IB/ibConfigFutures.csv)
    # ibfuturesdata.contract_dates_with_price_data_for_instrument_code("EDOLLAR")  # returns list of contract dates
    # ibfuturesdata.get_prices_for_contract_object(
    #     futuresContract("EDOLLAR", "201203"))  # returns OHLC price and volume data
    print(a)

