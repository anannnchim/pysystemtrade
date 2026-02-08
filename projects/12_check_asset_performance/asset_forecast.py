# asset_forecast.py
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
DEFAULT_CONFIG = "/home/anan/AnanProjects/pysystemtrade/projects/12_check_asset_performance/asset_class.yaml"
DEFAULT_ASSET_MAP = "/home/anan/AnanProjects/pysystemtrade/projects/12_check_asset_performance/asset_class_map.yaml"
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

# ---------- Forecast helpers ----------
def get_combined_forecast_series(sys_obj, instrument: str) -> pd.Series:
    """
    Returns the combined forecast series for a single instrument.
    Robustly coerces various shapes to a pd.Series indexed by date.
    """
    raw = sys_obj.combForecast.get_combined_forecast(instrument)
    # Typical is a Series; but be defensive:
    if isinstance(raw, pd.Series):
        return raw.dropna()
    if isinstance(raw, pd.DataFrame):
        # try first column
        return raw.iloc[:, 0].dropna()
    # fallback: wrap scalars/dicts into a Series (unlikely)
    try:
        ser = pd.Series(raw).dropna()
        # if no datetime index, return as-is
        return ser
    except Exception:
        return pd.Series(dtype=float)

def average_forecasts_equal_weight(forecasts: Dict[str, pd.Series]) -> pd.Series:
    """
    Align all instrument forecast series on a common index and average equally.
    """
    if not forecasts:
        return pd.Series(dtype=float)
    df = pd.DataFrame(forecasts)  # outer-join on index
    return df.mean(axis=1, skipna=True).dropna()

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
    p = argparse.ArgumentParser(description="Compare combined forecasts by (sub)asset class.")
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

    # Build systems and collect forecasts
    group_forecasts: Dict[str, pd.Series] = {}
    per_instrument_forecasts: Dict[str, Dict[str, pd.Series]] = {}
    missing_instruments: Dict[str, List[str]] = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        for label, inst_list in groups.items():
            base_instruments = set((base_cfg.get("instrument_weights") or {}).keys())
            miss = [i for i in inst_list if i not in base_instruments]
            if miss:
                missing_instruments[label] = miss

            # Group-level system (equal-weight rules, etc.)
            cfg_grp = make_asset_class_config(base_cfg, inst_list)
            tmp_cfg_path = Path(tmpdir) / f"tmp_{label.replace(': ','_').replace(' ','_')}.yaml"
            save_yaml(cfg_grp, tmp_cfg_path)
            sys_grp = build_system_from_yaml(tmp_cfg_path, args.data)

            # Per-instrument combined forecasts
            per_instrument_forecasts[label] = {}
            for inst in inst_list:
                try:
                    f_ser = get_combined_forecast_series(sys_grp, inst)
                except Exception:
                    f_ser = pd.Series(dtype=float)
                per_instrument_forecasts[label][inst] = f_ser

            # Group equal-weight average forecast
            group_forecasts[label] = average_forecasts_equal_weight(per_instrument_forecasts[label])

    # ---------- Quick summary table ----------
    # Provide simple descriptive stats for the group-level forecasts
    # (mean, std, avg |forecast|, % time > +10, % time < -10)
    stats = {}
    for label, ser in group_forecasts.items():
        s = ser.dropna()
        if len(s) == 0:
            stats[label] = {"mean": np.nan, "std": np.nan, "avg_abs": np.nan, "pct_gt_10": np.nan, "pct_lt_-10": np.nan}
            continue
        n = float(len(s))
        stats[label] = {
            "mean": s.mean(),
            "std": s.std(),
            "avg_abs": s.abs().mean(),
            "pct_gt_10": (s > 10).sum() / n,
            "pct_lt_-10": (s < -10).sum() / n,
        }
    if stats:
        df_stats = pd.DataFrame(stats).T[["mean", "std", "avg_abs", "pct_gt_10", "pct_lt_-10"]]
        fmt_pct = lambda x: f"{x:.1%}" if pd.notna(x) else "—"
        printable = df_stats.copy()
        printable["pct_gt_10"] = printable["pct_gt_10"].map(fmt_pct)
        printable["pct_lt_-10"] = printable["pct_lt_-10"].map(fmt_pct)
        print(f"\n== Combined forecast stats by {'class' if (args.level or 'class')=='class' else 'sub-class'} ==")
        print(printable.to_string())

    if missing_instruments:
        print("\n[WARN] Instruments listed in map but absent from base instrument_weights:")
        for label, mis in missing_instruments.items():
            print(f"  - {label}: {', '.join(mis)}")

    # ---------- Plots ----------
    if args.plot:
        # Group-level combined forecasts
        plt.figure(figsize=(10, 5))
        for label, ser in group_forecasts.items():
            ser.plot(label=label)
        plt.title(f"Combined Forecast by {'Class' if (args.level or 'class')=='class' else 'Sub-class'} (equal-weight avg)")
        plt.xlabel("Date"); plt.ylabel("Forecast (scalar)")
        plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()

        # Per-group: each member instrument's combined forecast
        for label, inst_map in per_instrument_forecasts.items():
            if not inst_map:
                continue
            plt.figure(figsize=(10, 5))
            for inst, ser in inst_map.items():
                ser.plot(label=inst)
            plt.title(f"{label} — Instrument Combined Forecasts")
            plt.xlabel("Date"); plt.ylabel("Forecast (scalar)")
            plt.grid(True); plt.legend(title="Instrument", ncol=2); plt.tight_layout(); plt.show()

if __name__ == "__main__":
    main()
