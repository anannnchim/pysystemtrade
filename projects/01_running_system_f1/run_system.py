"""
Reponsible for:
1. Generate order
2.
"""

import pandas as pd

from program.googlesheet.googlesheet_access import GoogleSheetAccess
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")

data = csvFuturesSimData()

s = futures_system(config=config)

# # Adjust pandas options to display all rows and columns
# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.max_rows', None)  # Show all rows
# pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

# Initialize data source
sheet_access = GoogleSheetAccess()

# INPUT
sheet_url = 'https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1742643022#gid=1742643022'


if __name__ == '__main__':



    # Note 1. CombForecast for market monitoring
    # FIXME: Make it outputs number not string
    df = pd.DataFrame({
        "S50": s.combForecast.get_combined_forecast("S50"),
        "USD": s.combForecast.get_combined_forecast("USD"),
        "GF10": s.combForecast.get_combined_forecast("GF10"),
    })
    df = df.tail(10)
    print(df)
    # df = df.astype(float)  # Ensure all values are numeric
    sheet_access.write_dataframe_to_sheet(sheet_url, "01-Market-monitor", df, start_cell='B11')

    # Note 2. Generate target position
    # FIXME: Get capital, calculate capital multi, adjust target position
    # data = sheet_access.get_worksheet_data(sheet_url, "Accounting")

    
    # s.portfolio.capital_multiplier()  # Ratio between actual account value over initial capital
    # s.accounts.get_actual_capital()
    #
    # df = pd.DataFrame({
    #     "S50": s.portfolio.get_actual_position("S50"),
    #     "USD": s.portfolio.get_actual_position("USD"),
    #     "GF10": s.portfolio.get_actual_position("GF10")
    # })
    # print(df)
    #
    # # print(s.portfolio.get_buffers_for_position("USD"))
    #
    # # Note: ref
    # c1 = "S50"
    #
    # df = pd.DataFrame({
    #     "Price": s.rawdata.get_daily_prices(c1),
    #     "Change": s.rawdata.daily_returns(c1),
    #     "InsRisk": s.positionSize.get_instrument_value_vol(c1),
    #     "NotionalCap": s.positionSize.get_notional_trading_capital(),
    #     "DailyRiskTarget": s.positionSize.get_daily_cash_vol_target(),
    #     "VolScalar": s.positionSize.get_average_position_at_subsystem_level(c1),
    #     "CombForecast": s.combForecast.get_combined_forecast(c1),
    #     "SubSystemPosition": s.portfolio.get_subsystem_position(c1),
    #
    #     "buffer": s.portfolio.get_buffers(c1),
    #
    #     "NotionalPosition": s.portfolio.get_notional_position(c1),
    #     "Upper": s.portfolio.get_buffers_for_position(c1).iloc[:, 0],
    #     "Lower": s.portfolio.get_buffers_for_position(c1).iloc[:, 1],
    #
    #     "CAPMULTI": s.accounts.capital_multiplier(),
    #     "AC_CAP": s.accounts.get_actual_capital(),
    #     "AC_POS": s.accounts.get_actual_position(c1),
    #     "Return": s.accounts.portfolio()/s.accounts.get_actual_capital(),
    #     "PNL": s.accounts.portfolio()
    #
    # })
    # df = df.tail(10)
    # print(df)
    #
    # data  = sheet_access.write_dataframe_to_sheet(sheet_url, "5-Backtest-data", df, start_cell='B11')
    #
    #
