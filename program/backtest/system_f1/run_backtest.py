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
    config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/program/backtest/system_f1/config.yaml")
)


if __name__ == '__main__':


    input("This is stats")
    print(s.accounts.portfolio().stats())

    input("This is % cummulative return")
    print(s.accounts.portfolio().net.percent.curve())
    s.accounts.portfolio().net.percent.curve().plot()
    plt.show()

    input("This is cost")
    print(s.accounts.portfolio().costs.annual.percent)
