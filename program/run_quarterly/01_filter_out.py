from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/private_config.yaml")

s = futures_system(config=config, data=data)

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

"""
1. Check Cost in Sharpe ( Need to < 0.01 ) and cheap rules
2. Remove too low vol
3. Check Avg. position & Buffered position
"""
if __name__ == '__main__':

    instruments = s.get_instrument_list()

    # ──────────────────────────────────────────────────────────────────────────────
    # Note 1) Cost in Sharpe per instrument
    # ──────────────────────────────────────────────────────────────────────────────

    input("1. Check each instrument if it's Expensive: Cost > 0.01")
    rows = []
    for instr in instruments:
        cost = round(s.accounts.get_SR_cost_per_trade_for_instrument(instr), 4)
        status = "Remove (Too expensive)" if cost > 0.01 else "PASS"
        rows.append({
            "Instrument": instr,
            "SR Cost/Trade": cost,
            "Rule": "Cost > 0.01",
            "Status": status
        })
    cost_df = pd.DataFrame(rows).sort_values("SR Cost/Trade", ascending=False)
    print(cost_df.to_string(index=False))

    # ──────────────────────────────────────────────────────────────────────────────
    # Extra table: SR cost per trade, rolls per year, SR holding cost only
    # ──────────────────────────────────────────────────────────────────────────────

    input("\n2. Show cost, turnover, and holding-cost (SR terms) per instrument")
    rows_detail = []
    for instr in instruments:
        sr_cost_trade = s.accounts.get_SR_cost_per_trade_for_instrument(instr)
        rolls_year = s.rawdata.rolls_per_year(instr)
        sr_holding_cost = s.accounts.get_SR_holding_cost_only(instr)

        rows_detail.append({
            "Instrument": instr,
            "SR Cost/Trade": round(sr_cost_trade, 4),
            "Rolls/Year": round(rolls_year, 2),
            "SR Holding Cost Only": round(sr_holding_cost, 4)
        })

    detail_df = pd.DataFrame(rows_detail).sort_values("SR Cost/Trade", ascending=False)
    print(detail_df.to_string(index=False))
    # ──────────────────────────────────────────────────────────────────────────────
    # Note 1.1) Cheap trading rules post-processing (table)
    # ──────────────────────────────────────────────────────────────────────────────

    input("1.1 Check each rule if it's cheap enough to trade: Cost in SR < 0.15")

    def stringify_rules(x):
        if x is None:
            return ""
        if isinstance(x, (list, tuple, set)):
            return ", ".join(map(str, x))
        if isinstance(x, dict):
            try:
                true_keys = [k for k, v in x.items() if v]
                if true_keys:
                    return ", ".join(map(str, true_keys))
            except Exception:
                pass
            return ", ".join(f"{k}:{v}" for k, v in x.items())
        return str(x)

    rule_rows = []
    for instr in instruments:
        rules = s.combForecast.cheap_trading_rules_post_processing(instr)
        rule_rows.append({"Instrument": instr, "Cheap Rules (<0.15 SR cost)": stringify_rules(rules)})
    rules_df = pd.DataFrame(rule_rows)
    print(rules_df.to_string(index=False))

    # ──────────────────────────────────────────────────────────────────────────────
    # Note 2) Too safe to trade? annualized vol < 5%
    # ──────────────────────────────────────────────────────────────────────────────

    input("2. Check if it's too safe to trade: vol < 5%?")
    risk_rows = []
    for instr in instruments:
        avg_ann_vol = float(s.rawdata.get_daily_percentage_volatility(instr).mean() * 16)  # your factor
        status = "Remove (Too safe)" if avg_ann_vol < 5 else "PASS"
        risk_rows.append({
            "Instrument": instr,
            "Avg Annualized Vol (%)": round(avg_ann_vol, 4),
            "Rule": "Vol < 5%",
            "Status": status
        })
    risk_df = pd.DataFrame(risk_rows).sort_values("Avg Annualized Vol (%)")
    print(risk_df.to_string(index=False))

    # ──────────────────────────────────────────────────────────────────────────────
    # Note 3) Avg position (|avg| > 1.5) + last-N per-instrument plots
    # ──────────────────────────────────────────────────────────────────────────────
    input("3. Check average position: should be > abs(1.5) (It's compounded number)")
    LAST_N_ROWS = 512  # adjust as needed

    pos_rows = []

    for instr in instruments:
        vol_scalar = s.positionSize.get_average_position_at_subsystem_level(instr)  # vol_scalar =  target vol / instru vol
        IDM = s.portfolio.get_instrument_diversification_multiplier()
        weight = s.portfolio.get_instrument_weights()[instr]

        ser = vol_scalar * IDM * weight

        if ser is None or ser.empty:
            pos_rows.append({
                "Instrument": instr,
                "Avg Notional (signed)": None,
                "Avg |Notional|": None,
                "Last Notional": None,
                "Rule": "|avg| > 1.5",
                "Status": "N/A"
            })
            print(f"[skip] No notional series for {instr}")
            continue

        ser = ser.sort_index()  # ensure chronological

        # Metrics
        avg_signed = float(ser.mean())
        avg_abs = float(ser.abs().mean())
        last_val = float(ser.dropna().iloc[-1]) if not ser.dropna().empty else float("nan")
        status = "OK" if avg_abs > 1.5 else "Low"

        pos_rows.append({
            "Instrument": instr,
            "Avg Notional (signed)": round(avg_signed, 4),
            "Avg |Notional|": round(avg_abs, 4),
            "Last Notional": None if pd.isna(last_val) else round(last_val, 4),
            "Rule": "|avg| > 1.5",
            "Status": status
        })

        # ── Plot per instrument (last N rows)
        ser_lastN = ser.tail(LAST_N_ROWS)
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(ser_lastN.index, ser_lastN.values, label=instr)
        ax.set_title(f"{instr} — Avg Position (last {len(ser_lastN)} rows)")
        ax.set_ylabel("Notional Position")
        ax.set_xlabel("Date")
        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(fontsize=9)
        plt.tight_layout()
        plt.show()

    # Table
    notional_pos_df = pd.DataFrame(pos_rows).sort_values("Avg |Notional|", ascending=False, na_position="last")
    print(notional_pos_df.to_string(index=False))

    # ──────────────────────────────────────────────────────────────────────────────
    # Note 3.1) Buffered positions over time — (Should not be all 0)
    # ──────────────────────────────────────────────────────────────────────────────
    series = []
    for instr in instruments:
        ser_buf = s.accounts.get_buffered_position(instr)
        if ser_buf is not None:
            series.append(ser_buf.rename(instr))

    input("3.1 Show buffered positions over time (table + plot)")
    LAST_N_ROWS = 512

    if series:
        pos_ts_df = pd.concat(series, axis=1).sort_index().fillna(0)
        pos_print = pos_ts_df.reindex(columns=instruments).tail(LAST_N_ROWS).round(2)
        print(f"\nBuffered Positions (last {len(pos_print)} rows):")
        print(pos_print.to_string())

        ax = pos_print.plot(
            title=f"Buffered Positions by Instrument (last {len(pos_print)} rows)",
            ylabel="Contracts",
            legend=True,
            figsize=(12, 6)
        )
        locator2 = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator2)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator2))
        ax.legend(ncol=min(3, len(instruments)), fontsize=8)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()
    else:
        print("[info] No position data to show for buffered positions over time.")


