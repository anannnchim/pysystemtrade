import pandas as pd
from matplotlib import pyplot as plt
from private.systems.system_02.update_system_02_gg import start_date
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# Setup data sources
db = dbFuturesSimData()
csv = csvFuturesSimData()

# Load config and systems
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/05_verify_backtesting/single_config.yaml")
systemDB = futures_system(config=config, data=db)
systemCSV = futures_system(config=config, data=csv)

if __name__ == '__main__':
    symbol = systemDB.get_instrument_list()[0]

    # Check gross return
    # perf_db = systemDB.accounts.portfolio().gross.percent.curve()
    # perf_csv = systemCSV.accounts.portfolio().gross.percent.curve()

    # Check net return
    perf_db = systemDB.accounts.portfolio().net.percent.curve()
    perf_csv = systemCSV.accounts.portfolio().net.percent.curve()

    # Plot raw forecasts with legend
    plt.figure(figsize=(14, 6))
    perf_db.plot(label="DB", ax=plt.gca())
    perf_csv.plot(label="CSV", ax=plt.gca())
    plt.title(f"{symbol} - Cummulative Return")
    plt.ylabel("Return")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Combine and align
    df = pd.concat([
        perf_db.rename("P&L DB"),
        perf_csv.rename("P&L CSV")
    ], axis=1).dropna()

    # Plot
    plt.figure(figsize=(14, 6))
    df.plot(ax=plt.gca())
    plt.title(f"{symbol} - Single Instrument Performance (DB vs CSV)")
    plt.ylabel("Cumulative P&L")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Print comparison stats
    print("Performance Summary:")
    print(f"DB - Final Value: {df['P&L DB'].iloc[-1]:,.2f}, Std Dev: {df['P&L DB'].std():,.2f}")
    print(f"CSV - Final Value: {df['P&L CSV'].iloc[-1]:,.2f}, Std Dev: {df['P&L CSV'].std():,.2f}")

    first_common_date = df.index.min()
    print(f"First aligned P&L date: {first_common_date.date()}")
    print(f"Years of data before alignment: {(first_common_date - pd.to_datetime(start_date)).days / 365:.1f} years")
