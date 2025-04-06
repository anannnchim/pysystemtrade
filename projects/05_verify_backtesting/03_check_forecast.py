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
    # Choose symbol (assumes at least one is available)
    symbol = systemDB.get_instrument_list()[0]

    # Get forecasts
    forecast_db = systemDB.combForecast.get_combined_forecast(symbol)
    forecast_csv = systemCSV.combForecast.get_combined_forecast(symbol)

    print(forecast_db)
    print(forecast_csv)

    # Plot raw forecasts with legend
    plt.figure(figsize=(14, 6))
    forecast_db.plot(label="DB", ax=plt.gca())
    forecast_csv.plot(label="CSV", ax=plt.gca())
    plt.title(f"{symbol} - Raw Forecasts")
    plt.ylabel("Forecast Value")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Combine forecasts and drop NaNs for alignment
    df = pd.concat([
        forecast_db.rename("Forecast DB"),
        forecast_csv.rename("Forecast CSV")
    ], axis=1).dropna()

    # Plot aligned forecasts
    plt.figure(figsize=(14, 6))
    df.plot(ax=plt.gca())
    plt.title(f"{symbol} - Forecast Comparison (DB vs CSV)")
    plt.ylabel("Forecast Value")
    plt.xlabel("Date")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Optional: Print how many years are needed before alignment
    first_common_date = df.index.min()
    print(f"First aligned forecast date: {first_common_date.date()}")
    print(
        f"Years of data needed before alignment: {(first_common_date - pd.to_datetime(start_date)).days / 365:.1f} years")
