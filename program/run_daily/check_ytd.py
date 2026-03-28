from sysdata.config.configdata import Config
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import pandas as pd


data = dbFuturesSimData()

config = Config("/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026.yaml")
s = futures_system(config=config, data=data)


# === NEW: TWR FUNCTION ===
def compute_twr_curve(perc_return, start_date, end_date=None):
    r = perc_return.loc[start_date:end_date] / 100.0
    twr_curve = (1 + r).cumprod()
    twr_pct = (twr_curve - 1) * 100
    return twr_pct


def compute_twr_value(perc_return, start_date, end_date=None):
    r = perc_return.loc[start_date:end_date] / 100.0
    twr = (1 + r).prod() - 1
    return twr * 100


start_date = "2026-01-01"   # 🔥 change this anytime


if __name__ == '__main__':

    # === ORIGINAL ===
    input("0. This is stats in percentage.")
    print(s.accounts.portfolio().percent.stats())


    # === CHANGE 1: SYSTEM PERFORMANCE (TWR instead of raw %) ===
    input("1. System Performance (TWR)")

    perc_return = s.accounts.portfolio_with_multiplier().net.percent

    end_date = None             # optional

    twr_pct = compute_twr_curve(perc_return, start_date, end_date)
    twr_value = compute_twr_value(perc_return, start_date, end_date)

    print(f"TWR from {start_date}: {twr_value:.2f}%")

    twr_pct.plot(title=f"TWR (%) from {start_date}")
    plt.xlabel("Date")
    plt.ylabel("Return (%)")
    plt.axhline(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # === CHANGE 2: DRAWDOWN BASED ON TWR (more correct) ===
    input("2. Drawdown (TWR-based)")

    twr_curve = (twr_pct / 100) + 1
    running_max = twr_curve.cummax()
    drawdowns = (twr_curve / running_max - 1) * 100

    print("Drawdown Series:")
    print(drawdowns)
    print(f"Average drawdown: {drawdowns.mean():.2f}%")

    drawdowns.plot(title="Portfolio Drawdown (%)", ylabel="Drawdown")
    plt.show()


    # === ORIGINAL (kept) ===
    input("3. Performance based on market")

    plt.figure(figsize=(12, 6))
    for instr in s.get_instrument_list():
        curve = s.accounts.pandl_for_instrument(instr).percent.curve()
        plt.plot(curve, label=instr)

    plt.title("Performance by Instrument")
    plt.xlabel("Date")
    plt.ylabel("%")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()