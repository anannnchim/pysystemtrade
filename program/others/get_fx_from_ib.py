import pandas as pd

from sysbrokers.IB.ib_Fx_prices_data import ibFxPricesData
from sysbrokers.IB.ib_futures_contract_price_data import ibFuturesContractPriceData
from sysdata.config.production_config import get_production_config
from sysdata.data_blob import dataBlob
from sysbrokers.IB.ib_connection import connectionIB

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

BROKER_ACCOUNT = get_production_config().get_element('broker_account')
IB_IPADDRESS = get_production_config().get_element('ib_ipaddress')
IB_PORT = get_production_config().get_element('ib_port')

if __name__ == '__main__':
    conn = connectionIB(client_id=1,
                        ib_ipaddress=IB_IPADDRESS,
                        ib_port=IB_PORT,
                        account=BROKER_ACCOUNT)

    # Note 1: Get FX price: This one get the daily data [correct]
    a = ibFxPricesData(conn, dataBlob())
    print(a.get_fx_prices("AUDUSD"))
