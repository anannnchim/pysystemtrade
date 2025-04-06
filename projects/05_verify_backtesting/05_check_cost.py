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

    symbol = systemCSV.get_instrument_list()[0]  # we're using systemCSV below

    # Get gross and net cumulative P&L
    gross_curve = systemCSV.accounts.portfolio().gross.percent.curve()
    net_curve = systemCSV.accounts.portfolio().net.percent.curve()

    plt.figure(figsize=(14, 6))
    gross_curve.plot(label="Gross Return", ax=plt.gca())
    net_curve.plot(label="Net Return", ax=plt.gca())
    plt.ylabel("Cumulative P&L")
    plt.title(f"{symbol} - Gross vs Net Return (CSV)")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Combine and align
    df = pd.concat([
        gross_curve.rename("Gross Return"),
        net_curve.rename("Net Return")
    ], axis=1).dropna()

    # Plot again for comparison
    plt.figure(figsize=(14, 6))
    df.plot(ax=plt.gca())
    plt.title(f"{symbol} - Gross vs Net Return CSV (Aligned)")
    plt.ylabel("Cumulative P&L")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Print comparison stats
    print("Performance Summary:")
    print(f"Gross - Final Value: {df['Gross Return'].iloc[-1]:,.2f}, Std Dev: {df['Gross Return'].std():,.2f}")
    print(f"Net   - Final Value: {df['Net Return'].iloc[-1]:,.2f}, Std Dev: {df['Net Return'].std():,.2f}")

    first_common_date = df.index.min()
    print(f"First aligned P&L date: {first_common_date.date()}")
    print(f"Years of data before alignment: {(first_common_date - pd.to_datetime(start_date)).days / 365:.1f} years")


    # Check net return from different source
    net_curve_csv = systemCSV.accounts.portfolio().net.percent.curve()
    net_curve_db = systemDB.accounts.portfolio().net.percent.curve()

    plt.figure(figsize=(14, 6))
    net_curve_csv.plot(label="Net CSV", ax=plt.gca())
    net_curve_db.plot(label="Net DB", ax=plt.gca())
    plt.ylabel("Cumulative P&L")
    plt.title(f"{symbol} - Net Return CSV vs DB")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
