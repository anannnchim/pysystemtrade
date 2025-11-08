# compare_strategy.py
import argparse
from pathlib import Path
from typing import Dict, Optional, Any, Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# ===== Defaults so it runs directly from PyCharm "Run" =====
DEFAULT_CONFIG1 = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/diversified.yaml"
DEFAULT_CONFIG2 = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/system_f1_config.yaml"
DEFAULT_LABEL1  = "Diversified"
DEFAULT_LABEL2  = "F1"
DEFAULT_USE_DB  = False  # switch to True if you prefer DB by default

# ===== Builders & helpers =====
def build_system(config_path: str, use_db: bool = False):
    cfg = Config(config_path)
    data = dbFuturesSimData() if use_db else csvFuturesSimData()
    return futures_system(config=cfg, data=data)

def get_equity_percent_curve(sys_obj) -> pd.Series:
    """Return cumulative net % curve from pysystemtrade (NaNs dropped)."""
    return sys_obj.accounts.portfolio().net.percent.curve().dropna()

def to_index(curve_pct: pd.Series) -> pd.Series:
    """Convert cumulative % curve to growth index (1.0 baseline)."""
    return 1.0 + (curve_pct / 100.0)

def drawdown_series(index_curve: pd.Series) -> pd.Series:
    """Drawdown from running peak on 1-based index curve (returns negative values)."""
    peak = index_curve.cummax()
    return (index_curve / peak) - 1.0

def summarize(index_curve: pd.Series) -> dict:
    """
    Basic performance summary: CAGR, Vol (ann), MaxDD, Sharpe (rf=0).
    Expects a 1-based growth index.
    """
    idx = index_curve.dropna()
    if len(idx) < 2:
        return {"CAGR": np.nan, "Vol": np.nan, "MaxDD": np.nan, "Sharpe": np.nan}

    rets = idx.pct_change().dropna()
    ann_factor = 252.0

    days = (idx.index[-1] - idx.index[0]).days
    years = max(days / 365.25, 1e-9)
    total_return = idx.iloc[-1] / idx.iloc[0] - 1.0
    cagr = (1.0 + total_return) ** (1.0 / years) - 1.0

    vol = rets.std() * np.sqrt(ann_factor)
    sharpe = (rets.mean() * ann_factor) / vol if vol > 0 else np.nan
    maxdd = drawdown_series(idx).min()

    return {"CAGR": cagr, "Vol": vol, "MaxDD": maxdd, "Sharpe": sharpe}

def _coerce_to_series(x: Any) -> pd.Series:
    """Helper: coerce various 1-D structures to a Series."""
    if isinstance(x, pd.Series):
        return x
    if isinstance(x, pd.DataFrame):
        if x.shape[1] == 1:
            return x.iloc[:, 0]
        return x.iloc[:, 0]
    if isinstance(x, dict):
        return pd.Series(x)
    if isinstance(x, (list, tuple)):
        # handle [(name, value), ...] OR [value1, value2, ...]
        if len(x) > 0 and isinstance(x[0], (list, tuple)) and len(x[0]) == 2:
            return pd.Series({k: v for k, v in x})
        return pd.Series(x)
    return pd.Series([x])

def rolling_realised_risk(sys_obj, window_days: int = 42, ann_factor: float = 252.0) -> pd.Series:
    """
    2-month realised risk (annualised stdev).
    Returns a **decimal** series (e.g., 0.20 for 20%).
    - If pysystemtrade's percent.rolling_ann_std() returns percent units (≈20),
      convert to decimal by dividing by 100.
    - Else compute from returns and annualise.
    """
    percent = sys_obj.accounts.portfolio().percent
    # Try native API (often already annualised, commonly in percent units)
    try:
        ser = percent.rolling_ann_std()
        s = _coerce_to_series(ser).dropna()
        # Detect units: if median > 5, it's percent (e.g., 20), convert to decimal.
        if s.median() > 5:
            s = s / 100.0
        return s
    except Exception:
        pass

    # Fallback: rolling std of daily returns * sqrt(ann_factor)
    curve_pct = sys_obj.accounts.portfolio().net.percent.curve().dropna()
    idx = to_index(curve_pct)
    rets = idx.pct_change().dropna()
    return (rets.rolling(window_days).std() * np.sqrt(ann_factor)).dropna()

