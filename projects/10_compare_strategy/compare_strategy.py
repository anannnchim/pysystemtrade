# compare_strategy.py
import argparse
from pathlib import Path
from typing import Dict, Optional, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# ===== Defaults so it runs directly from PyCharm "Run" =====
DEFAULT_CONFIG1 = "/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/config.yaml"
DEFAULT_CONFIG2 = "/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/config_v2.yaml"
DEFAULT_CONFIG3 = "/Users/nanthawat/PycharmProjects/pysystemtrade/private/systems/new/config_v3.yaml"
DEFAULT_CONFIG4 = ""
DEFAULT_CONFIG5 = ""

DEFAULT_LABEL1  = "Comb"
DEFAULT_LABEL2  = "EMA"
DEFAULT_LABEL3  = "BO"
DEFAULT_LABEL4  = "10X"
DEFAULT_LABEL5  = "BreakoutEMACarry"

DEFAULT_DATA1   = "db"   # "csv" or "db"
DEFAULT_DATA2   = "db"
DEFAULT_DATA3   = "db"
DEFAULT_DATA4   = "csv"
DEFAULT_DATA5   = "db"

# ===== Builders & helpers =====
def make_data(source: str):
    s = (source or "csv").strip().lower()
    if s == "db":
        return dbFuturesSimData()
    if s == "csv":
        return csvFuturesSimData()
    raise ValueError(f"Unknown data source '{source}'. Use 'csv' or 'db'.")

def build_system(config_path: str, data_source: str = "csv"):
    cfg = Config(config_path)
    data = make_data(data_source)
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
    """CAGR, Vol (ann), MaxDD, Sharpe (rf=0). Expects 1-based growth index."""
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
    if isinstance(x, pd.Series):
        return x
    if isinstance(x, pd.DataFrame):
        return x.iloc[:, 0] if x.shape[1] >= 1 else pd.Series(dtype=float)
    if isinstance(x, dict):
        return pd.Series(x)
    if isinstance(x, (list, tuple)):
        if len(x) > 0 and isinstance(x[0], (list, tuple)) and len(x[0]) == 2:
            return pd.Series({k: v for k, v in x})
        return pd.Series(x)
    return pd.Series([x])

def returns_from_curve_pct(curve_pct: pd.Series) -> pd.Series:
    """Daily returns from a cumulative % curve."""
    idx = to_index(curve_pct)
    return idx.pct_change().dropna()

def blend_curve_pct_equal_weight(*curves: pd.Series) -> pd.Series:
    """
    Equal-weight blend of DAILY RETURNS of N systems, then re-cumulated to a curve %.
    This represents an equally-weighted portfolio rebalanced daily.
    """
    rets_list: List[pd.Series] = []
    for c in curves:
        if c is None:
            continue
        r = returns_from_curve_pct(c)
        if not r.empty:
            rets_list.append(r)

    if not rets_list:
        return pd.Series(dtype=float)

    df_rets = pd.concat(rets_list, axis=1)
    blended_rets = df_rets.mean(axis=1, skipna=True)
    blended_idx = (1.0 + blended_rets).cumprod()
    blended_curve_pct = (blended_idx - 1.0) * 100.0
    return blended_curve_pct

def rolling_realised_risk(sys_obj, window_days: int = 42, ann_factor: float = 252.0) -> pd.Series:
    """
    2-month realised risk (annualised stdev).
    Returns a **decimal** series (0.20 = 20%).
    """
    percent = sys_obj.accounts.portfolio().percent
    try:
        ser = percent.rolling_ann_std()
        s = _coerce_to_series(ser).dropna()
        if s.median() > 5:  # already in percent units (e.g., 20)
            s = s / 100.0
        return s
    except Exception:
        pass
    curve_pct = sys_obj.accounts.portfolio().net.percent.curve().dropna()
    idx = to_index(curve_pct)
    rets = idx.pct_change().dropna()
    return (rets.rolling(window_days).std() * np.sqrt(ann_factor)).dropna()

def rolling_realised_risk_from_returns(rets: pd.Series, window_days: int = 42, ann_factor: float = 252.0) -> pd.Series:
    """Annualised rolling stdev from a returns series (decimal)."""
    return (rets.rolling(window_days).std() * np.sqrt(ann_factor)).dropna()

