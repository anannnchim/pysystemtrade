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

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines


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
    config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/program/config.yaml")
)


if __name__ == '__main__':
    a = s.rawdata.daily_returns("CORN_mini")
    a = s. rawdata.get_daily_prices("CORN_mini")
    print(a)

    """
    
    2024-01-11    -1.000
2024-01-12    -8.750
2024-01-15       NaN
2024-01-16       NaN
2024-01-17    -1.875
2024-01-18     2.500



    2024-02-13     0.625
2024-02-14    -6.750
2024-02-15    -6.750
2024-02-16    -1.125
2024-02-19       NaN
2024-02-20       NaN
2024-02-21    -8.375
2024-02-22    -3.875
2024-02-23    -6.750
    """