# ===== percent.stats() → tidy comparison helpers =====
def _extract_pairs_like_stats(raw) -> Optional[pd.Series]:
    """
    Accepts many shapes (list-of-pairs, dict, Series/DataFrame) and returns a Series of metrics.
    Special-case for builds that return: [ [(k,v), (k,v), ...], "You can also ..."]
    """
    # DataFrame / Series
    if isinstance(raw, pd.DataFrame):
        if raw.shape[1] == 1:
            return raw.iloc[:, 0]
        return raw.iloc[:, 0]
    if isinstance(raw, pd.Series):
        return raw

    # Dict
    if isinstance(raw, dict):
        return pd.Series(raw)

    # List / tuple
    if isinstance(raw, (list, tuple)):
        # Look for the first list-of-pairs inside
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) > 0:
                if isinstance(item[0], (list, tuple)) and len(item[0]) == 2:
                    try:
                        return pd.Series({k: v for k, v in item})
                    except Exception:
                        pass
        # Fallback: if it's a simple list of values, index them
        return pd.Series({f"stat_{i}": v for i, v in enumerate(raw)})

    # Anything else → wrap
    return pd.Series({"value": raw})

def get_percent_stats_series(sys_obj) -> Optional[pd.Series]:
    """Safe wrapper around s.accounts.portfolio().percent.stats() → Series of metrics."""
    try:
        raw = sys_obj.accounts.portfolio().percent.stats()
    except Exception:
        return None
    ser = _extract_pairs_like_stats(raw)
    if ser is None or len(ser) == 0:
        return None
    # Drop helper/noise keys if present
    for k in list(ser.index):
        if isinstance(ser[k], str) and "You can also" in ser[k]:
            ser = ser.drop(index=k)
    return ser

# Preferred order and formatting rules
_METRIC_ORDER = [
    "ann_mean", "ann_std", "sharpe", "sortino", "calmar",
    "avg_drawdown", "time_in_drawdown", "hitrate",
    "profitfactor", "gaintolossratio", "avg_return_to_drawdown",
    "avg_gain", "avg_loss",
    "mean", "median", "std", "min", "max",
    "t_stat", "p_value",
]

_PERCENT_METRICS = {
    # annual / risk / drawdown / hit-rate style
    "ann_mean", "ann_std", "avg_drawdown", "time_in_drawdown", "hitrate",
    # per-period returns in many builds:
    "mean", "median", "std", "min", "max", "avg_gain", "avg_loss",
}

_RATIO_METRICS = {"sharpe", "sortino", "calmar", "profitfactor", "gaintolossratio", "avg_return_to_drawdown"}

def _format_metric_value(metric: str, x: float) -> str:
    if pd.isna(x):
        return "—"
    if metric in _PERCENT_METRICS:
        return f"{x:.2f}%" if abs(x) > 1.5 else f"{x*100:.2f}%"
        # Heuristic: if stats already in percent units (e.g., 10.12), print as-is with '%';
        # if likely decimal (e.g., 0.1012), multiply by 100. Threshold 1.5 handles both.
    if metric == "p_value":
        return f"{x:.3f}"
    if metric in _RATIO_METRICS or metric == "t_stat":
        return f"{x:.2f}"
    # default
    return f"{x:.4f}"

def print_stats_comparison(label1: str, s1: Optional[pd.Series],
                           label2: str, s2: Optional[pd.Series]) -> None:
    if s1 is None and s2 is None:
        print("\n(percent.stats() not available in this build)")
        return

    df = pd.DataFrame({label1: s1, label2: s2})

    # Reorder rows by our preferred order, then append any extras
    known = [m for m in _METRIC_ORDER if m in df.index]
    extras = [m for m in df.index if m not in known]
    df = df.loc[known + sorted(extras)]

    # Format nicely
    shown = df.copy()
    for m in shown.index:
        for col in shown.columns:
            try:
                shown.loc[m, col] = _format_metric_value(m, float(shown.loc[m, col]))
            except Exception:
                pass  # keep non-numeric values as-is

    print("\n== percent.stats() (comparison) ==")
    print(shown.to_string())

