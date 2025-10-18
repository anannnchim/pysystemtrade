import pandas as pd
import numpy as np
from datetime import date
import os

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


# === CONFIGURATION ===
data = csvFuturesSimData()
# data = dbFuturesSimData()
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/sytem_f1.yaml")

s = futures_system(config=config, data=data)


# === HELPER FUNCTION ===
def latest_scalar(x, prefer="last"):
    """Convert Series/DataFrame/scalar to a float scalar."""
    if np.isscalar(x):
        return float(x)
    if hasattr(x, "dropna") and hasattr(x, "iloc") and not hasattr(x, "columns"):
        ser = x.dropna()
        if ser.empty:
            return np.nan
        return float(ser.iloc[-1] if prefer == "last" else ser.mean())
    if hasattr(x, "columns"):
        try:
            if len(x.columns) == 1:
                return latest_scalar(x.iloc[:, 0], prefer)
        except Exception:
            pass
        try:
            ser = x.ffill().bfill().iloc[-1]
            return float(ser.squeeze()) if np.isscalar(ser.squeeze()) else np.nan
        except Exception:
            return np.nan
    if hasattr(x, "shape"):
        arr = np.asarray(x)
        return float(arr[-1]) if arr.size > 0 else np.nan
    try:
        return float(x)
    except Exception:
        return np.nan


# === MAIN EXECUTION ===
if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    instruments = s.get_instrument_list()
    rows = []

    for instr in instruments:
        try:
            ann_risk_ts = s.rawdata.annualised_returns_volatility(instr)
            daily_risk_ts = s.rawdata.daily_returns_volatility(instr)
            cont_value_ts = s.portfolio.get_baseccy_value_per_contract(instr)

            ann_risk = latest_scalar(ann_risk_ts)
            daily_risk = latest_scalar(daily_risk_ts)
            cont_value = latest_scalar(cont_value_ts)

            risk_pct = (ann_risk / cont_value * 100.0
                        if pd.notna(ann_risk) and pd.notna(cont_value) and cont_value != 0
                        else np.nan)

            rows.append({
                "Instrument": instr,
                "Annual Risk / Contract (base ccy)": round(ann_risk, 2) if pd.notna(ann_risk) else None,
                "Daily Risk / Contract (base ccy)": round(daily_risk, 2) if pd.notna(daily_risk) else None,
                "Contract Value (base ccy)": round(cont_value, 2) if pd.notna(cont_value) else None,
                "Annual Risk % of Contract Value": round(risk_pct, 3) if pd.notna(risk_pct) else None,
            })
        except Exception as e:
            rows.append({
                "Instrument": instr,
                "Annual Risk / Contract (base ccy)": None,
                "Daily Risk / Contract (base ccy)": None,
                "Contract Value (base ccy)": None,
                "Annual Risk % of Contract Value": None,
                "Note": f"Error: {e}"
            })

    risk_df = pd.DataFrame(rows).sort_values(
        by=["Annual Risk / Contract (base ccy)"],
        ascending=False,
        na_position="last"
    )

    print(risk_df.to_string(index=False))

    # === ASK TO EXPORT ===
    save_choice = input("\nDo you want to save this table as a CSV file? (yes/no): ").strip().lower()
    if save_choice in ["yes", "y"]:
        today = date.today().strftime("%Y%m%d")
        filename = f"risk_per_contract_{today}.csv"
        output_path = os.path.join(os.getcwd(), filename)
        risk_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"\n✅ File saved successfully: {output_path}")
    else:
        print("\n❌ Skipped saving CSV.")
