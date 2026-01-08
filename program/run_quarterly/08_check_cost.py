import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from sysproduction.reporting.report_configs import slippage_report_config
from systems.provided.futures_chapter15.basesystem import futures_system


data = csvFuturesSimData()
# data = dbFuturesSimData()


config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/temp/config_v1.yaml")
s = futures_system(config=config, data=data)

if __name__ == '__main__':


    instruments = s.get_instrument_list()
    # ──────────────────────────────────────────────────────────────────────────────
    # Note 1) Cost in Sharpe per instrument
    # ──────────────────────────────────────────────────────────────────────────────
    rows = []
    for instr in instruments:

        # Basic info
        last_price = s.rawdata.get_daily_prices(instr).iloc[-1]
        multiplier = s.rawdata.get_value_of_block_price_move(instr)
        value = last_price * multiplier

        risk = s.portfolio.get_stdev_df().iloc[-1, 0]
        comm_per_block = s.data.get_raw_cost_data(instr).value_of_block_commission
        slip_per_block = s.data.get_raw_cost_data(instr).price_slippage * multiplier
        cost_in_sharpe = round(s.accounts.get_SR_cost_per_trade_for_instrument(instr), 4)


        rolls_per_year = s.rawdata.rolls_per_year(instr)
        sr_holding_cost = s.accounts.get_SR_holding_cost_only(instr)
        turnover = s.accounts.forecast_turnover(instr, "ewmac64_256")
        sr_trading_cost = cost_in_sharpe * turnover
        total_sharpe_cost = sr_holding_cost + sr_trading_cost
        vol_target = s.config.get_element("percentage_vol_target")
        cost_perc = total_sharpe_cost * vol_target

        rows.append({
            "Instrument": instr,
            "Price" : last_price,
            "Multi" : multiplier,
            "Value" : value,
            "|": "|",
            "Annual.Risk": risk,
            "commPerBlock" : comm_per_block,
            "slipPerBlock" : slip_per_block,
            "SR Cost/Trade": cost_in_sharpe,
            "rollPerYear": rolls_per_year,
            "SR Holding": sr_holding_cost,
            "Turnover": turnover,
            "SR Trading" : sr_trading_cost,
            "Total SR in cost": total_sharpe_cost,
            "Cost (%)": cost_perc

        })

    cost_df = pd.DataFrame(rows).sort_values("SR Cost/Trade", ascending=False)
    input("1. Cost data ")
    print(cost_df.to_string(index=False))

    # Yearly number
    input("2. Perforamnce over time")
    df = pd.DataFrame({
        "Gross": s.accounts.portfolio().gross.annual.percent,
        "Costs": s.accounts.portfolio().costs.annual.percent,
        "Net": s.accounts.portfolio().net.annual.percent
    });
    print(df)
    print(df['Gross'].mean())
    print(df['Costs'].mean())
    print(df['Net'].mean())
