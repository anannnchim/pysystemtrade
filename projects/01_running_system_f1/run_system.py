import pandas as pd
from private.gg_config_path import SYSTEM_F1_SHEET_URL
from program.googlesheet.googlesheet_access import GoogleSheetAccess, convert_to_numeric
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# Configuration
CONFIG_PATH = "private/systems/system_f1/private_config.yaml"
SHEET_URL = SYSTEM_F1_SHEET_URL

# Initialize system
config = Config(CONFIG_PATH)
data = csvFuturesSimData()
s = futures_system(config=config, data=data)
sheet_access = GoogleSheetAccess()

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

def get_instrument_target_position(instrument_code, account_value):
    """
    Compute target position for a given instrument.

    :param instrument_code: e.g. "S50", "USD", "GF10"
    :param account_value: current trading capital
    :return: DataFrame with top_pos, bot_pos, target
    """

    try:
        # -------------------------------
        # 1. Validate capital input
        # -------------------------------
        if account_value is None:
            raise ValueError("account_value is None")

        if config.notional_trading_capital == 0:
            raise ValueError("config.notional_trading_capital is 0")

        multiplier = account_value / config.notional_trading_capital

        # -------------------------------
        # 2. Get buffers
        # -------------------------------
        buffers = s.accounts.get_buffers_for_position(instrument_code)

        df = pd.DataFrame({
            "top_pos": buffers.iloc[:, 0],
            "bot_pos": buffers.iloc[:, 1],
        })

        # -------------------------------
        # 3. Apply capital scaling
        # -------------------------------
        df["top_pos"] = df["top_pos"] * multiplier
        df["bot_pos"] = df["bot_pos"] * multiplier

        # Optional: round after scaling
        df["top_pos"] = df["top_pos"].round(0)
        df["bot_pos"] = df["bot_pos"].round(0)

        # -------------------------------
        # 4. Compute target
        # -------------------------------
        df["target"] = 0.0   # numeric dtype (important)

        for i in range(1, len(df)):
            prev_target = df.iloc[i - 1]["target"]
            top_pos = df.iloc[i]["top_pos"]
            bot_pos = df.iloc[i]["bot_pos"]

            df.iloc[i, df.columns.get_loc("target")] = \
                min(max(prev_target, bot_pos), top_pos)

        print(df.tail(5).round(0))
        return df

    except Exception as e:
        print(f"Error retrieving data for {instrument_code}: {e}")
        return pd.DataFrame()


def main():
    print("\n=== Calculating Target Positions ===")

    try:
        # ---------------------------------
        # 1. Retrieve capital from Google Sheet
        # ---------------------------------
        equity_list = sheet_access.get_cell_data(
            SHEET_URL,
            "Accounting",
            "C11:C"
        )

        equity_list = convert_to_numeric(equity_list)

        if not equity_list:
            raise ValueError("No equity data found in sheet")

        account_value = equity_list[-1]

        if account_value is None:
            raise ValueError("Latest account value is None")

        # ---------------------------------
        # 2. Process all instruments
        # ---------------------------------
        all_targets = {}

        instrument_list = s.get_instrument_list()

        for instrument in instrument_list:
            print(f"Processing {instrument} =====================")

            df = get_instrument_target_position(
                instrument,
                account_value
            )

            if not df.empty:
                all_targets[instrument] = df["target"]

        # ---------------------------------
        # 3. Combine into portfolio DataFrame
        # ---------------------------------
        if not all_targets:
            raise ValueError("No target positions calculated")

        target_df = pd.DataFrame(all_targets)

        print("\n=== Latest Target Snapshot ===")
        print(target_df.tail(5).round(0))

        print(f"Account value: {account_value}")

        return target_df

    except Exception as e:
        print(f"Error in main(): {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    main()
