# asset_performance.py
import argparse
import copy
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# ===== Defaults (edit for click-to-run) =====
DEFAULT_CONFIG = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/12_check_asset_performance/asset_class.yaml"
DEFAULT_ASSET_MAP = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/12_check_asset_performance/asset_class_map.yaml"
DEFAULT_DATA = "db"          # "csv" or "db"
DEFAULT_PLOT = True          # plot by default
DEFAULT_INTERACTIVE = True   # ask questions when click-running in PyCharm

# ---------- Data helpers ----------
def make_data(source: str):
    s = (source or "csv").strip().lower()
    if s == "db":
        return dbFuturesSimData()
    if s == "csv":
        return csvFuturesSimData()
    raise ValueError("data source must be 'csv' or 'db'")

def to_index(curve_pct: pd.Series) -> pd.Series:
    """Convert cumulative percent curve (0 at start) to a growth index (1.0 at start)."""
    return 1.0 + (curve_pct / 100.0)

def to_twr_percent(curve_pct: pd.Series) -> pd.Series:
    """Convert cumulative percent curve to time-weighted return in percent (starts at 0%)."""
    return (to_index(curve_pct) - 1.0) * 100.0

def drawdown_series(index_curve: pd.Series) -> pd.Series:
    peak = index_curve.cummax()
    return (index_curve / peak) - 1.0

def summarize(index_curve: pd.Series) -> dict:
    idx = index_curve.dropna()
    if len(idx) < 2:
        return {"CAGR": np.nan, "Vol": np.nan, "MaxDD": np.nan, "Sharpe": np.nan}
    rets = idx.pct_change().dropna()
    ann = 252.0
    days = (idx.index[-1] - idx.index[0]).days
    years = max(days / 365.25, 1e-9)
    total = idx.iloc[-1] / idx.iloc[0] - 1.0
    cagr = (1.0 + total) ** (1.0 / years) - 1.0
    vol = rets.std() * np.sqrt(ann)
    sharpe = (rets.mean() * ann) / vol if vol > 0 else np.nan
    maxdd = drawdown_series(idx).min()
    return {"CAGR": cagr, "Vol": vol, "MaxDD": maxdd, "Sharpe": sharpe}

def rolling_realised_risk_from_returns(rets: pd.Series, window_days: int = 42, ann: float = 252.0) -> pd.Series:
    return (rets.rolling(window_days).std() * np.sqrt(ann)).dropna()

def returns_from_curve_pct(curve_pct: pd.Series) -> pd.Series:
    idx = to_index(curve_pct)
    return idx.pct_change().dropna()

def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def save_yaml(doc: dict, path: Path) -> None:
    with open(path, "w") as f:
        yaml.safe_dump(doc, f, sort_keys=False)

def subset_dict(d: Optional[dict], keys: List[str]) -> Optional[dict]:
    if d is None:
        return None
    return {k: v for k, v in d.items() if k in keys}

def normalize_equal_weights(instruments: List[str]) -> Dict[str, float]:
    if not instruments:
        return {}
    w = 1.0 / float(len(instruments))
    return {inst: w for inst in instruments}

def build_system_from_yaml(config_path: Path, data_source: str):
    cfg = Config(str(config_path))
    return futures_system(config=cfg, data=make_data(data_source))

def get_equity_percent_curve(sys_obj) -> pd.Series:
    # cumulative portfolio net % curve from pysystemtrade (NaNs dropped)
    return sys_obj.accounts.portfolio().net.percent.curve().dropna()

# ---------- Asset map expansion ----------
# Accepts either:
#   Class: [inst, ...]
# or
#   Class: { SubClass: [inst,...], ... }
# level="class" -> groups are each Class (union of its instruments)
# level="sub"   -> groups are "Class: SubClass"
def expand_asset_map(
    asset_map: Dict[str, Union[List[str], Dict[str, List[str]]]],
    level: str = "class"
) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for cls, v in asset_map.items():
        if isinstance(v, dict):
            if level == "class":
                merged: List[str] = []
                for lst in v.values():
                    merged.extend(lst or [])
                out[cls] = sorted(list(dict.fromkeys(merged)))  # unique
            else:  # level == "sub"
                for sub, lst in v.items():
                    out[f"{cls}: {sub}"] = list(lst or [])
        else:
            # simple list
            out[cls] = list(v or [])
    return out

