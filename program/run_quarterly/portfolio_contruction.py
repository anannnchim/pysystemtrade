"""
Functionality

1. Show expensive rules
2. Check liquidity
"""
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import systems.provided.static_small_system_optimise.optimise_small_system

# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_02_config.yaml")

# Adjust pandas options to display all rows and columns
# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.max_rows', None)  # Show all rows
# pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines


s = futures_system(config=config, data=data)

if __name__ == '__main__':

    # Note - Plot ----------------------------------------
    s.accounts.portfolio().percent.curve().plot()
    plt.show()

    print(s.accounts.portfolio().percent.rolling_ann_std())
    s.accounts.portfolio().percent.rolling_ann_std().plot()
    plt.show()

    for instrument in s.get_instrument_list():
        s.accounts.get_buffered_position(instrument).plot()
    plt.show()

    # IDM
    s.portfolio.get_instrument_diversification_multiplier().plot()
    plt.show()

    # Correlation
    correlation = s.portfolio.get_instrument_correlation_matrix().corr_list[-1]
    print(correlation)


    # Note - Start ----------------------------------------
    a = input("1. Check each instrument if it's Expensive: Cost > 0.01")
    for instrument in s.get_instrument_list():
        print(instrument, ": ", round(s.accounts.get_SR_cost_per_trade_for_instrument(instrument), 4))
        if s.accounts.get_SR_cost_per_trade_for_instrument(instrument) > 0.01:
            print("Too expensive. Remove")
        else:
            print(instrument, " PASS")

    a = input("2. Check each rule if it's cheap enough to trade: Cost in SR < 0.13")
    for instrument in s.get_instrument_list():
        print(s.combForecast.cheap_trading_rules_post_processing(instrument))


    input("3. Chekc if it's too safe to trade: vol < 5%?")
    for instrument in s.get_instrument_list():
        average_annual_risk = s.rawdata.get_daily_percentage_volatility(instrument).mean() * 16
        print("---")
        print(instrument, ": ", round(average_annual_risk, 4))
        if average_annual_risk < 5 :
            print("Too safe to trade. Remove")
        else:
            print(instrument, " PASS")


    input("4. Check average position: should be > 2")
    vol_scalar = {}
    for instrument in s.get_instrument_list():
        vol_scalar[instrument] = s.positionSize.get_average_position_at_subsystem_level(instrument).mean()
        vol_scalar_df = pd.DataFrame([vol_scalar])
    print(vol_scalar_df)

    a = input("5. Check liquidity for each instrument")
    print("Check Liquidity report from Rob.")
    print("https://github.com/robcarver17/reports/blob/master/Liquidity_report")


    # Final position
    input("This is final position: position shouldn't be 0")
    positions = {}
    for instrument in s.get_instrument_list():
        positions[instrument] = s.accounts.get_buffered_position(instrument)
    df = pd.DataFrame(positions)
    print(df)