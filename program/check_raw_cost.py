from sysdata.sim.csv_futures_sim_data import csvFuturesSimData

if __name__ == '__main__':
    data = csvFuturesSimData()

    print(data.get_raw_cost_data("USD"))
