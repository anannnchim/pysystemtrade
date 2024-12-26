from sysdata.config.production_config import get_production_config
from syscore.fileutils import resolve_path_and_filename_for_package
from sysdata.csv.csv_futures_contract_prices import ConfigCsvFuturesPrices, csvFuturesContractPriceData
from sysinit.futures.contract_prices_from_split_freq_csv_to_db import (
    init_db_with_split_freq_csv_prices_for_code,
)

# Config for the Barchart CSV files
BARCHART_CONFIG = ConfigCsvFuturesPrices(
    input_date_index_name="Time",  # Matches the CSV header
    input_skiprows=0,  # No rows to skip
    input_skipfooter=0,  # No footer rows to skip
    input_date_format="%Y-%m-%dT%H:%M:%S",
    input_column_mapping=dict(
        OPEN="Open", HIGH="High", LOW="Low", FINAL="Close", VOLUME="Volume"
    ),
)

# Resolve the path to the CSV files
# datapath = resolve_path_and_filename_for_package(
#     get_production_config().get_element_or_default("barchart_path", None)
# )
#

if __name__ == '__main__':
    """
    Convert contract price (csv) into parquet for an instrument. 
    """
    datapath = '/Users/nanthawat/PycharmProjects/bc-utils/data'

    # Note 1. Convert single instrument
    # # Import prices for a single instrument (CORN)
    init_db_with_split_freq_csv_prices_for_code("MXP", datapath=datapath, csv_config=BARCHART_CONFIG)

    # Note 2. Convert the whole folder (Not working)
    # csv_prices = csvFuturesContractPriceData(datapath)
    # instrument_codes = csv_prices.get_list_of_instrument_codes_with_merged_price_data()
    # instrument_codes.sort()
    # for instrument_code in instrument_codes:
    #     print(instrument_code)
    #     init_db_with_split_freq_csv_prices_for_code(
    #         instrument_code,
    #         datapath,
    #         csv_config=BARCHART_CONFIG,
    #         ignore_duplication=True,  # if True, we overwrite existing prices
    #     )
