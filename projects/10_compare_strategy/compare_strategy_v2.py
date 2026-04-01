import pandas as pd
import matplotlib.pyplot as plt

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# ====== DATA SOURCE ======
data = dbFuturesSimData()
# data = csvFuturesSimData()


# ====== STRATEGY DEFINITIONS ======
STRATEGIES = [
    ("Breakout",    "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026.yaml"),
    ("Carry",   "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-carry.yaml"),
    ("Comb", "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-comb.yaml"),
     ("Comb-all",  "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-comb-all.yaml"),

]

STRATEGIES = [
    ("LT",    "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-LT.yaml"),
    ("ST",   "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-ST.yaml"),
    ("AVG", "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-AVG.yaml"),
    ("Fitted", "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026.yaml"),

    #("Comb", "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-comb.yaml"),
   #  ("Comb-all",  "/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026-comb-all.yaml"),

]

# STRATEGIES = [
#     ("BO",    "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/example/global_bo.yaml"),
#     ("EMA",   "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/example/global_ema.yaml"),
#     # ("Carry", "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/example/global_carry.yaml"),
#     # ("Comb",  "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/example/global_comb.yaml"),
# ]


# ==============================
# HELPERS
# ==============================
def stats_to_series(stats_obj):
    """Convert percent.stats() output to pandas Series"""
    tuples_list = stats_obj[0]
    return pd.Series({k: float(v) for k, v in tuples_list})


def build_systems(strategies, data):
    systems = {}
    for name, path in strategies:
        cfg = Config(path)
        systems[name] = futures_system(config=cfg, data=data)
    return systems


def format_stats_table(df):
    """Make stats table human-readable"""

    pct_rows = {
        "min", "max", "median", "mean", "std",
        "ann_mean", "ann_std", "avg_drawdown", "time_in_drawdown"
    }

    ratio_rows = {"sharpe", "sortino", "calmar", "skew"}

    formatted = df.copy()

    for row in formatted.index:
        if row in pct_rows:
            formatted.loc[row] = formatted.loc[row].map(lambda x: f"{x:,.2f}%")
        elif row in ratio_rows:
            formatted.loc[row] = formatted.loc[row].map(lambda x: f"{x:.2f}")
        else:
            formatted.loc[row] = formatted.loc[row].map(lambda x: f"{x:,.0f}")

    return formatted


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":

    # 0) BUILD SYSTEMS
    systems = build_systems(STRATEGIES, data)

    # ==============================
    # 1) SUMMARY STATS COMPARISON
    # ==============================
    stats_table = {}

    for name, sys in systems.items():
        raw_stats = sys.accounts.portfolio().percent.stats()
        stats_table[name] = stats_to_series(raw_stats)

    comparison_table = pd.concat(stats_table, axis=1)
    comparison_table_fmt = format_stats_table(comparison_table)

    print("\n==== PERFORMANCE STATISTICS COMPARISON ====\n")
    print(comparison_table_fmt)

    # ==============================
    # 2) PERFORMANCE CURVE COMPARISON
    # ==============================
    plt.figure(figsize=(11, 6))

    for name, sys in systems.items():
        curve = sys.accounts.portfolio_with_multiplier().net.percent.curve()
        plt.plot(curve, label=name)

    plt.title("Net % Performance Comparison")
    plt.xlabel("Date")
    plt.ylabel("Net %")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==============================
    # 3) DRAWDOWN STATISTICS
    # ==============================
    dd_stats = {}

    for name, sys in systems.items():
        dd = sys.accounts.portfolio().percent.drawdown()
        dd_stats[name] = {
            "Max Drawdown (%)": f"{dd.min():,.2f}%",
            "Avg Drawdown (%)": f"{dd.mean():,.2f}%",
        }

    dd_table = pd.DataFrame(dd_stats).T

    print("\n==== DRAWDOWN STATISTICS ====\n")
    print(dd_table)

    # ==============================
    # 4) DRAWDOWN CURVE PLOT
    # ==============================
    plt.figure(figsize=(11, 6))

    for name, sys in systems.items():
        dd = sys.accounts.portfolio().percent.drawdown()
        plt.plot(dd, label=f"{name} Drawdown")

    plt.title("Portfolio Drawdown (%)")
    plt.xlabel("Date")
    plt.ylabel("Drawdown %")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