# ---------- Config builder for a group ----------
def make_asset_class_config(base_cfg: dict, instruments: List[str]) -> dict:
    cfg = copy.deepcopy(base_cfg)
    cfg["instrument_weights"] = normalize_equal_weights(instruments)

    fw = cfg.get("forecast_weights")
    if isinstance(fw, dict):
        base_instruments = set((base_cfg.get("instrument_weights") or {}).keys())
        keys = set(fw.keys())
        # If keys look like instruments, subset; else keep global rule dict
        cfg["forecast_weights"] = subset_dict(fw, instruments) if (keys & base_instruments) else fw

    fdm = cfg.get("forecast_div_multiplier")
    if isinstance(fdm, dict):
        cfg["forecast_div_multiplier"] = subset_dict(fdm, instruments)
    # if numeric/global: leave as-is

    return cfg

# ---------- Interactive utilities ----------
def ask_choice(prompt: str, options: dict, default_key: str) -> str:
    """
    Prompt user to choose among options; returns the chosen option VALUE.
    options example: {"1": "class", "2": "sub"}
    """
    opts_text = " / ".join([f"{k}) {v}" for k, v in options.items()])
    while True:
        ans = input(f"{prompt} [{opts_text}] (default {default_key}): ").strip().lower()
        if ans == "":
            ans = default_key
        if ans in options:
            return options[ans]
        print(f"Please type one of: {', '.join(options.keys())}")

def ask_db_or_csv(current_default: str = "db") -> str:
    """
    One-step tolerant prompt:
    - Enter: keep default (e.g., 'db')
    - y/yes/db -> 'db'
    - n/no/csv -> 'csv'
    """
    default_yes = (current_default.lower() == "db")
    d = "Y/n" if default_yes else "y/N"
    while True:
        ans = input(f"Use data source 'db'? (choose 'db' for local DB, 'csv' for CSV files) [{d}]: ").strip().lower()
        if ans == "":
            return "db" if default_yes else "csv"
        if ans in ("y", "yes", "db"):
            return "db"
        if ans in ("n", "no", "csv", "c"):
            return "csv"
        print("Please answer y or n (or type 'db' or 'csv').")

def ask_filter_terms() -> str:
    """
    One-step filter prompt.
    - Enter: no filter (returns "")
    - Otherwise: return the string as-is (e.g., "FX, Oil")
    """
    return input("Filter groups (comma-separated), or press Enter for none: ").strip()

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="Compare equally-weighted performance by (sub)asset class.")
    p.add_argument("--config", default=DEFAULT_CONFIG, help="Base system YAML")
    p.add_argument("--asset-map", default=DEFAULT_ASSET_MAP, help="YAML mapping of class -> list or class -> {sub:list}")
    p.add_argument("--data", default=DEFAULT_DATA, choices=["csv", "db"], help="Data source for all groups")

    # plot flags
    plot_group = p.add_mutually_exclusive_group()
    plot_group.add_argument("--plot", dest="plot", action="store_true", help="Show plots (default)")
    plot_group.add_argument("--no-plot", dest="plot", action="store_false", help="Disable plots")
    p.set_defaults(plot=DEFAULT_PLOT)

    # choose level (major asset vs sub-asset breakdown)
    p.add_argument("--level", choices=["class", "sub"], default=None,
                   help="Use 'class' for major asset level (FX, Ags, ...), 'sub' for sub-asset (Em/Dev, Oil/Gas, ...).")

    # optional filter (comma-separated substrings)
    p.add_argument("--include", default="", help="Only run groups whose name contains any of these comma-separated terms.")

    # interactive toggle
    inter = p.add_mutually_exclusive_group()
    inter.add_argument("--interactive", dest="interactive", action="store_true", help="Prompt for choices (default)")
    inter.add_argument("--no-interactive", dest="interactive", action="store_false", help="Do not prompt; use flags/defaults")
    p.set_defaults(interactive=DEFAULT_INTERACTIVE)

    p.add_argument("--window-days", type=int, default=42, help="Rolling risk window (trading days)")
    return p.parse_args()

