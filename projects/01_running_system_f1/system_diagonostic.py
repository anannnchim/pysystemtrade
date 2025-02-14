"""
Objective: Access system data.

"""
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
from program.googlesheet.googlesheet_access import GoogleSheetAccess

# INPUT
sheet_url = 'https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1248180211#gid=1248180211'
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

    # # PNL
    # PNL = pd.DataFrame({
    #     "S50": s.accounts.portfolio()['S50'],
    #     "USD": s.accounts.portfolio()['USD'],
    #     "GF10": s.accounts.portfolio()['GF10'],
    #     "ALL": s.accounts.portfolio()
    # })
    #
    # # 1.1 Change
    # code = "S50"
    # pd.DataFrame({
    #     "Price": s.accounts.get_instrument_prices_for_position_or_forecast(code),
    #     "ChangePerCont": s.accounts.get_instrument_prices_for_position_or_forecast(code).diff(1) * s.accounts.get_value_of_block_price_move(code)
    # })
    #
    # # 1.2 Position
    # # Assume single, fix weight.
    # pd.DataFrame({
    #     "Up": s.portfolio.get_buffers_for_position("S50").iloc[:, 0],
    #     "Down": s.portfolio.get_buffers_for_position("S50").iloc[:, 1],
    #     "Pos": s.portfolio.get_notional_position("S50"),
    #     "rounded": s.accounts.get_buffered_position("S50")  # This is target hold.
    # })

    code = "S50"
    c = pd.DataFrame({

        # Price
        "Price": s.accounts.get_instrument_prices_for_position_or_forecast(code),
        "ChangePerCont": s.accounts.get_instrument_prices_for_position_or_forecast(code).diff(
            1) * s.accounts.get_value_of_block_price_move(code),

        # PNL from portfolio
        "PNL": s.accounts.portfolio()[code],
        "PNLForInstru": s.accounts.pandl_for_instrument(code),
        "Gross": s.accounts.pandl_for_instrument(code).gross,
        "Costs": s.accounts.pandl_for_instrument(code).costs,
        "Net": s.accounts.pandl_for_instrument(code).net,

        # Position
        "Up": s.portfolio.get_buffers_for_position(code).iloc[:, 0],
        "Down": s.portfolio.get_buffers_for_position(code).iloc[:, 1],
        "Pos": s.portfolio.get_notional_position(code),
        "rounded": s.accounts.get_buffered_position(code),

        # Actaul Capi
        "CapMulti": s.portfolio.capital_multiplier(),
        "ActualCapital": s.accounts.get_actual_capital(),
        "PortfolioMulti":s.accounts.portfolio_with_multiplier(),
        "Portfolio": s.accounts.portfolio(),

        "Forecast": s.combForecast.get_combined_forecast("S50")
    })

    # FIX
    pd.DataFrame({
        "PNL": s.accounts.portfolio().net,
        "Cap": s.accounts.get_notional_capital(),
        "PNLpercent": s.accounts.portfolio().net.percent
    })

    # Compound
    pd.DataFrame({
        "PNL": s.accounts.portfolio_with_multiplier().net,
        "Cap": s.accounts.get_actual_capital(),
        "PNLpercent": s.accounts.portfolio_with_multiplier().net.percent
    })

    #
    #

    """
    # PNL calculation
    s.accounts.portfolio().pandl_calculator_with_costs.costs_percentage_pandl()
    s.accounts.portfolio().pandl_calculator_with_costs._costs_pandl_in_base_currency
    
    # Cost
    s.accounts.portfolio().pandl_calculator_with_costs
    """

    # Modify
    c = c.tail(300)
    c.fillna(0, inplace=True)  # Replace NaN with zero (or another value)

    # Write to sheet
    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "03-System-diagnostic",
        c,
        "B11",
        header=False)


    # Note - use Backtesting data.
    # df = pd.DataFrame({
    #     "Price": s.rawdata.get_daily_prices(c1),
    #     "Change": s.rawdata.daily_returns(c1),
    #     "InsRisk": s.positionSize.get_instrument_value_vol(c1),
    #     "NotionalCap": s.positionSize.get_notional_trading_capital(),
    #     "DailyRiskTarget": s.positionSize.get_daily_cash_vol_target(),
    #     "VolScalar": s.positionSize.get_average_position_at_subsystem_level(c1),
    #     "CombForecast": s.combForecast.get_combined_forecast(c1),
    #     "NotionalPosition": s.portfolio.get_notional_position(c1),
    #     "Upper": s.portfolio.get_buffers_for_position(c1).iloc[:, 0],
    #     "Lower": s.portfolio.get_buffers_for_position(c1).iloc[:, 1],
    #
    #     "CAPMULTI": s.accounts.capital_multiplier(),
    #     "AC_CAP": s.accounts.get_actual_capital(),
    #     "AC_POS": s.accounts.get_actual_position(c1),
    #     "Return": s.accounts.portfolio()/s.accounts.get_actual_capital(),
    #     "PNL": s.accounts.portfolio()
    # })

