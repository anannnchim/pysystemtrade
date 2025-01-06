import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.accounts.accounts_stage import Account
from systems.basesystem import System
from systems.forecast_combine import ForecastCombine
from systems.forecast_scale_cap import ForecastScaleCap
from systems.forecasting import Rules
from systems.portfolio import Portfolios
from systems.positionsizing import PositionSizing
from systems.rawdata import RawData
import matplotlib.pyplot as plt


data = csvFuturesSimData()
s = System(
    [
        Account(),
        Portfolios(),
        PositionSizing(),
        ForecastCombine(),
        ForecastScaleCap(),
        Rules(),
        RawData(),
    ],
    data=data,
    config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/system_f1/config.yaml")
)

c1 = "S50"
c2 = "USD"
c3 = "GF10"

if __name__ == '__main__':

    # Note 4 - Account costs & turnover
    s.accounts.get_SR_cost_per_trade_for_instrument(c1)  # SR cost per trade
    s.accounts.forecast_turnover("S50", "ewmac16_64")  # Turnover for each instrument & rule
    s.rawdata.rolls_per_year(c1) * 2  # Holding turnover

    s.accounts.get_SR_holding_cost_only(c1)
    s.accounts.get_SR_transaction_cost_for_instrument_forecast(c1, "ewmac16_64")  # Transaction cost in SR
    s.accounts.get_SR_cost_for_instrument_forecast(c1, "ewmac16_64")  # [hold+trans]turnover * SR cost

    # Note - Config
    s.config.get_element("percentage_vol_target") # Return % risk target (number%)
    s.config.get_element("notional_trading_capital")  # Return initial capital in USD

    # Note 1 - RawData
    s.rawdata.get_daily_prices(c1) # Price

    s.rawdata.get_value_of_block_price_move(c1)  # Multiplier
    s.rawdata.rolls_per_year(c1) # Roll per year
    s.rawdata.get_raw_cost_data(c1) # cost data

    s.rawdata.annualised_returns_volatility(c1) # Annual risk in USD
    s.rawdata.daily_returns_volatility(c1)  # Daily % risk in USD
    s.rawdata.get_daily_percentage_volatility(c1) # Daily % risk or (number%)

    s.rawdata.daily_returns(c1)  # Change in price USD
    s.rawdata.get_daily_percentage_returns(c1) # % Change in price

    # Note 2 - ForecastScaleCap
    s.forecastScaleCap.get_raw_forecast(c1, "ewmac16_64") # raw (net ema / vol)
    s.forecastScaleCap.get_scaled_forecast(c1, "ewmac16_64")  # scaled
    s.forecastScaleCap.get_capped_forecast(c1, "ewmac16_64")  # capped, scaled forecast

    # Note 3 - ForecastCombine
    s.combForecast.get_forecast_diversification_multiplier_fixed(c1)  # FIX FDM
    s.combForecast.get_raw_fixed_forecast_weights(c1) # forecast weight
    s.combForecast.get_forecast_weights(c1)  # forecast weight exclude expensive rule
    s.combForecast.cheap_trading_rules_post_processing(c1)  # List of cheap enough trading rule
    s.combForecast.get_combined_forecast(c1)  # Main: weighed capped, scaled forecast

    # Note 5 - positionSize
    s.positionSize.get_average_position_at_subsystem_level(c1)  # vol_scalar =  target vol / instru vol
    s.positionSize.get_subsystem_position(c1)  # Main: (vol_scalr * combForecast)/10 [assume full fixed cap]
    s.positionSize.get_subsystem_buffers(c1)
    s.positionSize.get_buffers_for_subsystem_position(c1)


    # Note 6 - portfolio




    #
    # # Note 2 - System data
    #
    # print(" 1. accounts---------------------------------------------")
    # s.accounts.get_actual_position(c1) # 0.380550 , Actual target position, we want to hold
    #
    # print("2. portfolio ---------------------------------------------")
    # s.portfolio.get_actual_buffers_for_position(c1) # 0.529692  0.433385, Actual bounds
    # s.portfolio.get_notional_position(c1) # 0.37 , FIX CAP, position without forecast?
    # s.portfolio.get_buffers(c1) #  0.037772, 0.1 x get_notional_position

    # #
    # # Additional RISK
    # s.portfolio.get_df_of_perc_vol()
    # s.portfolio.annualised_percentage_vol(c1)
    # s.portfolio.daily_percentage_vol100scale(c1)
    #
    # # Additional position data
    # s.portfolio.returns_across_instruments_as_df()
    # s.portfolio.get_instrument_weights()
    # s.portfolio.get_subsystem_position(c1) # FIX, assume fully invest
    # s.portfolio.turnover_across_subsystems()
    # s.portfolio.get_average_position_at_subsystem_level(c1)
    # s.portfolio.get_leverage_for_original_position()
    # s.portfolio.get_portfolio_risk_for_original_positions()
    # s.portfolio.get_trading_capital()
    # s.combForecast.get_combined_forecast(c1).tail(2)
    #
    #
    # # Note - Check performance
    # s.accounts.portfolio().stats()
    # # print(s.accounts.portfolio().curve())
    # # s.accounts.portfolio().curve().plot()
    # # plt.show() #  7260.686027
    #
    # # print(s.accounts.portfolio().net.percent.curve())
    # # s.accounts.portfolio().net.percent.curve().plot()
    # # plt.show() #  1.270271 mean cum gain of 1.27% or X%
    #
    # # s.accounts.portfolio().annual.plot()
    # # plt.show()
    #
    # # Note: Check cost
    # s.accounts.portfolio().costs.annual
    # s.accounts.portfolio().costs.annual.percent
    #
    #
    #
    #
    #
    #
    #
    #
    # # print(s.accounts.get_actual_position(c2))
    # # print(s.accounts.get_actual_position(c3))
    #
    # # print("1. Avg. Position ---------------------------------------------")
    # # print(s.positionSize.get_average_position_at_subsystem_level(c1))
    #
    # # print("1. Avg. Position ---------------------------------------------")
    # # print()
    #
    #
    #
    #
    #
    #
    #
    #
