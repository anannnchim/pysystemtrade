from sysbrokers.IB.ib_capital_data import ibCapitalData
from sysdata.config.production_config import get_production_config
from sysdata.data_blob import dataBlob
from sysdata.sim.db_futures_sim_data import dbFuturesSimData

BROKER_ACCOUNT = get_production_config().get_element('broker_account')
IB_IPADDRESS = get_production_config().get_element('ib_ipaddress')
IB_PORT = get_production_config().get_element('ib_port')


if __name__ == '__main__':

    # 1. Connection
    from sysbrokers.IB.ib_connection import connectionIB
    conn = connectionIB(client_id=11,
                        ib_ipaddress=IB_IPADDRESS,
                        ib_port=IB_PORT,
                        account=BROKER_ACCOUNT)
    print(conn)

    # # 2. Data
    data = dbFuturesSimData()
    capital_data = ibCapitalData(conn, dataBlob())
    cap = capital_data.get_account_value_across_currency()
    print(cap)