# ===== Plotters =====
def plot_equities(curves: Dict[str, pd.Series]):
    plt.figure(figsize=(10, 5))
    for label, curve_pct in curves.items():
        to_index(curve_pct).plot(label=label)
    plt.title("System Net % Performance (growth index)")
    plt.xlabel("Date"); plt.ylabel("Index (1.0 = start)")
    plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

def plot_drawdowns(curves: Dict[str, pd.Series]):
    plt.figure(figsize=(10, 4))
    for label, curve_pct in curves.items():
        (drawdown_series(to_index(curve_pct)) * 100.0).plot(label=label)
    plt.title("Portfolio Drawdown (%)")
    plt.xlabel("Date"); plt.ylabel("Drawdown (%)")
    plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

def plot_rolling_risk(series_map: Dict[str, pd.Series]):
    plt.figure(figsize=(10, 4))
    for label, ser in series_map.items():
        # ser is decimal (0.20=20%); convert to %
        (ser * 100.0).plot(label=label)
    plt.title("Rolling 2-Month Realised Risk (annualised, %)")
    plt.xlabel("Date"); plt.ylabel("Risk (%)")
    plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

# ===== CLI (with defaults so click-run works) =====
def parse_args():
    p = argparse.ArgumentParser(description="Compare two pysystemtrade configurations.")
    p.add_argument("--config1", default=DEFAULT_CONFIG1, help="Path to YAML for system 1")
    p.add_argument("--config2", default=DEFAULT_CONFIG2, help="Path to YAML for system 2")
    p.add_argument("--label1", default=DEFAULT_LABEL1, help="Label for system 1")
    p.add_argument("--label2", default=DEFAULT_LABEL2, help="Label for system 2")
    p.add_argument("--use-db", action="store_true", default=DEFAULT_USE_DB, help="Use DB data instead of CSV")
    return p.parse_args()

def main():
    args = parse_args()

    # Warn if defaults not found, but continue to avoid crashing click-run
    missing = [p for p in [args.config1, args.config2] if not Path(p).exists()]
    if missing:
        print("WARNING: Missing config(s):")
        for m in missing:
            print(" -", m)
        print("Update DEFAULT_CONFIG* or pass --config1/--config2 in Run Configuration.")

    # Build systems
    s1 = build_system(args.config1, use_db=args.use_db)
    s2 = build_system(args.config2, use_db=args.use_db)

    # Curves
    c1 = get_equity_percent_curve(s1)
    c2 = get_equity_percent_curve(s2)

    # 1) Equity (growth index) & Drawdown plots
    plot_equities({args.label1: c1, args.label2: c2})
    plot_drawdowns({args.label1: c1, args.label2: c2})

    # 2) Summary metrics table
    m1 = summarize(to_index(c1))
    m2 = summarize(to_index(c2))
    metrics_df = pd.DataFrame.from_dict({args.label1: m1, args.label2: m2}, orient="index")
    fmt_pct = lambda x: f"{x:.2%}" if pd.notna(x) else "—"
    printable = metrics_df.copy()
    printable["CAGR"]   = printable["CAGR"].map(fmt_pct)
    printable["Vol"]    = printable["Vol"].map(fmt_pct)
    printable["MaxDD"]  = printable["MaxDD"].map(fmt_pct)  # already negative
    printable["Sharpe"] = printable["Sharpe"].map(lambda x: f"{x:.2f}" if pd.notna(x) else "—")
    print("\n== Summary metrics ==")
    print(printable.to_string())

    # 3) Rolling 2-M realised risk (≈42 trading days), chart + averages
    r1 = rolling_realised_risk(s1, window_days=42)
    r2 = rolling_realised_risk(s2, window_days=42)
    plot_rolling_risk({args.label1: r1, args.label2: r2})
    print("\n== Avg. 2-Month Realised Risk (annualised) ==")
    print(f"{args.label1}: {r1.mean():.2%}")
    print(f"{args.label2}: {r2.mean():.2%}")

    # 4) percent.stats() tidy comparison
    s1_stats_ser = get_percent_stats_series(s1)
    s2_stats_ser = get_percent_stats_series(s2)
    print_stats_comparison(args.label1, s1_stats_ser, args.label2, s2_stats_ser)

if __name__ == "__main__":
    main()
