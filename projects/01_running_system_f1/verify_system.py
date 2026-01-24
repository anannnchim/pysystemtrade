import pandas as pd
from private.gg_config_path import SYSTEM_F1_SHEET_URL
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
from program.googlesheet.googlesheet_access import GoogleSheetAccess


config = Config("private/systems/system_f1/private_config.yaml")
sheet_url = SYSTEM_F1_SHEET_URL
start_date = "2025-02-03"

data = csvFuturesSimData()
s = futures_system(config=config, data=data)
sheet_access = GoogleSheetAccess()


if __name__ == '__main__':

    df = pd.DataFrame({
        "ActualCapital": s.accounts.get_actual_capital(),
        "PNL": s.accounts.portfolio_with_multiplier(),
    })

    df_subset = df.loc[start_date:]
    df_subset.fillna(0, inplace=True)

    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "02-Verify-system",
        df_subset, "B12",
        header=False)
