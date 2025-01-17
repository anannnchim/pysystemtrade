from sysdata.data_blob import dataBlob
from sysproduction.data.broker import dataBroker

if __name__ == '__main__':
    # broker_data_source = dataBroker(dataBlob())
    # print(broker_data_source.get_list_of_fxcodes())
    # print(broker_data_source.broker_fx_balances())
    # print(broker_data_source.get_all_current_contract_positions())
    # print(broker_data_source.get_list_of_orders())
    ## setup

    ## IB trading hours
    from sysproduction.data.broker import *

    d = dataBroker()
    c = d.broker_futures_contract_data.get_contract_object_with_IB_data(futuresContract("ZC", '202503'))
    print(c)
    # ref: https://github.com/robcarver17/pysystemtrade/discussions/845
