import pandas as pd
import matplotlib.pyplot as plt

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# ====== DATA SOURCE ======
# data = csvFuturesSimData()
data = dbFuturesSimData()


# ====== CONFIG FILES ======
CONFIG1 = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/example/global_bo.yaml")
CONFIG2 = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/example/global_carry.yaml")


# ====== BUILD SYSTEMS ======
s1 = futures_system(config=CONFIG1, data=data)
s2 = futures_system(config=CONFIG2, data=data)

# ====== LABEL NAMES ======
s1_name = "Global"
s2_name = "Equally Weighted"


def stats_to_series(stats_obj):
    """Convert percent.stats() output to pandas Series"""

    tuples_list = stats_obj[0]  # only first element contains stats
    d = {k: float(v) for k, v in tuples_list}
    return pd.Series(d)


if __name__ == '__main__':

    # ==============================
    # 1) SUMMARY STATS COMPARISON
    # ==============================
    raw_stats1 = s1.accounts.portfolio().percent.stats()
    raw_stats2 = s2.accounts.portfolio().percent.stats()

    stats1 = stats_to_series(raw_stats1)
    stats2 = stats_to_series(raw_stats2)

    comparison_table = pd.concat(
        {
            s1_name: stats1,
            s2_name: stats2
        },
        axis=1
    )

    print("\n==== PERFORMANCE STATISTICS COMPARISON ====\n")
    print(comparison_table)

    # ==============================
    # 2) PERFORMANCE CURVE COMPARISON
    # ==============================
    curve1 = s1.accounts.portfolio_with_multiplier().net.percent.curve()
    curve2 = s2.accounts.portfolio_with_multiplier().net.percent.curve()

    plt.figure(figsize=(11, 6))
    plt.plot(curve1, label=s1_name)
    plt.plot(curve2, label=s2_name)
    plt.title("Net % Performance Comparison")
    plt.xlabel("Date")
    plt.ylabel("Net %")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==============================
    # 3) DRAWDOWN SERIES COMPARISON
    # ==============================
    dd1 = s1.accounts.portfolio().percent.drawdown()
    dd2 = s2.accounts.portfolio().percent.drawdown()

    dd_table = pd.DataFrame({
        f"{s1_name} MaxDD": [dd1.min()],
        f"{s2_name} MaxDD": [dd2.min()],
        f"{s1_name} AvgDD": [dd1.mean()],
        f"{s2_name} AvgDD": [dd2.mean()],
    })

    print("\n==== DRAWDOWN STATISTICS ====\n")
    print(dd_table)

    # ==============================
    # 4) DRAWDOWN CURVE PLOT
    # ==============================
    plt.figure(figsize=(11, 6))
    plt.plot(dd1, label=f"{s1_name} Drawdown")
    plt.plot(dd2, label=f"{s2_name} Drawdown")
    plt.title("Portfolio Drawdown (%)")
    plt.xlabel("Date")
    plt.ylabel("Drawdown %")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
