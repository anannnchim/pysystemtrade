"""
Objective: Verify backtest vs live trading equity curve
System: System F1
"""
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
from program.googlesheet.googlesheet_access import GoogleSheetAccess

# INPUT
sheet_url = 'https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1248180211#gid=1248180211'
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")
start_date = "2025-02-03"

data = csvFuturesSimData()
s = futures_system(config=config, data=data)

# Initialize data source
sheet_access = GoogleSheetAccess()

if __name__ == '__main__':

    df = pd.DataFrame({
        "ActualCapital": s.accounts.get_actual_capital(),
        "PNL":s.accounts.portfolio_with_multiplier(),
    })

    df_subset = df.loc[start_date:]
    df_subset.fillna(0, inplace=True)

    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "02-Verify-system",
        df_subset, "B12",
        header=False)
