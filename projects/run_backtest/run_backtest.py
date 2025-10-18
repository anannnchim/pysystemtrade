import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


data = csvFuturesSimData()
# data = dbFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/diversified.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v3.yaml")

s = futures_system(config=config, data=data)


if __name__ == '__main__':

    input("1. System Performance")
    s.accounts.portfolio().net.percent.curve().plot(title="System Net % Performance")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.grid(True);
    plt.tight_layout()
    plt.show()

    drawdowns = s.accounts.portfolio().percent.drawdown()
    print("Drawdown Series:")
    print(drawdowns)
    print(f"Average drawdown: {drawdowns.mean():.2f}%")
    drawdowns.plot(title="Portfolio Drawdown (%)", ylabel="Drawdown")
    plt.show()

    input("Performance based on market")
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

    # Rolling 2-M realised risk
    input("Rolling 2 month realised Risk")
    a = s.accounts.portfolio().percent.rolling_ann_std()
    print(a)
    a.plot(title="Rolling 2M Realised Risk")
    plt.show()
    print("Avg. 2M Risk: ", a.mean()[0])

    input("Portfolio Risk (1M)")
    a = s.portfolio.get_portfolio_risk_for_original_positions()*100  # Annual port risk include correlation, 0 if 1 instrument
    print(a)
    a.plot(title="Portfolio Risk (1M)")
    plt.show()
    print("Avg. Port Risk: ", a.mean())

    input("Absolute Sum Risk")
    a = s.portfolio.get_sum_annualised_risk_for_original_positions()
    print(a)
    a.plot(title="Abs sum Risk")
    plt.show()
    print("Avg. Abs sum Risk ", a.mean())


    input("2. This is stats in percentage.")
    print(s.accounts.portfolio().percent.stats())

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

    input("4. This is Annual data table")
    df = pd.DataFrame({
        "Gross": s.accounts.portfolio().gross.annual.percent,
        "Costs": s.accounts.portfolio().costs.annual.percent,
        "Net": s.accounts.portfolio().net.annual.percent
    }); print(df)

    input("5. This is annual average return and costs")
    print(df['Gross'].mean())
    print(df['Costs'].mean())
    print(df['Net'].mean())

    input("6. This is % cummulative return")
    df = pd.DataFrame({
        "Gross": s.accounts.portfolio().gross.percent.curve(),
        "Net": s.accounts.portfolio().net.percent.curve(),
    }); print(df)
    df.plot()
    plt.show()

    input("7. Check if it's too safe to trade: vol < 5%?")
    for instrument in s.get_instrument_list():
        average_annual_risk = s.rawdata.get_daily_percentage_volatility(instrument).mean() * 16
        print(instrument, ": ", round(average_annual_risk, 4))
    print(s.portfolio.get_stdev_df())

    a = input("8. Check expensive instrument: Cost > 0.01")
    for instrument in s.get_instrument_list():
        print(instrument,": ", round(s.accounts.get_SR_cost_per_trade_for_instrument(instrument),4))
        if s.accounts.get_SR_cost_per_trade_for_instrument(instrument) > 0.01:
            print("Too expensive. Remove")
        else:
            print(instrument, " PASS")

    a = input("9. Check cheap enough to trade: Cost in SR < 0.13")
    for instrument in s.get_instrument_list():
        print(s.combForecast.cheap_trading_rules_post_processing(instrument))

    input("10. This is allocation")
    print(s.portfolio.get_instrument_weights())

    input("12. This is example of buffered position.")
    for instrument in s.get_instrument_list():
        s.accounts.get_buffered_position(instrument).plot()
    plt.show()
    for instrument in s.get_instrument_list():
        print(s.accounts.get_buffered_position(instrument))

    input("13. Compare return of Fix vs compound")
    df = pd.DataFrame({
        "Fixed": s.accounts.portfolio().net.percent.curve(),
        "Compound": s.accounts.portfolio_with_multiplier().net.percent.curve()
    }); print(df)
    df.plot()
    plt.show()

    input("IDM")
    a = s.portfolio.get_instrument_diversification_multiplier() # Estimated IDM
    print(a)
    a.plot()
    plt.show()
    print("Avg. IDM: ", a.mean())


    input("Different way of getting return. But it pretty much the same.")
    df = pd.DataFrame({
        "NotionalCap": s.accounts.get_notional_capital(),
        "ActualCap": s.accounts.get_actual_capital(),
        "Portfolio": s.accounts.portfolio(),
        "PortfolioMulti": s.accounts.portfolio_with_multiplier(),
        "PortfolioPer": s.accounts.portfolio().percent,
        "PortfolioMultiPer": s.accounts.portfolio_with_multiplier().percent
    }); print(df)

    input("Generate daily_returns.csv for generating report")
    daily_returns = s.accounts.portfolio().percent/100
    daily_returns = pd.DataFrame({
        "Index": daily_returns.index,
        "Return": daily_returns.values
    })
    daily_returns.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/daily_returns.csv", index=False)
