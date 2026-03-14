from sysbrokers.IB.ib_futures_contract_price_data import ibFuturesContractPriceData
from sysdata.data_blob import dataBlob
from sysproduction.data.broker import dataBroker
from sysproduction.data.contracts import dataContracts

if __name__ == '__main__':

    data = dataBlob()
    db = dataBroker(data)
    dc = dataContracts(data)

    print("Instrument list:",
          db.broker_futures_contract_price_data.get_list_of_instrument_codes_with_merged_price_data())

    instrument = "EURIBOR"
    print("Priced contract id:", dc.get_priced_contract_id(instrument))
    #
    from sysdata.data_blob import dataBlob
    from sysproduction.data.broker import dataBroker

    data = dataBlob()
    db = dataBroker(data)

    lst = db.broker_futures_contract_price_data.get_list_of_instrument_codes_with_merged_price_data()

    print("EURIBOR in list?", "EURIBOR" in lst)
    print("Total instruments:", len(lst))

    a = ibFuturesContractPriceData(data)
