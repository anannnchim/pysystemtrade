import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems import rawdata
from systems.provided.futures_chapter15.basesystem import futures_system
import pandas as pd

# INPUT: Select data and system
data = csvFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/system_f1_new_config.yaml")

s = futures_system(config=config, data=data)

if __name__ == '__main__':


    # 1. Check pnl for each instrument
    plt.figure(figsize=(12, 6))  # Optional: Set the chart size

    for instr in s.get_instrument_list():
        curve = s.accounts.pandl_for_instrument(instr).percent.curve()
        plt.plot(curve, label=instr)

    plt.title("P&L Percentage Curve by Instrument")
    plt.xlabel("Date")
    plt.ylabel("P&L %")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # 2. Get Annualised risk
    input("2.Check annualised risk")
    for instrument in s.get_instrument_list():
        average_annual_risk = s.rawdata.get_daily_percentage_volatility(instrument).mean() * 16
        print("---")
        print(instrument, ": ", round(average_annual_risk, 4))
        if average_annual_risk < 5 :
            print("Too safe to trade. Remove")
        else:
            print(instrument, " PASS")


    # 3. Get costs data
    costs = {}
    for instrument in s.get_instrument_list():
        print(instrument + ": ", s.rawdata.get_raw_cost_data(instrument))

        costs[instrument] = {
            'Multiplier': s.rawdata.get_value_of_block_price_move(instrument),
            'roll_per_year': s.rawdata.rolls_per_year(instrument),
            'SR_cost_per_trade': s.accounts.get_SR_cost_per_trade_for_instrument(instrument),
            'SR_holding_cost_only': s.accounts.get_SR_holding_cost_only(instrument)
        }

    df = pd.DataFrame.from_dict(costs, orient='index')
    print(df)

    # 4. Get risk
    print(s.portfolio.get_stdev_df()*100)

    s.accounts.get_SR_cost_given_turnover("S50", 5)
