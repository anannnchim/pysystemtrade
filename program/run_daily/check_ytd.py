from sysdata.config.configdata import Config
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import pandas as pd


# === INIT SYSTEM ===
data = dbFuturesSimData()

config = Config("/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026.yaml")
s = futures_system(config=config, data=data)


# === TWR FUNCTIONS ===
def compute_twr_curve(perc_return, start_date, end_date=None):
    r = perc_return.loc[start_date:end_date] / 100.0
    twr_curve = (1 + r).cumprod()
    return (twr_curve - 1) * 100


def compute_twr_value(perc_return, start_date, end_date=None):
    r = perc_return.loc[start_date:end_date] / 100.0
    return ((1 + r).prod() - 1) * 100


def compute_yearly_twr(perc_return):
    r = perc_return / 100.0

    yearly_twr = (
        r.groupby(r.index.year)
         .apply(lambda x: (1 + x).prod() - 1)
         * 100
    )

    return yearly_twr


# === CONFIG ===
start_date = "2020-01-01"   # 🔥 change anytime
end_date = None             # optional


if __name__ == '__main__':

    # === 0. STATS ===
    input("0. This is stats in percentage.")
    print(s.accounts.portfolio().percent.stats())


    # === 1. SYSTEM PERFORMANCE (TWR) ===
    input("1. System Performance (TWR)")

    perc_return = s.accounts.portfolio_with_multiplier().net.percent

    # ensure Series (avoid double line issue)
    perc_return = perc_return.squeeze()

    # --- TWR (custom period) ---
    twr_pct = compute_twr_curve(perc_return, start_date, end_date)
    twr_value = compute_twr_value(perc_return, start_date, end_date)


    # --- PLOT TWR ---
    plt.figure()
    twr_pct.plot(title=f"TWR (%) from {start_date}", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Return (%)")
    plt.axhline(0)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # === 2. DRAWDOWN (TWR-BASED) ===
    input("2. Drawdown (TWR-based)")

    twr_curve = (twr_pct / 100) + 1
    running_max = twr_curve.cummax()
    drawdowns = (twr_curve / running_max - 1) * 100

    print("\nDrawdown Series:")
    print(drawdowns)
    print(f"\nAverage drawdown: {drawdowns.mean():.2f}%")

    plt.figure()
    drawdowns.plot(title="Portfolio Drawdown (%)", ylabel="Drawdown", color="red")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    # === 3. PERFORMANCE BY INSTRUMENT ===
    input("3. Performance based on market")

    plt.figure(figsize=(12, 6))

    for instr in s.get_instrument_list():
        curve = s.accounts.pandl_for_instrument(instr).percent.curve()
        curve = curve.squeeze()
        plt.plot(curve, label=instr)

    plt.title("Performance by Instrument")
    plt.xlabel("Date")
    plt.ylabel("%")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    from sysdata.config.configdata import Config
    import matplotlib.pyplot as plt
    from sysdata.sim.db_futures_sim_data import dbFuturesSimData
    from systems.provided.futures_chapter15.basesystem import futures_system
    import pandas as pd

    # === INIT SYSTEM ===
    data = dbFuturesSimData()

    config = Config("/home/anan/AnanProjects/pysystemtrade/private/systems/new/diversified/config-2-2026.yaml")
    s = futures_system(config=config, data=data)


    # === TWR FUNCTIONS ===
    def compute_twr_curve(perc_return, start_date, end_date=None):
        r = perc_return.loc[start_date:end_date] / 100.0
        twr_curve = (1 + r).cumprod()
        return (twr_curve - 1) * 100


    def compute_twr_value(perc_return, start_date, end_date=None):
        r = perc_return.loc[start_date:end_date] / 100.0
        return ((1 + r).prod() - 1) * 100


    def compute_yearly_twr(perc_return):
        r = perc_return / 100.0

        yearly_twr = (
                r.groupby(r.index.year)
                .apply(lambda x: (1 + x).prod() - 1)
                * 100
        )

        return yearly_twr


    if __name__ == '__main__':

        # === 0. STATS ===
        input("0. This is stats in percentage.")
        print(s.accounts.portfolio().percent.stats())

        # === 1. SYSTEM PERFORMANCE (TWR) ===
        input("1. System Performance (TWR)")

        perc_return = s.accounts.portfolio_with_multiplier().net.percent

        # --- ensure Series safely ---
        if isinstance(perc_return, pd.DataFrame):
            perc_return = perc_return.iloc[:, 0]

        # --- ensure datetime index ---
        if not isinstance(perc_return.index, pd.DatetimeIndex):
            perc_return.index = pd.to_datetime(perc_return.index)

        # --- TWR ---
        twr_pct = compute_twr_curve(perc_return, start_date, end_date)
        twr_value = compute_twr_value(perc_return, start_date, end_date)

        # --- PLOT ---
        plt.figure()
        twr_pct.plot(title=f"TWR (%) from {start_date}", color="blue")
        plt.xlabel("Date")
        plt.ylabel("Return (%)")
        plt.axhline(0)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # === 2. DRAWDOWN ===
        input("2. Drawdown (TWR-based)")

        twr_curve = (twr_pct / 100) + 1
        running_max = twr_curve.cummax()
        drawdowns = (twr_curve / running_max - 1) * 100

        print("\nDrawdown Series:")
        print(drawdowns)
        print(f"\nAverage drawdown: {drawdowns.mean():.2f}%")

        plt.figure()
        drawdowns.plot(title="Portfolio Drawdown (%)", ylabel="Drawdown", color="red")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # === 3. PERFORMANCE BY INSTRUMENT ===
        input("3. Performance based on market")

        plt.figure(figsize=(12, 6))

        for instr in s.get_instrument_list():
            curve = s.accounts.pandl_for_instrument(instr).percent.curve()

            if isinstance(curve, pd.DataFrame):
                curve = curve.iloc[:, 0]

            plt.plot(curve, label=instr)

        plt.title("Performance by Instrument")
        plt.xlabel("Date")
        plt.ylabel("%")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # === FINAL PRINT (AS YOU WANT) ===

        print("\n================ PERFORMANCE SUMMARY ================")

        # --- TWR ---
        print(f"\nTWR from {start_date}: {twr_value:.2f}%")

        # --- YEARLY TWR ---
        yearly_twr = compute_yearly_twr(perc_return)

        yearly_df = yearly_twr.to_frame(name="TWR (%)")
        yearly_df["TWR (%)"] = yearly_df["TWR (%)"].map(lambda x: f"{x:.2f}%")

        # --- TOTAL (since inception) ---
        first_date = perc_return.index.min().strftime("%Y-%m-%d")
        total_twr = compute_twr_value(perc_return, first_date)

        yearly_df.loc["Total"] = f"{total_twr:.2f}%"

        print("\n=== Yearly TWR (%) ===")
        print(yearly_df)
