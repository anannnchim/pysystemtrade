import pandas as pd
from matplotlib import pyplot as plt
from private.systems.system_02.update_system_02_gg import start_date
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# Setup data sources
csv = csvFuturesSimData()
db = dbFuturesSimData()

# Load config and systems
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/05_verify_backtesting/single_config.yaml")
systemCSV = futures_system(config=config, data=csv)
systemDB = futures_system(config=config, data=db)

if __name__ == '__main__':

    symbol = systemCSV.get_instrument_list()[0]

    return_csv = systemCSV.accounts.portfolio().net.percent.curve()
    return_db = systemDB.accounts.portfolio().net.percent.curve()

    # Plot full range
    plt.figure(figsize=(14, 6))
    return_csv.plot(label="CSV Return", ax=plt.gca())
    return_db.plot(label="DB Return", ax=plt.gca())
    plt.title(f"{symbol} - Cumulative Return (Full Range)")
    plt.ylabel("Return")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Combine and align (drop NaNs)
    df = pd.concat([
        return_csv.rename("CSV Return"),
        return_db.rename("DB Return")
    ], axis=1).dropna()

    # Plot aligned range only
    plt.figure(figsize=(14, 6))
    df.plot(ax=plt.gca())
    plt.title(f"{symbol} - Cumulative Return (Aligned Period)")
    plt.ylabel("Return")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Compare system summary stat
    print(systemCSV.accounts.portfolio().percent.stats())
    print(systemDB.accounts.portfolio().percent.stats())


    # Get daily returns (not cumulative)
    return_csv_daily = systemCSV.accounts.portfolio().percent
    return_db_daily = systemDB.accounts.portfolio().percent

    # Align daily returns
    df_daily = pd.concat([
        return_csv_daily.rename("CSV"),
        return_db_daily.rename("DB")
    ], axis=1).dropna()

    # Calculate statistics
    stats = pd.DataFrame({
        "Mean": df_daily.mean()*256,
        "Std Dev": df_daily.std()*16,
        "Sharpe Ratio": (df_daily.mean()*256) / (df_daily.std()*16)
    })

    # Print stats
    print("\nPerformance Statistics on Aligned Period:")
    print(stats.round(4))