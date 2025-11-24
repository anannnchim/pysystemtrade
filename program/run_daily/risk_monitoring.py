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

# If you set N to None or comment this out, the helper will plot full series
# N = 252


def plot_maybe_tail(series, label=None, title=None):
    """
    Plot last N points if N is defined and not None, otherwise plot full series/DataFrame.
    Uses global N so you don't have to change each plot call.
    """
    try:
        n = N
    except NameError:
        n = None

    if n is not None:
        data = series.tail(n)
    else:
        data = series

    data.plot(label=label)
    if label is not None:
        plt.legend()
    if title is not None:
        plt.title(title)
    plt.show()


if __name__ == '__main__':

    risk_overlay_cfg = s.config.get_element("risk_overlay")
    percentage_vol_target = s.config.get_element("percentage_vol_target")

    ### A) GETTING DATA ------------------------------------------------------------------------

    # A) Realised Risk

    # 1. Static value: should be aligned with risk in stats()
    perc_daily_return = s.accounts.portfolio().percent

    # 2. 2M-Rolling value: 2 Methods
    rolling_2m_risk = s.accounts.portfolio().percent.rolling_ann_std()  # 2 Month
    rolling_2m_risk = rolling_2m_risk.rename(
        columns={rolling_2m_risk.columns[0]: "Rolling 2M Realised Risk"}
    )
    # OR b = perc_daily_return.rolling(40).std() * 16 # 2 month

    # B) Estimated Risk (Risk overlay)
    normal_risk = s.portfolio.get_portfolio_risk_for_original_positions() * 100
    shocked_vol_risk = (
        s.portfolio.get_portfolio_risk_for_original_positions_with_shocked_vol() * 100
    )
    sum_abs_risk = (
        s.portfolio.get_sum_annualised_risk_for_original_positions() * 100
    )
    leverage = s.portfolio.get_leverage_for_original_position()

    # OR
    normal_risk_by_IDM = (
        s.portfolio.get_sum_annualised_risk_for_original_positions()
        * 100
        / s.portfolio.get_instrument_diversification_multiplier()
    )

    # C) Risk scalar
    risk_scalar = s.portfolio.get_risk_scalar()

    # number of days where risk overlay is effective (scalar != 1)
    effective_days = (risk_scalar != 1).sum()
    total_days = risk_scalar.shape[0]
    effective_days = (risk_scalar != 1).sum()
    effective_pct = effective_days / total_days * 100



    ### STRUCTURE DATA ------------------------------------------------------------------------

    risk_table = pd.DataFrame(
        {
            "value": [
                normal_risk.iloc[-1],
                shocked_vol_risk.iloc[-1],
                sum_abs_risk.iloc[-1],
                leverage.iloc[-1],
                normal_risk_by_IDM.iloc[-1],
            ],
            "config_limit": [
                risk_overlay_cfg["max_risk_fraction_normal_risk"]
                * percentage_vol_target,  # Normal risk
                risk_overlay_cfg["max_risk_fraction_stdev_risk"]
                * percentage_vol_target,  # Shock vol risk
                risk_overlay_cfg["max_risk_limit_sum_abs_risk"]
                * percentage_vol_target,  # Sum abs risk
                risk_overlay_cfg["max_risk_leverage"],  # Leverage - limit
                None,  # Normal risk / IDM - none
            ],
        },
        index=[
            "Normal risk",
            "Shocked vol risk",
            "Sum abs risk",
            "Leverage",
            "Normal risk / IDM",
        ],
    )

    ### B) PRINTING ------------------------------------------------------------------------

    print("1. REALISED RISK --------------------")
    print(f"LT-Risk (Risk Target): {perc_daily_return.std() * 16}")
    print("\n")

    print("2. ESTIMATED RISK --------------------")
    print("\nRisk overlay check:")
    print(risk_table.to_string())
    print("\n")

    print("3. Risk scalar --------------------")
    print(risk_scalar.tail(1))
    print("\n")
    print(f"Total days                 : {total_days}")
    print(f"Effective days (scalar≠1)  : {effective_days}")
    print(f"Effective percentage       : {effective_pct:.2f}%")

    ### C) PLOTTING ------------------------------------------------------------------------

    # Realised risk
    plot_maybe_tail(
        rolling_2m_risk,
        title="Realised Risk: Rolling 2 months",
    )

    # Estimated risk components
    plot_maybe_tail(normal_risk, label="Normal", title="Estimated Risk: Normal")
    plot_maybe_tail(shocked_vol_risk, label="shocked_vol_risk", title="Estimated Risk: Shocked vol risk")
    plot_maybe_tail(sum_abs_risk, label="sum_abs_risk", title="Estimated Risk: Sum abs risk")
    plot_maybe_tail(leverage, label="leverage", title="Estimated Risk: Leverage")
    plot_maybe_tail(
        normal_risk_by_IDM,
        label="normal_risk_by_IDM",
        title="Estimated Risk: Normal risk / IDM",
    )

    # Risk scalar
    plot_maybe_tail(risk_scalar, label="Risk scalar", title="Risk scalar")