# ===== percent.stats() → tidy comparison helpers =====
def _extract_pairs_like_stats(raw) -> Optional[pd.Series]:
    if isinstance(raw, pd.DataFrame):
        return raw.iloc[:, 0] if raw.shape[1] >= 1 else pd.Series(dtype=float)
    if isinstance(raw, pd.Series):
        return raw
    if isinstance(raw, dict):
        return pd.Series(raw)
    if isinstance(raw, (list, tuple)):
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) > 0:
                if isinstance(item[0], (list, tuple)) and len(item[0]) == 2:
                    try:
                        return pd.Series({k: v for k, v in item})
                    except Exception:
                        pass
        return pd.Series({f"stat_{i}": v for i, v in enumerate(raw)})
    return pd.Series({"value": raw})

def get_percent_stats_series(sys_obj) -> Optional[pd.Series]:
    try:
        raw = sys_obj.accounts.portfolio().percent.stats()
    except Exception:
        return None
    ser = _extract_pairs_like_stats(raw)
    if ser is None or len(ser) == 0:
        return None
    for k in list(ser.index):
        if isinstance(ser[k], str) and "You can also" in ser[k]:
            ser = ser.drop(index=k)
    return ser

_METRIC_ORDER = [
    "ann_mean", "ann_std", "sharpe", "sortino", "calmar",
    "avg_drawdown", "time_in_drawdown", "hitrate",
    "profitfactor", "gaintolossratio", "avg_return_to_drawdown",
    "avg_gain", "avg_loss",
    "mean", "median", "std", "min", "max",
    "t_stat", "p_value",
]
_PERCENT_METRICS = {
    "ann_mean", "ann_std", "avg_drawdown", "time_in_drawdown", "hitrate",
    "mean", "median", "std", "min", "max", "avg_gain", "avg_loss",
}
_RATIO_METRICS = {"sharpe", "sortino", "calmar", "profitfactor", "gaintolossratio", "avg_return_to_drawdown"}

def _format_metric_value(metric: str, x: float) -> str:
    if pd.isna(x):
        return "—"
    if metric in _PERCENT_METRICS:
        return f"{x:.2f}%" if abs(x) > 1.5 else f"{x*100:.2f}%"
    if metric == "p_value":
        return f"{x:.3f}"
    if metric in _RATIO_METRICS or metric == "t_stat":
        return f"{x:.2f}"
    return f"{x:.4f}"

def print_stats_comparison_multi(stats_dict: Dict[str, Optional[pd.Series]]) -> None:
    """Compare percent.stats() for multiple systems (columns = systems)."""
    non_empty = {label: s for label, s in stats_dict.items() if s is not None}
    if not non_empty:
        print("\n(percent.stats() not available in this build)")
        return

    df = pd.DataFrame(non_empty)
    known = [m for m in _METRIC_ORDER if m in df.index]
    extras = [m for m in df.index if m not in known]
    df = df.loc[known + sorted(extras)]

    shown = df.copy()
    for m in shown.index:
        for col in shown.columns:
            try:
                shown.loc[m, col] = _format_metric_value(m, float(shown.loc[m, col]))
            except Exception:
                pass

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
        (ser * 100.0).plot(label=label)
    plt.title("Rolling 2-Month Realised Risk (annualised, %)")
    plt.xlabel("Date"); plt.ylabel("Risk (%)")
    plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

# ===== CLI (with defaults so click-run works) =====
def parse_args():
    p = argparse.ArgumentParser(description="Compare 2–5 pysystemtrade configurations.")
    p.add_argument("--config1", default=DEFAULT_CONFIG1, help="Path to YAML for system 1")
    p.add_argument("--config2", default=DEFAULT_CONFIG2, help="Path to YAML for system 2")
    p.add_argument("--config3", default=DEFAULT_CONFIG3, help="Path to YAML for system 3 (optional)")
    p.add_argument("--config4", default=DEFAULT_CONFIG4, help="Path to YAML for system 4 (optional)")
    p.add_argument("--config5", default=DEFAULT_CONFIG5, help="Path to YAML for system 5 (optional)")

    p.add_argument("--label1",  default=DEFAULT_LABEL1,  help="Label for system 1")
    p.add_argument("--label2",  default=DEFAULT_LABEL2,  help="Label for system 2")
    p.add_argument("--label3",  default=DEFAULT_LABEL3,  help="Label for system 3")
    p.add_argument("--label4",  default=DEFAULT_LABEL4,  help="Label for system 4")
    p.add_argument("--label5",  default=DEFAULT_LABEL5,  help="Label for system 5")

    p.add_argument("--data1",   default=DEFAULT_DATA1,   choices=["csv", "db"], help="Data source for system 1")
    p.add_argument("--data2",   default=DEFAULT_DATA2,   choices=["csv", "db"], help="Data source for system 2")
    p.add_argument("--data3",   default=DEFAULT_DATA3,   choices=["csv", "db"], help="Data source for system 3")
    p.add_argument("--data4",   default=DEFAULT_DATA4,   choices=["csv", "db"], help="Data source for system 4")
    p.add_argument("--data5",   default=DEFAULT_DATA5,   choices=["csv", "db"], help="Data source for system 5")
    return p.parse_args()

