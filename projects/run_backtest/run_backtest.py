import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# INPUT: Select data and system
# data = csvFuturesSimData()
data = dbFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_02_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_02_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/single_config.yaml")

s = futures_system(config=config, data=data)


if __name__ == '__main__':

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
Risk 20%
Gross: 17.133985029443885
Cost: -1.4295124216953727
Net: 15.70447260774851
RollRisk: 19.86 

2012-12-31   8.936000 -1.536773   7.399227
2013-12-31  12.363500 -1.796817  10.566683
2014-12-31  30.646500 -1.692322  28.954178
2015-12-31  26.988000 -1.430961  25.557039
2016-12-31  -5.326000 -1.529265  -6.855265
2017-12-31  35.197500 -1.516347  33.681153
2018-12-31 -19.422015 -1.456617 -20.878631
2019-12-31 -23.877534 -1.129593 -25.007127
2020-12-31  22.748861 -1.806485  20.942376
2021-12-31  21.462388 -1.670757  19.791630
2022-12-31  17.251255 -2.001121  15.250134
2023-12-31 -10.079890 -1.987627 -12.067517
2024-12-31   3.889012 -0.457183   3.431828

"""