from sysdata.config.configdata import Config
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.accounts.accounts_stage import Account
from systems.basesystem import System
from systems.forecast_combine import ForecastCombine
from systems.forecast_scale_cap import ForecastScaleCap
from systems.forecasting import Rules
from systems.portfolio import Portfolios
from systems.positionsizing import PositionSizing
from systems.rawdata import RawData
import matplotlib.pyplot as plt


data = dbFuturesSimData()
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
    config=Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/strategy_1/config.yaml")
)

if __name__ == '__main__':

    code = "CORN_mini"

    # Note 1 - Instrument data
    s.rawdata.get_daily_prices(code)
    s.rawdata.annualised_returns_volatility(code)
    s.rawdata.get_daily_percentage_volatility(code)
    a = s.rawdata.daily_returns_volatility(code) # 4.547


    # Note 2 - System data
    avg_position = s.positionSize.get_average_position_at_subsystem_level(code)
    print(avg_position)



    """
    Check the system component and verify.
    
    
    Ref
    /Users/nanthawat/PycharmProjects/AnanCapitalFund/src/program/system_f1/livetest/run_multiple.py
    /Users/nanthawat/PycharmProjects/AnanCapitalFund/src/program/system_f1/backtest/single_level/run_single.py
    /Users/nanthawat/PycharmProjects/AnanCapitalFund/src/program/system_f1/backtest/portfolio_level/run_multiple.py
    """