def main():
    args = parse_args()

    # Collect configs / labels / data into lists  ← FIXED to include system 5
    config_paths = [args.config1, args.config2, args.config3, args.config4, args.config5]
    labels       = [args.label1,  args.label2,  args.label3,  args.label4,  args.label5]
    data_srcs    = [args.data1,   args.data2,   args.data3,   args.data4,   args.data5]

    systems = []
    curves  = []
    used_labels = []

    print("\nBuilding systems:")

    for cfg_path, label, data_src in zip(config_paths, labels, data_srcs):
        if not cfg_path:  # empty string -> skip
            continue

        path_obj = Path(cfg_path)
        if not path_obj.exists():
            print(f" - {label}: config={cfg_path}  data={data_src}  [SKIP: file not found]")
            continue

        print(f" - {label}: config={cfg_path}  data={data_src}")
        sys_obj = build_system(cfg_path, data_source=data_src)
        curve_pct = get_equity_percent_curve(sys_obj)

        systems.append(sys_obj)
        curves.append(curve_pct)
        used_labels.append(label)

    if len(systems) < 2:
        print("\nERROR: Need at least 2 valid systems (configs found and built).")
        print("Check your --config* paths or DEFAULT_CONFIG*.")
        return

    # Blended equity (equal-weight DAILY returns of all provided systems)
    blend_label = f"Avg (equal-weight {len(systems)} systems)"
    c_blend = blend_curve_pct_equal_weight(*curves)

    # 1) Equity (growth index) & Drawdown plots — include blend
    curve_map = {label: c for label, c in zip(used_labels, curves)}
    curve_map[blend_label] = c_blend

    plot_equities(curve_map)
    plot_drawdowns(curve_map)

    # 2) Summary metrics table (include blend)
    metrics_map = {}
    for label, c in zip(used_labels, curves):
        metrics_map[label] = summarize(to_index(c))
    metrics_map[blend_label] = summarize(to_index(c_blend))

    metrics_df = pd.DataFrame.from_dict(metrics_map, orient="index")
    fmt_pct = lambda x: f"{x:.2%}" if pd.notna(x) else "—"
    printable = metrics_df.copy()
    printable["CAGR"]   = printable["CAGR"].map(fmt_pct)
    printable["Vol"]    = printable["Vol"].map(fmt_pct)
    printable["MaxDD"]  = printable["MaxDD"].map(fmt_pct)
    printable["Sharpe"] = printable["Sharpe"].map(lambda x: f"{x:.2f}" if pd.notna(x) else "—")

    print("\n== Summary metrics ==")
    print(printable.to_string())

    # 3) Rolling 2-M realised risk (≈42 trading days), chart + averages (include blend)
    risk_map = {}
    for label, sys_obj in zip(used_labels, systems):
        risk_map[label] = rolling_realised_risk(sys_obj, window_days=42)

    r_blend = rolling_realised_risk_from_returns(
        returns_from_curve_pct(c_blend),
        window_days=42
    )
    risk_map[blend_label] = r_blend

    plot_rolling_risk(risk_map)

    print("\n== Avg. 2-Month Realised Risk (annualised) ==")
    for label, ser in risk_map.items():
        print(f"{label}: {ser.mean():.2%}")

    # 4) percent.stats() tidy comparison (only real systems; blend omitted)
    stats_map = {}
    for label, sys_obj in zip(used_labels, systems):
        stats_map[label] = get_percent_stats_series(sys_obj)

    print_stats_comparison_multi(stats_map)

if __name__ == "__main__":
    main()
