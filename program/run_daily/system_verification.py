import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
from systems.rawdata import RawData
import matplotlib.pyplot as plt


# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")


data = csvFuturesSimData()
#data = dbFuturesSimData()

s = futures_system(config=config, data=data)

c1 = "USD"

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    # Note - General
    s.rawdata.methods()

    # Note - Config
    s.config.get_element("percentage_vol_target") # Return % risk target (number%)
    s.config.get_element("notional_trading_capital")  # Return initial capital in USD
    s.get_list_of_duplicate_instruments_to_remove()  # Return market to be removed
    s.config.start_date = "2023-06-01" # Set element


    # Note 1 - RawData
    s.rawdata.get_daily_prices(c1) # Price

    s.rawdata.get_value_of_block_price_move(c1)  # Multiplier
    s.rawdata.rolls_per_year(c1) # Roll per year
    s.rawdata.get_raw_cost_data(c1) # cost data

    s.rawdata.annualised_returns_volatility(c1) # Annual risk in USD
    s.rawdata.daily_returns_volatility(c1)  # Daily risk in USD
    s.rawdata.get_daily_percentage_volatility(c1) # Daily % risk or (number%)

    s.rawdata.daily_returns(c1)  # Change in price USD
    s.rawdata.get_daily_percentage_returns(c1) # % Change in price (need to x 100 to be %number)

    # Note 2 - ForecastScaleCap
    s.forecastScaleCap.get_raw_forecast(c1, "ewmac16_64") # raw (net ema / vol)
    s.forecastScaleCap.get_scaled_forecast(c1, "ewmac16_64")  # scaled
    s.forecastScaleCap.get_capped_forecast(c1, "ewmac16_64")  # capped, scaled forecast

    # Note 3 - ForecastCombine
    s.combForecast.get_forecast_diversification_multiplier_fixed(c1)  # FIX FDM
    s.combForecast.get_raw_fixed_forecast_weights(c1) # forecast weight
    s.combForecast.get_forecast_weights(c1)  # forecast weight exclude expensive rule
    s.combForecast.cheap_trading_rules_post_processing(c1)  # List of cheap enough trading rule, compared with 0.13
    s.combForecast.get_combined_forecast(c1)  # Main: weighed capped, scaled forecast

    # Note 5 - positionSize
    s.positionSize.get_daily_cash_vol_target() # Get Daily risk target
    s.positionSize.get_instrument_value_vol(c1) # Daily instrument ris per cont in Base currency.
    s.positionSize.get_average_position_at_subsystem_level(c1)  # vol_scalar =  target vol / instru vol
    s.positionSize.get_subsystem_position(c1)  # Main: (vol_scalr * combForecast)/10 [assume full fixed cap]
    s.positionSize.get_subsystem_buffers(c1)
    s.positionSize.get_buffers_for_subsystem_position(c1)


    # Note 6 - portfolio
    s.portfolio.get_baseccy_value_per_contract(c1) # Get instrument contract value in base currency
    s.portfolio.get_trading_capital()
    s.portfolio.get_instrument_weights()  # Weight that account for missing position and un-added up weight
    s.portfolio.get_fixed_instrument_diversification_multiplier()  # Fix IDM
    s.portfolio.get_instrument_diversification_multiplier() # Estimated IDM
    s.portfolio.capital_multiplier()  # Ratio between actual account value over initial capital
    s.portfolio.get_notional_position(c1)  # Fixed but include weight, idm
    s.portfolio.get_buffers_for_position(c1)
    s.portfolio.get_actual_position(c1)  # Main: Account everything (weight, idm, actual capital)
    s.portfolio.get_buffers(c1)
    s.portfolio.get_actual_buffers_for_position(c1)
    s.portfolio.get_instrument_correlation_matrix().corr_list # Correlation matrix

    # ADDITIONAL

    # Correlation
    s.portfolio.get_list_of_instrument_returns_correlations().corr_list

    # Per contract value / fixed capital
    s.portfolio.get_baseccy_value_per_contract(c1)  # Value per cont / instrument
    s.portfolio.get_per_contract_value()  # static: value per cont / init capital
    s.portfolio.get_per_contract_value_as_proportion_of_capital_df()  # Combine timeseries of value per cont / init capital
    s.portfolio.get_per_contract_value_as_proportion_of_capital(c1)  # individual: value per cont / init capital

    # Leverage & Weight
    # noted: leverage calculated using fixed cap, un-round position
    s.portfolio.get_leverage_for_original_position()  # sum[abs(value_per_cont x notional cont / init capital)]
    s.portfolio.get_original_portfolio_weight_df()  # value_per_cont x notional cont / init capital
    s.portfolio.get_portfolio_weight_series_from_contract_positions(c1)

    # Risk
    s.portfolio.get_stdev_df()  # DF of Instrument Annual Risk
    s.portfolio.get_sum_annualised_risk_for_original_positions()  # Annual weighted portfolio risk
    s.portfolio.get_portfolio_risk_for_original_positions()  # Annual port risk include correlation, 0 if 1 instrument

    # Return
    s.portfolio.pandl_across_subsystems()  # PENDING
    s.portfolio.returns_across_instruments_as_df()  # all daily return

    # Turnover
    s.portfolio.turnover_across_subsystems()  # PENDING

    # Note 7 - accounts

    # Price
    s.accounts.get_instrument_prices_for_position_or_forecast(c1)

    # Get buffered position
    s.accounts.get_buffered_position(c1)
    s.accounts.get_buffered_position_with_multiplier(c1)

    # accountCosts & Turnover
    s.accounts.get_SR_cost_per_trade_for_instrument(c1)  # SR cost per trade
    s.accounts.forecast_turnover(c1, "ewmac16_64")  # AnnualisedtTurnover for each instrument & rule
    s.rawdata.rolls_per_year(c1)  # Holding turnover
    s.accounts.get_SR_holding_cost_only(c1) # (SR * roll per year) x 2
    s.accounts.get_SR_transaction_cost_for_instrument_forecast(c1, "ewmac16_64")  # Transaction cost in SR
    s.accounts.get_SR_cost_for_instrument_forecast(c1, "ewmac16_64")  # [hold+trans]turnover * SR cost
    s.accounts.get_SR_cost_given_turnover(c1, 5)  ## includes both holding and trading costs for a turnover of 10
    s.accounts.get_SR_trading_cost_only_given_turnover(c1, 5.0)  ## trading five times a year, no holding cost
    s.accounts.subsystem_turnover("CORN_mini") # transaction_turnover
    s.accounts.total_portfolio_level_turnover()  # Turnover

    # accountPortfolio: Two ways to get daily return but it's more or less the same
    """
    # 1. pandl_for_instrument / get_notional_capital with get_buffered_position
    # 2. pandl_for_instrument_with_multiplier / get_actual_capital with get_buffered_position_with_multiplier
    """
    s.accounts.portfolio().percent
    s.accounts.portfolio_with_multiplier().percent

    # Summary statistic
    s.accounts.portfolio().net.percent.stats()
    s.accounts.portfolio().gross.percent.stats()
    s.accounts.portfolio().costs.percent.stats()

    # Cumulative / Rolling annual risk / Drawdown
    s.accounts.portfolio().percent.curve() # For cumulative: TWR (number%)
    s.accounts.portfolio().percent.rolling_ann_std()
    s.accounts.portfolio().percent.drawdown()

    # Table of data
    s.accounts.to_ncg_frame()  # DF of gross,cost,net
    s.accounts.portfolio().costs.annual.percent # Annual cost
    s.accounts.portfolio().net.annual.percent # Annual return
    s.accounts.portfolio().costs.monthly.percent # Monthly cost
    s.accounts.portfolio().captial

    # Return all individual daily returns
    s.accounts.portfolio().to_frame()

    # Individual statatistic
    s.accounts.portfolio().annual.percent.mean()
    s.accounts.portfolio().annual.percent.std()
