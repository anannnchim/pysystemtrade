from sysdata.data_blob import dataBlob
from sysproduction.data.orders import dataOrders
from sysproduction.data.positions import diagPositions
import datetime

if __name__ == '__main__':
    data = dataBlob()
    # diag_positions = diagPositions(data)
    # diag = diagPositions(data)
    #
    # start_date = datetime.datetime(2025, 7, 1)
    # end_date = datetime.datetime(2025, 7, 19)
    # print(diag.get_list_of_contracts_with_any_contract_position_for_instrument_in_date_range(
    #     "CAD10", start_date, end_date))


    data_orders = dataOrders(data)
    from sysobjects.contracts import futuresContract

    contract = futuresContract("CAD10", "20250900")
    fills = data_orders.get_fills_history_for_contract(contract)
    print(fills)

