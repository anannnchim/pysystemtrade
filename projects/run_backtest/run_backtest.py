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
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/diversified_program_config.yaml")

s = futures_system(config=config, data=data)


if __name__ == '__main__':

    a = input("Check cheap enough to trade")
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
