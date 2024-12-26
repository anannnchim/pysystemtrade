from sysbrokers.IB.ib_capital_data import ibCapitalData
from sysdata.data_blob import dataBlob
from sysdata.sim.db_futures_sim_data import dbFuturesSimData

if __name__ == '__main__':

    # 1. Connection
    from sysbrokers.IB.ib_connection import connectionIB
    conn = connectionIB(client_id=1,
                        ib_ipaddress="127.0.0.1",
                        ib_port=4002, # 7496, 4001 for live, 4002 for sim ,7497 for tws sim
                        account="DU7559791")  #U12379349, U19256092, DU7559791
    print(conn)

    # # 2. Data
    data = dbFuturesSimData()
    capital_data = ibCapitalData(conn, dataBlob())
    cap = capital_data.get_account_value_across_currency()
    print(cap)
