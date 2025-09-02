import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/new_config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/single_config.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/static_three.yaml")

s = futures_system(config=config, data=data)


if __name__ == '__main__':


    # Note: Performance

    input("1. System Performance")
    s.accounts.portfolio().net.percent.curve().plot(title="System Net % Performance")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.grid(True);
    plt.tight_layout()
    plt.show()

    # Drawdown
    drawdowns = s.accounts.portfolio().percent.drawdown()
    print("Drawdown Series:")
    print(drawdowns)
    print(f"Average drawdown: {drawdowns.mean():.2f}%")
    drawdowns.plot(title="Portfolio Drawdown (%)", ylabel="Drawdown")
    plt.show()



    # Note: Check liquidity

    # Note: Check Cost
    a = input("1. Check each instrument if it's Expensive: Cost > 0.01")
    for instrument in s.get_instrument_list():
        print(instrument, ": ", round(s.accounts.get_SR_cost_per_trade_for_instrument(instrument), 4))
        if s.accounts.get_SR_cost_per_trade_for_instrument(instrument) > 0.01:
            print("Too expensive. Remove")
        else:
            print(instrument, " PASS")

    a = input("2. Check each rule if it's cheap enough to trade: Cost in SR < 0.13")
    for instrument in s.get_instrument_list():
        print(s.combForecast.cheap_trading_rules_post_processing(instrument))

    # Note: Check Too low risk
    input("3. Chekc if it's too safe to trade: vol < 5%?")
    for instrument in s.get_instrument_list():
        average_annual_risk = s.rawdata.get_daily_percentage_volatility(instrument).mean() * 16
        print("---")
        print(instrument, ": ", round(average_annual_risk, 4))
        if average_annual_risk < 5 :
            print("Too safe to trade. Remove")
        else:
            print(instrument, " PASS")

    # Note. Check position
    input("4. Check average position: should be > 2 (It's compounded number)")
    vol_scalar = {}
    for instrument in s.get_instrument_list():
        vol_scalar[instrument] = s.positionSize.get_average_position_at_subsystem_level(instrument).mean()
        vol_scalar_df = pd.DataFrame([vol_scalar])
    print(vol_scalar_df)



    # Plot separately
    # Poisition
    # for instru in s.get_instrument_list():
    #     s.accounts.get_buffered_position(instru).plot()
    #     plt.show()

    series = []
    for instr in s.get_instrument_list():
        ser = s.accounts.get_buffered_position(instr).rename(instr)  # make column name = instrument
        series.append(ser)

    df = pd.concat(series, axis=1).fillna(0)  # align on index, fill gaps with 0
    ax = df.plot(title="Buffered Positions by Instrument", ylabel="Contracts", legend=True, figsize=(12, 6))
    ax.legend(ncol=3, fontsize=8)
    plt.tight_layout()
    plt.show()


    # Final position
    input("This is final position: position shouldn't be 0")
    positions = {}
    for instrument in s.get_instrument_list():
        positions[instrument] = s.accounts.get_buffered_position(instrument)
    df = pd.DataFrame(positions)
    print(df)



    input("2. Stats")
    print(s.accounts.portfolio().percent.stats())


    input("2.1 RISK")
    # Note: 1. Realised risk: 2 month rolling for plotting
    a = s.accounts.portfolio().percent.rolling_ann_std()
    print(a)
    a.plot()
    plt.show()
    print(a.mean())

    # FIXME: Check with longterm data, which is which
    # NOTE: RISK ---
    # Note: 2. Static Current Annualised Risk:  8.833470
    a = s.portfolio.get_portfolio_risk_for_original_positions()*100  # Annual port risk include correlation, 0 if 1 instrument
    print(a)
    a.plot()
    plt.show()
    print(a.mean())

    # Note: 2. Abs sum risk, with no correlation & IDM": 24% (similar to EWMA)
    # With IDM, this will be around portfolio risk.
    a = s.portfolio.get_sum_annualised_risk_for_original_positions()
    print(a)
    a.plot()
    plt.show()
    print(a.mean())

    # IDM
    a = s.portfolio.get_instrument_diversification_multiplier() # Estimated IDM
    print(a)
    a.plot()
    plt.show()
    print(a.mean())

    # Correlation
    correlation = s.portfolio.get_instrument_correlation_matrix().corr_list[-1]
    print(correlation)

    input("3. Performance based on market")
    plt.figure(figsize=(12, 6))
    for instr in s.get_instrument_list():
        curve = s.accounts.pandl_for_instrument(instr).percent.curve()
        plt.plot(curve, label=instr)

    plt.title("Performance by Instrument")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


