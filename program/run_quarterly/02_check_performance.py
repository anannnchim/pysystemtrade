from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt

# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/new_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/single_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/static_three.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/AFTS_four.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v2.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/system_01/config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v2.yaml")

s = futures_system(config=config, data=data)

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

"""
1. Check stats
2. Equity curve
3. Drawdown
4. Performance based on market
"""

if __name__ == '__main__':

    # 1. Statistic
    stats_output = s.accounts.portfolio().percent.stats()
    metrics = stats_output[0]
    df = pd.DataFrame(metrics, columns=["Metric", "Value"])
    print(df.to_string(index=False))

    # 2. Equity curve
    s.accounts.portfolio().net.percent.curve().plot(title="System Net % Performance")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.grid(True);
    plt.tight_layout()
    plt.show()

    # 3. Equity curve
    drawdowns = s.accounts.portfolio().percent.drawdown()
    print("Drawdown Series:")
    print(drawdowns)
    print(f"Average drawdown: {drawdowns.mean():.2f}%")
    drawdowns.plot(title="Portfolio Drawdown (%)", ylabel="Drawdown")
    plt.show()

    # 4. Performance based on market
    instruments = s.get_instrument_list()

    plt.figure(figsize=(12, 6))
    for instr in instruments:
        curve = s.accounts.pandl_for_instrument(instr).percent.curve()
        plt.plot(curve, label=instr)

    plt.title("Performance by Instrument", fontsize=14, fontweight="bold")
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Return (%)", fontsize=12)
    plt.legend(loc="best", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    for instr in instruments:
        # --- Fetch data
        perf = s.accounts.pandl_for_instrument(instr).percent.curve()  # % return series
        pos = s.accounts.get_buffered_position(instr)  # position series
        price_raw = data.daily_prices(instrument_code=instr)  # daily price

        # Ensure price is a Series
        if isinstance(price_raw, pd.DataFrame):
            price = price_raw.select_dtypes("number").iloc[:, 0]
        else:
            price = price_raw

        # Skip if no data
        if any(x is None for x in (perf, pos, price)):
            print(f"[skip] Missing series for {instr}")
            continue
        if len(perf) == 0 or len(pos) == 0 or len(price) == 0:
            print(f"[skip] Empty series for {instr}")
            continue

        # Align indexes (union of all three)
        common_index = perf.index.union(pos.index).union(price.index)
        perf = perf.reindex(common_index)
        pos = pos.reindex(common_index)
        price = price.reindex(common_index).ffill()  # ffill gaps for price

        # --- Create figure with 3 stacked plots
        fig, (ax_price, ax_perf, ax_pos) = plt.subplots(
            3, 1, figsize=(12, 10), sharex=True,
            gridspec_kw={"height_ratios": [2, 1.5, 1], "hspace": 0.12}
        )

        # Top: Price
        ax_price.plot(price.index, price.values, label="Price", color="tab:blue")
        ax_price.set_title(f"{instr} — Price, Performance, Position", fontsize=13, fontweight="bold")
        ax_price.set_ylabel("Price", fontsize=11)
        ax_price.grid(True, linestyle="--", alpha=0.6)
        ax_price.legend(loc="best", fontsize=9)

        # Middle: Performance (%)
        ax_perf.plot(perf.index, perf.values, label="Return (%)", color="tab:green")
        ax_perf.set_ylabel("Return (%)", fontsize=11)
        ax_perf.grid(True, linestyle="--", alpha=0.6)
        ax_perf.legend(loc="best", fontsize=9)

        # Bottom: Position
        ax_pos.plot(pos.index, pos.values, label="Position", color="tab:red")
        ax_pos.set_ylabel("Position", fontsize=11)
        ax_pos.set_xlabel("Date", fontsize=11)
        ax_pos.grid(True, linestyle="--", alpha=0.6)
        ax_pos.legend(loc="best", fontsize=9)

        # Nice date formatting
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        ax_pos.xaxis.set_major_locator(locator)
        ax_pos.xaxis.set_major_formatter(formatter)

        plt.tight_layout()
        plt.show()
