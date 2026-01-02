"""
This script is responsible for
- plotting risk overlay value overtime
- get the 99% percentile and put it in config before production.
"""

import pandas as pd
from matplotlib import pyplot as plt
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
from systems.risk_overlay import get_risk_multiplier

# CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/diversified/config_bo.yaml"
config = Config(CONFIG_PATH)
data = csvFuturesSimData()
# data = dbFuturesSimData()

s = futures_system(config=config, data=data)

if __name__ == '__main__':

    # 1. 99 percentile of Risk overlay
    normal_risk = s.portfolio.get_portfolio_risk_for_original_positions() * 100
    shocked_vol_risk = (
        s.portfolio.get_portfolio_risk_for_original_positions_with_shocked_vol() * 100
    )
    sum_abs_risk = (
        s.portfolio.get_sum_annualised_risk_for_original_positions() * 100
    )
    leverage = s.portfolio.get_leverage_for_original_position()

    # ---- 99th percentile + print as DataFrame ----

    metrics = {
        "Normal risk": normal_risk,
        "Shocked vol risk": shocked_vol_risk,
        "Sum abs risk": sum_abs_risk,
        "Leverage": leverage,
    }

    rows = []
    for name, series in metrics.items():
        # Ensure we are working with a Series (in case any comes back as 1-col DataFrame)
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]
        p99 = series.quantile(0.99)
        rows.append((name, p99))

    p99_df = pd.DataFrame(rows, columns=["metric", "p99"])
    p99_df["p99"] = p99_df["p99"].round(2)

    # get risk target
    percentage_vol_target = s.config.get_element("percentage_vol_target")

    # add suggested threshold column: p99 / risk_target, except for leverage
    def compute_suggested_threshold(row):
        if row["metric"] == "Leverage":
            return None
        # divide by risk target to get suggested config threshold
        return round(row["p99"] / percentage_vol_target, 2)

    p99_df["suggested_risk_overlay_threshold"] = p99_df.apply(compute_suggested_threshold, axis=1)

    print("99th percentile of risk overlay metrics:")
    print(p99_df.to_string(index=False))

    # (Optional) quick plots of the series over time
    normal_risk.plot(title="Normal risk")
    plt.show()
    shocked_vol_risk.plot(title="Shocked vol risk")
    plt.show()
    sum_abs_risk.plot(title="Sum abs risk")
    plt.show()
    leverage.plot(title="Leverage")
    plt.show()
