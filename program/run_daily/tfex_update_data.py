from program.initialize.convert_csv_to_parquet import BARCHART_CONFIG
from sysdata.config.production_config import get_production_config
from sysinit.futures.adjustedprices_from_db_multiple_to_db import process_adjusted_prices_single_instrument
from sysinit.futures.contract_prices_from_split_freq_csv_to_db import init_db_with_split_freq_csv_prices_for_code
from sysinit.futures.multipleprices_from_db_prices_and_csv_calendars_to_db import process_multiple_prices_single_instrument
from sysinit.futures.rollcalendars_from_db_prices_to_csv import build_and_write_roll_calendar
import os
import glob
import builtins

# Constant
BARCHART_PATH = get_production_config().get_element("barchart_path")
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(BASE_PATH, "data")
csv_roll_data_path = os.path.join(DATA_PATH, "futures", "roll_calendars_csv")
csv_multiple_data_path = os.path.join(DATA_PATH, "futures", "multiple_prices_csv")
csv_adjusted_data_path = os.path.join(DATA_PATH, "futures", "adjusted_prices_csv")

"""
There will be 3 files in roll calendar, multiple, adjusted. 
"""
if __name__ == '__main__':

    instrument_list = [
        "S50-TFEX",
        "GF10-TFEX",
    ]

    for instrument in instrument_list:


        """
        1. Convert contract price (csv) into parquet for an instrument.
        """
        init_db_with_split_freq_csv_prices_for_code(
            instrument, datapath=BARCHART_PATH, csv_config=BARCHART_CONFIG, ignore_duplication=True
        )

        """
        2. rollcalendars_from_db_prices_to_csv
        """
        builtins.input = lambda _: "y"
        build_and_write_roll_calendar(
            instrument, output_datapath=csv_roll_data_path
        )

        """
        3. multiple prices
        """
        process_multiple_prices_single_instrument(
            instrument_code=instrument,
            csv_multiple_data_path=csv_multiple_data_path,
            csv_roll_data_path=csv_roll_data_path,
            ADD_TO_DB=True,
            ADD_TO_CSV=True,
        )

        """
        4. adjusted prices
        """
        process_adjusted_prices_single_instrument(
            instrument_code=instrument,
            ADD_TO_DB=False,
            ADD_TO_CSV=True,
            csv_adj_data_path=csv_adjusted_data_path
        )
        """
         5. Remove parquet files
         """

        # 5. Remove file
        BASE = os.path.join(
            DATA_PATH,
            "parquet",
        )
        patterns = [

            f"{BASE}/futures_multiple_prices/{instrument}.parquet",

            f"{BASE}/futures_contract_prices/{instrument}#*.parquet",

            f"{BASE}/futures_contract_prices/Day@{instrument}#*.parquet",

        ]

        for pattern in patterns:
            files = glob.glob(pattern)

            for f in files:
                print("REMOVE:", f)
                os.remove(f)

        print("DONE deleting parquet for", instrument)