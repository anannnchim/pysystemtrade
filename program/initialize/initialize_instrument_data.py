from program.initialize.convert_csv_to_parquet import BARCHART_CONFIG
from sysinit.futures.adjustedprices_from_db_multiple_to_db import process_adjusted_prices_all_instruments
from sysinit.futures.contract_prices_from_split_freq_csv_to_db import init_db_with_split_freq_csv_prices_for_code
from sysinit.futures.multipleprices_from_db_prices_and_csv_calendars_to_db import process_multiple_prices_all_instruments
from sysinit.futures.rollcalendars_from_db_prices_to_csv import build_and_write_roll_calendar

if __name__ == '__main__':

    instrument = "CORN_mini"
    # 0. Clean up folder
    """
    TODO: Delete all data in parquet and temp/csv folder 
    """

    # 1. Convert csv to parquet (overwrite)
    # FIXME : Need to fix format
    datapath = '/Users/nanthawat/PycharmProjects/bc-utils/data'
    init_db_with_split_freq_csv_prices_for_code(
        instrument,
        datapath=datapath,
        csv_config=BARCHART_CONFIG,
        ignore_duplication=False)  # Muse be false: since we want to add older data and don't touch current data.

    # 2. Build Roll calendars (overwrite)
    output_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/roll_calendars"
    build_and_write_roll_calendar(instrument, output_datapath=output_path)

    # 3.Build multiple price (overwrite)
    csv_multiple_data_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/multiple_prices"
    csv_roll_data_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/roll_calendars"
    process_multiple_prices_all_instruments(
        csv_multiple_data_path=csv_multiple_data_path,
        csv_roll_data_path=csv_roll_data_path,
        ADD_TO_DB=True,
        ADD_TO_CSV=True,  # IF true it will add csv to temp/multiple path
    )

    # 4. build adjusted price (overwrite)
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/adjusted_prices"
    process_adjusted_prices_all_instruments(
        csv_adj_data_path=path, ADD_TO_DB=True, ADD_TO_CSV=True
    )
