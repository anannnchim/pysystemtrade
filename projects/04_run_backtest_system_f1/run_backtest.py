import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from systems.provided.futures_chapter15.basesystem import futures_system

data = csvFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/04_run_backtest_system_f1/config_backtest.yaml")

s = futures_system(config=config, data=data)


if __name__ == '__main__':

    # a = input("Check cheap enough to trade")
    # s.combForecast.cheap_trading_rules_post_processing(a)

    input("This is stats")
    print(s.accounts.portfolio().stats())

    input("This is cost")
    print(s.accounts.portfolio().costs.annual.percent)

    input("This is % cummulative return")
    print(s.accounts.portfolio().net.percent.curve())
    s.accounts.portfolio().net.percent.curve().plot()
    plt.show()

    # Report
    daily_returns = s.accounts.portfolio().percent/100
    daily_returns = pd.DataFrame({
        "Time": daily_returns.index,
        "returns": daily_returns.values
    })
    daily_returns.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/04_run_backtest_system_f1/daily_returns.csv", index=False)
