'''
There are two kind of risk: A. Realised Risk, B. Estimated Risk

A. Realised Risk

    1. Static LT Average risk value (Check performance, LT-average should be the same as risk target)
    - GG: STDEV(all daily return) * 16
    - Account curve Report: Annual Risk

    2. Rolling realised Risk (Check how risk vary overtime)
    - GG: 1M EMA variance

B. Estimated Risk

    1. Normal Risk
    - GG: Using normal_risk_by_IDM
    2. Jump Risk
    3. Correlation Risk
    4. Leverage Risk

Report

    1. Account curve Report:
    - Annual Risk (Static realised risk)

    2. Strategy Report:
    - Normal risk (Normal Risk),
    - Shock Risk
    - Sum Abs risk (sum_abs_risk or risk with no IDM)
    - Leverage
    - Risk scalar

    3. Risk Report:
    - Annualised Risk (Normal Risk)
    - Margin
    - Sum abs notional exposure % capital (Gross exposure)
    - Sum abs risk
    - Net sum of risk
'''

import pandas as pd
from matplotlib import pyplot as plt
from program.googlesheet.update_system_gg import update_market_monitoring, update_portfolio_monitoring, \
    update_system_verification, update_system_diagnostic
from program.helper.run_scripts import run_scripts
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
from systems.risk_overlay import get_risk_multiplier

# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/diversified.yaml"
config = Config(CONFIG_PATH)
# data = csvFuturesSimData()
data = dbFuturesSimData()

s = futures_system(config=config, data=data)
N = 252
if __name__ == '__main__':
    # A) Realised Risk

    # 1. Static value: should be aligned with risk in stats()
    perc_daily_return = s.accounts.portfolio().percent
    print(f"LT-Risk (Risk Target): {perc_daily_return.std() * 16}")

    # 2. 2M-Rolling value: 2 Methods
    a = s.accounts.portfolio().percent.rolling_ann_std()  # 2 Month
    a.tail(N).plot(label="Rolling 2M Realised Risk")
    plt.legend()
    plt.show()

    # OR b = perc_daily_return.rolling(40).std() * 16 # 2 month

    # B) Estimated Risk (Risk overlay)
    normal_risk = s.portfolio.get_portfolio_risk_for_original_positions() * 100
    shocked_vol_risk = s.portfolio.get_portfolio_risk_for_original_positions_with_shocked_vol() * 100
    sum_abs_risk = s.portfolio.get_sum_annualised_risk_for_original_positions() * 100
    leverage = s.portfolio.get_leverage_for_original_position()

    # OR
    normal_risk_by_IDM = s.portfolio.get_sum_annualised_risk_for_original_positions() * 100 / 1.48

    print(f'Normal: {normal_risk.tail(1)}')
    print(f'shocked_vol_risk: {shocked_vol_risk.tail(1)}')
    print(f'sum_abs_risk: {sum_abs_risk.tail(1)}')
    print(f'leverage: {leverage.tail(1)}')
    print(f'normal_risk_by_IDM: {normal_risk_by_IDM.tail(1)}')

    # Plot each series separately (keeping your structure)
    normal_risk.tail(N).plot(label="Normal")
    plt.legend()
    plt.show()

    shocked_vol_risk.tail(N).plot(label="shocked_vol_risk")
    plt.legend()
    plt.show()

    sum_abs_risk.tail(N).plot(label="sum_abs_risk")
    plt.legend()
    plt.show()

    leverage.tail(N).plot(label="leverage")
    plt.legend()
    plt.show()

    normal_risk_by_IDM.tail(N).plot(label="normal_risk_by_IDM")
    plt.legend()
    plt.show()

    # DO NOT TOUCH BELOW
    # # Additional: Risk multiplier
    # risk_overlay_config = s.portfolio.config.get_element("risk_overlay")
    # percentage_vol_target = s.portfolio.get_percentage_vol_target()
    #
    # risk_scalar = get_risk_multiplier(
    #     risk_overlay_config=risk_overlay_config,
    #     normal_risk=normal_risk,
    #     shocked_vol_risk=shocked_vol_risk,
    #     sum_abs_risk=sum_abs_risk,
    #     leverage=leverage,
    #     percentage_vol_target=percentage_vol_target,
    # )
    # s.portfolio.get_risk_scalar()