def main():
    args = parse_args()

    # --- interactive questions (for PyCharm click-run) ---
    if args.interactive:
        if not args.level:
            args.level = ask_choice("Group by", {"1": "class", "2": "sub"}, default_key="1")
        if args.include == "":
            args.include = ask_filter_terms()  # Enter→none; text→used directly
        # Simplified single-step db/csv choice
        args.data = ask_db_or_csv(args.data)

    base_path = Path(args.config)
    asset_map_path = Path(args.asset_map)

    if not base_path.exists():
        raise FileNotFoundError(f"Config not found: {base_path}")
    if not asset_map_path.exists():
        raise FileNotFoundError(f"Asset map not found: {asset_map_path}")

    base_cfg = load_yaml(base_path)
    raw_map: Dict[str, Any] = load_yaml(asset_map_path)

    groups = expand_asset_map(raw_map, level=args.level or "class")

    # optional include filter
    include_terms = [t.strip() for t in args.include.split(",") if t.strip()]
    if include_terms:
        groups = {k: v for k, v in groups.items() if any(t.lower() in k.lower() for t in include_terms)}

    # Build systems per group by writing temp configs
    curves_pct: Dict[str, pd.Series] = {}
    risks: Dict[str, pd.Series] = {}
    metrics: Dict[str, dict] = {}
    per_instrument_curves: Dict[str, Dict[str, pd.Series]] = {}
    missing_instruments: Dict[str, List[str]] = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        for label, inst_list in groups.items():
            base_instruments = set((base_cfg.get("instrument_weights") or {}).keys())
            miss = [i for i in inst_list if i not in base_instruments]
            if miss:
                missing_instruments[label] = miss

            # Group-level system
            cfg_grp = make_asset_class_config(base_cfg, inst_list)
            tmp_cfg_path = Path(tmpdir) / f"tmp_{label.replace(': ','_').replace(' ','_')}.yaml"
            save_yaml(cfg_grp, tmp_cfg_path)

            sys_grp = build_system_from_yaml(tmp_cfg_path, args.data)
            curve_pct = get_equity_percent_curve(sys_grp)
            curves_pct[label] = curve_pct

            idx = to_index(curve_pct)
            metrics[label] = summarize(idx)

            rets = returns_from_curve_pct(curve_pct)
            risks[label] = rolling_realised_risk_from_returns(rets, window_days=args.window_days)

            # ---- Per-instrument systems within this group ----
            per_instrument_curves[label] = {}
            for inst in inst_list:
                cfg_inst = make_asset_class_config(base_cfg, [inst])
                tmp_inst_path = Path(tmpdir) / f"tmp_{label.replace(': ','_').replace(' ','_')}_{inst}.yaml"
                save_yaml(cfg_inst, tmp_inst_path)
                sys_inst = build_system_from_yaml(tmp_inst_path, args.data)
                inst_curve = get_equity_percent_curve(sys_inst)
                per_instrument_curves[label][inst] = inst_curve

    # ---------- Output tables ----------
    metrics_df = pd.DataFrame(metrics).T[["CAGR", "Vol", "MaxDD", "Sharpe"]]
    as_pct = lambda x: f"{x:.2%}" if pd.notna(x) else "—"
    pretty = metrics_df.copy()
    pretty["CAGR"] = pretty["CAGR"].map(as_pct)
    pretty["Vol"] = pretty["Vol"].map(as_pct)
    pretty["MaxDD"] = pretty["MaxDD"].map(as_pct)
    pretty["Sharpe"] = pretty["Sharpe"].map(lambda x: f"{x:.2f}" if pd.notna(x) else "—")

    print(f"\n== Performance by {'class' if (args.level or 'class')=='class' else 'sub-class'} (equal weight within group) ==")
    print(pretty.to_string())

    if missing_instruments:
        print("\n[WARN] Instruments listed in map but absent from base instrument_weights:")
        for label, mis in missing_instruments.items():
            print(f"  - {label}: {', '.join(mis)}")

    # ---------- Plots ----------
    if args.plot:
        # Equity (TWR % starting at 0) by group
        plt.figure(figsize=(10, 5))
        for label, curve_pct in curves_pct.items():
            to_twr_percent(curve_pct).plot(label=label)
        plt.title(f"Equity by {'Class' if (args.level or 'class')=='class' else 'Sub-class'} (TWR, %)")
        plt.xlabel("Date"); plt.ylabel("TWR (%)")
        plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

        # Drawdown (from index) by group
        plt.figure(figsize=(10, 4))
        for label, curve_pct in curves_pct.items():
            (drawdown_series(to_index(curve_pct)) * 100.0).plot(label=label)
        plt.title(f"Drawdown by {'Class' if (args.level or 'class')=='class' else 'Sub-class'} (%)")
        plt.xlabel("Date"); plt.ylabel("Drawdown (%)")
        plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

        # Rolling risk (annualised %) by group
        plt.figure(figsize=(10, 4))
        for label, risk_ser in risks.items():
            (risk_ser * 100.0).plot(label=label)
        plt.title(f"Rolling {args.window_days}-day Realised Risk (annualised, %)")
        plt.xlabel("Date"); plt.ylabel("Risk (%)")
        plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

        # ---- Per-instrument equity plots inside each group ----
        for label, inst_map in per_instrument_curves.items():
            if not inst_map:
                continue
            plt.figure(figsize=(10, 5))
            for inst, curve_pct in inst_map.items():
                to_twr_percent(curve_pct).plot(label=inst)
            plt.title(f"{label} — Instrument Performance (TWR, %)")
            plt.xlabel("Date"); plt.ylabel("TWR (%)")
            plt.grid(True); plt.legend(title="Instrument", ncol=2); plt.tight_layout(); plt.show()

if __name__ == "__main__":
    main()
