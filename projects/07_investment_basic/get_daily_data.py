from sysdata.sim.csv_futures_sim_data import csvFuturesSimData

instruments = ["BITCOIN", "SP500", "AUD"]
data = csvFuturesSimData()

if __name__ == '__main__':

    for instrument in instruments:
        price = data.daily_prices(instrument)
        print(price)
        price.to_csv(f"/Users/nanthawat/PycharmProjects/pysystemtrade/projects/07_investment_basic/{instrument}.csv")
