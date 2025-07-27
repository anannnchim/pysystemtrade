import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_new_config.yaml")

s = futures_system(config=config, data=data)


if __name__ == '__main__':

    input("Check if it's too safe to trade: vol < 5%?")
    for instrument in s.get_instrument_list():
        average_annual_risk = s.rawdata.get_daily_percentage_volatility(instrument).mean() * 16
        print(instrument, ": ", round(average_annual_risk, 4))
    print(s.portfolio.get_stdev_df())

    a = input("Check expensive instrument: Cost > 0.01")
    for instrument in s.get_instrument_list():
        print(instrument,": ", round(s.accounts.get_SR_cost_per_trade_for_instrument(instrument),4))
        if s.accounts.get_SR_cost_per_trade_for_instrument(instrument) > 0.01:
            print("Too expensive. Remove")
        else:
            print(instrument, " PASS")

    a = input("Check cheap enough to trade: Cost in SR < 0.13")
    for instrument in s.get_instrument_list():
        print(s.combForecast.cheap_trading_rules_post_processing(instrument))

    input("This is allocation")
    print(s.portfolio.get_instrument_weights())

    input("This is stats in percentage.")
    print(s.accounts.portfolio().percent.stats())

    input("This is Annual data table")
    df = pd.DataFrame({
        "Gross": s.accounts.portfolio().gross.annual.percent,
        "Costs": s.accounts.portfolio().costs.annual.percent,
        "Net": s.accounts.portfolio().net.annual.percent
    }); print(df)

    input("This is annual average return and costs")
    print(df['Gross'].mean())
    print(df['Costs'].mean())
    print(df['Net'].mean())

    input("This is % cummulative return")
    df = pd.DataFrame({
        "Gross": s.accounts.portfolio().gross.percent.curve(),
        "Net": s.accounts.portfolio().net.percent.curve(),
    }); print(df)
    df.plot()
    plt.show()

    input("This is rolling risk%")
    print(s.accounts.portfolio().percent.rolling_ann_std())
    print(s.accounts.portfolio().percent.rolling_ann_std().mean())
    s.accounts.portfolio().percent.rolling_ann_std().plot()
    plt.show()

    input("This is example of buffered position.")
    for instrument in s.get_instrument_list():
        s.accounts.get_buffered_position(instrument).plot()
    plt.show()
    for instrument in s.get_instrument_list():
        print(s.accounts.get_buffered_position(instrument))

    input("Compare return of Fix vs compound")
    df = pd.DataFrame({
        "Fixed": s.accounts.portfolio().net.percent.curve(),
        "Compound": s.accounts.portfolio_with_multiplier().net.percent.curve()
    }); print(df)
    df.plot()
    plt.show()

    input("Different way of getting return. But it pretty much the same.")
    df = pd.DataFrame({
        "NotionalCap": s.accounts.get_notional_capital(),
        "ActualCap": s.accounts.get_actual_capital(),
        "Portfolio": s.accounts.portfolio(),
        "PortfolioMulti": s.accounts.portfolio_with_multiplier(),
        "PortfolioPer": s.accounts.portfolio().percent,
        "PortfolioMultiPer": s.accounts.portfolio_with_multiplier().percent
    }); print(df)

    input("Generate daily_returns.csv for generating report")
    daily_returns = s.accounts.portfolio().percent/100
    daily_returns = pd.DataFrame({
        "Index": daily_returns.index,
        "Return": daily_returns.values
    })
    daily_returns.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/daily_returns.csv", index=False)



"""
CSV
                Gross     Costs        Net
2013-12-31   0.619322  0.000000   0.619322
2014-12-31  35.035229 -1.467480  33.567749
2015-12-31  47.394364 -1.406130  45.988234
2016-12-31 -14.939903 -1.307464 -16.247368
2017-12-31  -7.918356 -0.967374  -8.885730
2018-12-31   2.557889 -1.036171   1.521719
2019-12-31 -17.935246 -0.998671 -18.933917
2020-12-31  14.485599 -1.506260  12.979339
2021-12-31  26.089170 -1.620194  24.468977
2022-12-31  26.666150 -1.736659  24.929491
2023-12-31 -13.934901 -1.355026 -15.289926
2024-12-31  -1.412704 -0.254365  -1.667069
This is annual average return and costs
8.058884499276603
-1.1379828021792038
6.9209016970974

Total Return      Sharpe  CAGR    Max Drawdown
--------------  --------  ------  --------------
83.36%              0.37  5.55%   -51.83%


Total Return      Sharpe  CAGR    Max Drawdown
--------------  --------  ------  --------------
63.09%              0.29  4.07%   -49.85%

DB
              Gross     Costs        Net
2013-12-31   0.805453  0.000000   0.805453
2014-12-31  32.946219 -1.441686  31.504533
2015-12-31  50.394365 -1.269489  49.124876
2016-12-31 -14.746860 -1.318935 -16.065794
2017-12-31  -5.571092 -1.007490  -6.578582
2018-12-31   2.789566 -1.028714   1.760852
2019-12-31 -15.518965 -0.989369 -16.508334
2020-12-31  13.419844 -1.464531  11.955313
2021-12-31  30.649724 -1.659034  28.990691
2022-12-31  27.077941 -1.708257  25.369684
2023-12-31  -8.930448 -1.303943 -10.234391
2024-12-31  -5.460004 -1.137335  -6.597338
2025-12-31 -13.922166 -0.306116 -14.228282
This is annual average return and costs
7.225659848962722
-1.1257613663616541
6.099898482601067


"""