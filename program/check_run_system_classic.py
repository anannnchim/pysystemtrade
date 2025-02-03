from sysdata.config.configdata import Config
from sysdata.csv.csv_adjusted_prices import csvFuturesAdjustedPricesData
from sysdata.data_blob import dataBlob
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysproduction.strategy_code.run_system_classic import runSystemClassic, production_classic_futures_system
import pandas as pd

if __name__ == '__main__':

    config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")
    a = runSystemClassic(data = dataBlob([csvFuturesAdjustedPricesData]), strategy_name= "A",backtest_config_filename = config)

    s = a.system_method(534819)
    print(a.system_method(534819).get_instrument_list())


    """
    Objective
    1. Run system f1 in python environment
    2. Verify backtesting vs live trade  

    Process
    1. Update data source from googlesheet: update_data_gg.py
    2. Update new equity curve that we store in csv
    3. Generate backtest row using last equity 
    4. update googlesheet
    5. Reconcile and verify
    """




    c1 = "S50"
    df = pd.DataFrame({
        "Price": s.rawdata.get_daily_prices(c1),
        "Change": s.rawdata.daily_returns(c1),
        "InsRisk": s.positionSize.get_instrument_value_vol(c1),
        "NotionalCap": s.positionSize.get_notional_trading_capital(),
        "DailyRiskTarget": s.positionSize.get_daily_cash_vol_target(),
        "VolScalar": s.positionSize.get_average_position_at_subsystem_level(c1),
        "CombForecast": s.combForecast.get_combined_forecast(c1),
        "NotionalPosition": s.portfolio.get_notional_position(c1),
        "Upper": s.portfolio.get_buffers_for_position(c1).iloc[:, 0],
        "Lower": s.portfolio.get_buffers_for_position(c1).iloc[:, 1],

        "CAPMULTI": s.accounts.capital_multiplier(),
        "AC_CAP": s.accounts.get_actual_capital(),
        "AC_POS": s.accounts.get_actual_position(c1),
        "Return": s.accounts.portfolio()/s.accounts.get_actual_capital(),
        "PNL": s.accounts.portfolio()


    })
    df = df.tail(10)
    print(df)
