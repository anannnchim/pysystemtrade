"""
Responsible for:
- Market monitoring via CombForecast.
- Generating target positions for instruments.
"""

import pandas as pd
import matplotlib.pyplot as plt
from program.googlesheet.googlesheet_access import GoogleSheetAccess, convert_to_numeric
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# Configuration
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
SHEET_URL = "https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1742643022#gid=1742643022"
INSTRUMENTS = ["S50", "USD", "GF10"]

# Initialize system
config = Config(CONFIG_PATH)
data = csvFuturesSimData()
s = futures_system(config=config)
sheet_access = GoogleSheetAccess()

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines


def update_market_monitoring():
    """
    Updates market monitoring data in Google Sheets.
    """
    df = pd.DataFrame({
        instrument: s.combForecast.get_combined_forecast(instrument)
        for instrument in INSTRUMENTS
    })

    df = df.tail(252)  # Keep last 252 rows (1 year of trading days)
    sheet_access.write_dataframe_to_sheet(SHEET_URL, "01-Market-monitor", df, start_cell="B11", header=False)


def calculate_target_positions():
    """
    Calculates target positions for all instruments based on capital adjustment.
    :return: DataFrame containing target positions.
    """
    try:
        # Get latest account value from Google Sheets
        equity_list = sheet_access.get_cell_data(SHEET_URL, "Accounting", "C11:C")
        equity_list = convert_to_numeric(equity_list)
        account_value = equity_list[-1]
        print("Account_value: ", account_value)

        # Get backtest capital value
        backtest_acc_value = s.accounts.get_actual_capital()[-1]
        cap_multi = account_value / backtest_acc_value

        # Compute target positions
        target_positions = {}
        for instrument in INSTRUMENTS:
            df = pd.DataFrame({
                "top_pos": round(s.accounts.get_actual_buffers_for_position(instrument).iloc[:, 0] * cap_multi, 0),
                "bot_pos": round(s.accounts.get_actual_buffers_for_position(instrument).iloc[:, 1] * cap_multi, 0),
            })

            # Initialize target column with NaN
            df["target"] = None

            # Set first row's target to 0
            df.iloc[0, df.columns.get_loc("target")] = 0

            # Iterate over DataFrame row by row for correct computation
            for i in range(1, len(df)):
                prev_target = df.iloc[i - 1]["target"]
                top_pos = df.iloc[i]["top_pos"]
                bot_pos = df.iloc[i]["bot_pos"]

                # Apply correct constraint logic
                df.iloc[i, df.columns.get_loc("target")] = min(max(prev_target, bot_pos), top_pos)

            target_positions[instrument] = df["target"]

        return pd.DataFrame(target_positions)

    except Exception as e:
        print(f"Error calculating target positions: {e}")
        return pd.DataFrame()


def get_instrument_target_position(instrument_code):
    """
    Retrieves and computes the target position for a given instrument.

    :param instrument_code: The instrument code (e.g., "S50", "USD", "GF10").
    :return: DataFrame with top_pos, bot_pos, and target columns.
    """
    try:
        # Retrieve account value and capital multiplier
        equity_list = sheet_access.get_cell_data(SHEET_URL, "Accounting", "C11:C")
        equity_list = convert_to_numeric(equity_list)
        account_value = equity_list[-1]
        backtest_acc_value = s.accounts.get_actual_capital()[-1]
        cap_multi = account_value / backtest_acc_value

        # Fetch top and bottom position values
        df = pd.DataFrame({
            "top_pos": round(s.accounts.get_actual_buffers_for_position(instrument_code).iloc[:, 0] * cap_multi, 0),
            "bot_pos": round(s.accounts.get_actual_buffers_for_position(instrument_code).iloc[:, 1] * cap_multi, 0),
        })

        # Initialize target column
        df["target"] = None

        # Set first row's target to 0
        df.iloc[0, df.columns.get_loc("target")] = 0

        # Compute target positions iteratively
        for i in range(1, len(df)):
            prev_target = df.iloc[i - 1]["target"]
            top_pos = df.iloc[i]["top_pos"]
            bot_pos = df.iloc[i]["bot_pos"]

            df.iloc[i, df.columns.get_loc("target")] = min(max(prev_target, bot_pos), top_pos)

        print(df.tail(5))  # Show the last 5 rows for quick verification
        return df

    except Exception as e:
        print(f"Error retrieving data for {instrument_code}: {e}")
        return pd.DataFrame()

def main():
    """
    Main execution function to update market monitoring and target positions.
    """
    print("Updating market monitoring data...")
    update_market_monitoring()

    print("\nCalculating target positions...")
    target_position_df = calculate_target_positions()
    print(target_position_df.tail(5))

    # Interactive instrument lookup
    while True:
        instrument = input("\nEnter instrument code (S50, USD, GF10) or press Enter to exit: ").strip().upper()

        if instrument == "":
            print("Exiting program.")
            break  # Exit the loop if Enter is pressed

        if instrument in INSTRUMENTS:
            get_instrument_target_position(instrument)
        else:
            print("Invalid instrument code. Please enter a valid instrument (S50, USD, GF10).")


if __name__ == "__main__":
    main()
