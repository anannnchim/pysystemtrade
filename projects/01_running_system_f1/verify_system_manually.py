"""
This file is the backtest result.

"""
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
from program.googlesheet.googlesheet_access import GoogleSheetAccess

# INPUT
sheet_url = 'https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1742643022#gid=1742643022'
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")
c1 = "USD"

data = csvFuturesSimData()
s = futures_system(config=config, data=data)

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

# Initialize data source
sheet_access = GoogleSheetAccess()

if __name__ == '__main__':

    #
    # print("Price and multiplier")
    # print(s.rawdata.get_daily_prices(c1))
    # print(s.rawdata.get_value_of_block_price_move(c1))
    #
    # print('Minium Capital to trade 4 contracts')
    # contract_value = s.portfolio.get_baseccy_value_per_contract(c1).tail(1).values
    # instru_risk = s.portfolio.get_stdev_df().tail(1).values
    # risk_target = s.config.get_element("percentage_vol_target")/100
    # print(contract_value * instru_risk * 4/ risk_target)
    #
    # print("Sharpe in Cost")
    # print(s.accounts.get_SR_cost_per_trade_for_instrument(c1))  # SR cost per trade
    #
    # print("1. Cheap rule to trade ---------------------")
    # print(s.combForecast.cheap_trading_rules_post_processing(c1))  # List of cheap enough trading rule
    #
    # print("2 Instrument Annual Risk ---------------------")
    # print(s.portfolio.get_stdev_df())  # Combined instrument annual risk
    # #
    # # 2025-01-16     0.644855
    # # 2025-01-17     0.619203
    # print("3. Vol scalar ---------------------")
    # print(s.positionSize.get_average_position_at_subsystem_level(c1))
    #
    # print('4. Combined forecast ---------------------')
    # print(s.combForecast.get_combined_forecast(c1))
    #
    # print("Sub system position")
    # print(s.positionSize.get_subsystem_position(c1))
    #
    # print('5. Actual position and buffer ---------------------')
    # print(s.portfolio.get_actual_position(c1))
    # print(s.portfolio.get_actual_buffers_for_position(c1))
    # print(s.portfolio.get_buffers(c1) * s.portfolio.capital_multiplier())
    #
    # print('6. Return')
    # print(s.portfolio.returns_across_instruments_as_df())  # all daily return
    # print(s.portfolio.pandl_across_subsystems())
    #
    # # Performance
    # print("7. Performance")
    # print(s.accounts.portfolio().stats())
    #
    #  # Capital
    # print("8. Actual Capital")
    # print(s.accounts.get_actual_capital())
    # print(s.accounts.get_notional_capital())
    #
    # # Net TWR (number%)
    # s.accounts.portfolio().net.percent.curve().plot()
    # plt.show()

    # PNL
    pd.DataFrame({
        "S50": s.accounts.portfolio()['S50'],
        "USD": s.accounts.portfolio()['USD'],
        "GF10": s.accounts.portfolio()['GF10'],
        "ALL": s.accounts.portfolio()
    })

    # CHANGE
    pd.DataFrame({
        "S50": s.accounts.portfolio()['S50'],
        "USD": s.accounts.portfolio()['USD'],
        "GF10": s.accounts.portfolio()['GF10'],
        "ALL": s.accounts.portfolio()
    })


    # CHECK if it's the same as target position



    # Assume single, fix weight.
    pd.DataFrame({
        "Up": s.portfolio.get_buffers_for_position("S50").iloc[:, 0],
        "Down": s.portfolio.get_buffers_for_position("S50").iloc[:, 1],
        "Pos": s.portfolio.get_notional_position("S50"),
        "rounded": s.accounts.get_buffered_position("S50")
    })

    # PENDING
    s.accounts.get_buffered_position_with_multiplier("S50")
    s.accounts.get_buffered_subsystem_position("S50")

    # Note - use Backtesting data.

    df = pd.DataFrame({
        "Price": s.rawdata.get_daily_prices(c1),
        "Change": s.rawdata.daily_returns(c1),
        "InsRisk": s.positionSize.get_instrument_value_vol(c1),
        "NotionalCap": s.positionSize.get_notional_trading_capital(),
        "DailyRiskTarget": s.positionSize.get_daily_cash_vol_target(),
        "VolScalar": s.positionSize.get_average_position_at_subsystem_level(c1),
        "CombForecast": s.combForecast.get_combined_forecast(c1),
        "NotionalPosition": s.portfolio.get_notional_position(c1),
        "Upper": s.portfolio.get_buffers_for_position(c1).iloc[:, 0],
        "Lower": s.portfolio.get_buffers_for_position(c1).iloc[:, 1],

        "CAPMULTI": s.accounts.capital_multiplier(),
        "AC_CAP": s.accounts.get_actual_capital(),
        "AC_POS": s.accounts.get_actual_position(c1),
        "Return": s.accounts.portfolio()/s.accounts.get_actual_capital(),
        "PNL": s.accounts.portfolio()
    })



"""
1. What I try to achieve?

- Get equity of backtest vs live trading, to see the different from execution. 
- How to get backtest demo? 
    -    Check if different equity level will have different return 
"""