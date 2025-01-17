from sysdata.data_blob import dataBlob
from sysproduction.data.prices import get_list_of_instruments, diagPrices

if __name__ == '__main__':
    # instrument_list = get_list_of_instruments(dataBlob(), source="multiple")
    # print("Instruments:", instrument_list)

    # instrument_list = get_list_of_instruments(dataBlob(), source="single")
    # print("Instruments:", instrument_list)

    # instrument_list = get_list_of_instruments(dataBlob(), source="config")
    # print("Configured Instruments:", instrument_list)

    price_data = diagPrices(dataBlob())
    list_of_instrument_codes = price_data.get_list_of_instruments_in_multiple_prices()
    print(list_of_instrument_codes)
