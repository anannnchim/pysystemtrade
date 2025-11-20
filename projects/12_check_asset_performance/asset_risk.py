# asset_risk.py
import argparse
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


def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


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


# ---------- Risk helpers ----------
def instrument_daily_pct_vol_series(sys_obj, instrument: str) -> pd.Series:
    """
    Return a Series of daily percentage volatility for an instrument.

    Handles the different possible return types from
    sys_obj.rawdata.get_daily_percentage_volatility(instrument):

    - DataFrame: use the first column
    - Series   : use as-is
    - Scalar   : return empty Series (no time axis to align on)
    """
    daily_pct_vol = sys_obj.rawdata.get_daily_percentage_volatility(instrument)

    if daily_pct_vol is None:
        return pd.Series(dtype=float)

    if isinstance(daily_pct_vol, pd.DataFrame):
        if daily_pct_vol.empty:
            return pd.Series(dtype=float)
        vol_series = daily_pct_vol.iloc[:, 0]
    elif isinstance(daily_pct_vol, pd.Series):
        vol_series = daily_pct_vol
    else:
        # Scalar or unknown type: we can't build a meaningful curve, so return empty.
        try:
            float(daily_pct_vol)
            return pd.Series(dtype=float)
        except (TypeError, ValueError):
            return pd.Series(dtype=float)

    vol_series = vol_series.dropna().astype(float)
    vol_series.name = instrument
    return vol_series


def instrument_annual_risk_series(sys_obj, instrument: str) -> pd.Series:
    """
    Time series of annualised risk (%), using daily percentage volatility:

        annual % vol(t) = daily % vol(t) * 16
    """
    daily_pct_vol = instrument_daily_pct_vol_series(sys_obj, instrument)
    if daily_pct_vol.empty:
        return pd.Series(dtype=float)

    ann_pct_vol = daily_pct_vol * 16.0
    ann_pct_vol.name = instrument
    return ann_pct_vol


def instrument_annual_risk_pct(sys_obj, instrument: str) -> float:
    """
    Current (most recent) annualised risk in percent for an instrument,
    derived from the annual risk series.
    """
    ann_series = instrument_annual_risk_series(sys_obj, instrument)
    if ann_series.empty:
        return np.nan
    ann_series = ann_series.dropna()
    if ann_series.empty:
        return np.nan
    return float(ann_series.iloc[-1])


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
        ans = input(
            "Use data source 'db'? (choose 'db' for local DB, 'csv' for CSV files) "
            f"[{d}]: "
        ).strip().lower()
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
    p = argparse.ArgumentParser(description="Compare annualised risk by (sub)asset class.")
    p.add_argument("--config", default=DEFAULT_CONFIG, help="Base system YAML")
    p.add_argument(
        "--asset-map",
        default=DEFAULT_ASSET_MAP,
        help="YAML mapping of class -> list or class -> {sub:list}",
    )
    p.add_argument(
        "--data",
        default=DEFAULT_DATA,
        choices=["csv", "db"],
        help="Data source used to build the system",
    )

    # plot flags
    plot_group = p.add_mutually_exclusive_group()
    plot_group.add_argument(
        "--plot", dest="plot", action="store_true", help="Show plots (default)"
    )
    plot_group.add_argument(
        "--no-plot", dest="plot", action="store_false", help="Disable plots"
    )
    p.set_defaults(plot=DEFAULT_PLOT)

    # choose level (major asset vs sub-asset breakdown)
    p.add_argument(
        "--level",
        choices=["class", "sub"],
        default=None,
        help="Use 'class' for major asset level (FX, Ags, ...), "
        "'sub' for sub-asset (Em/Dev, Oil/Gas, ...).",
    )

    # optional filter (comma-separated substrings)
    p.add_argument(
        "--include",
        default="",
        help="Only run groups whose name contains any of these comma-separated terms.",
    )

    # interactive toggle
    inter = p.add_mutually_exclusive_group()
    inter.add_argument(
        "--interactive",
        dest="interactive",
        action="store_true",
        help="Prompt for choices (default)",
    )
    inter.add_argument(
        "--no-interactive",
        dest="interactive",
        action="store_false",
        help="Do not prompt; use flags/defaults",
    )
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
        args.data = ask_db_or_csv(args.data)

    base_path = Path(args.config)
    asset_map_path = Path(args.asset_map)

    if not base_path.exists():
        raise FileNotFoundError(f"Config not found: {base_path}")
    if not asset_map_path.exists():
        raise FileNotFoundError(f"Asset map not found: {asset_map_path}")

    # Load config & asset map
    base_cfg = load_yaml(base_path)
    raw_map: Dict[str, Any] = load_yaml(asset_map_path)

    groups = expand_asset_map(raw_map, level=args.level or "class")

    # optional include filter
    include_terms = [t.strip() for t in args.include.split(",") if t.strip()]
    if include_terms:
        groups = {
            k: v
            for k, v in groups.items()
            if any(t.lower() in k.lower() for t in include_terms)
        }

    # Build a single system from the base config.
    # We only need rawdata, so we don't rebuild per-group configs.
    sys_all = build_system_from_yaml(base_path, args.data)

    # Universe for sanity checks
    base_instruments = set((base_cfg.get("instrument_weights") or {}).keys())

    group_risks_pct: Dict[str, float] = {}
    per_instrument_risks_pct: Dict[str, Dict[str, float]] = {}
    per_instrument_risk_curves: Dict[str, Dict[str, pd.Series]] = {}
    group_risk_curves: Dict[str, pd.Series] = {}
    missing_instruments: Dict[str, List[str]] = {}

    # ----- Compute instrument + group risk -----
    for label, inst_list in groups.items():
        per_instrument_risks_pct[label] = {}
        per_instrument_risk_curves[label] = {}
        inst_risks_decimal: List[float] = []

        for inst in inst_list:
            if inst not in base_instruments:
                # Instrument configured in map but not in base instrument_weights
                missing_instruments.setdefault(label, []).append(inst)
                continue

            # Full annual risk curve and current point
            ann_curve_pct = instrument_annual_risk_series(sys_all, inst)
            ann_risk_pct = np.nan
            if not ann_curve_pct.empty:
                ann_curve_pct = ann_curve_pct.dropna()
                if not ann_curve_pct.empty:
                    ann_risk_pct = float(ann_curve_pct.iloc[-1])

            if np.isnan(ann_risk_pct):
                continue

            # store per-instrument risk (percent)
            per_instrument_risks_pct[label][inst] = ann_risk_pct
            # store curve
            per_instrument_risk_curves[label][inst] = ann_curve_pct
            # convert to decimal for aggregation
            inst_risks_decimal.append(ann_risk_pct / 100.0)

        # group-level current risk (simple average => ρ = 1 inside group)
        if inst_risks_decimal:
            arr = np.array(inst_risks_decimal, dtype=float)
            arr = arr[~np.isnan(arr)]
            if arr.size > 0:
                group_risk_dec = float(np.mean(arr))   # decimal vol
                group_risks_pct[label] = group_risk_dec * 100.0
            else:
                group_risks_pct[label] = np.nan
        else:
            group_risks_pct[label] = np.nan

        # group-level risk curve over time (equal-weight of instrument curves)
        inst_curves = per_instrument_risk_curves[label]
        if inst_curves:
            # Align on date, take simple mean across instruments
            df_curves = pd.concat(inst_curves.values(), axis=1)
            group_curve = df_curves.mean(axis=1, skipna=True)
            group_curve.name = label
            group_risk_curves[label] = group_curve

    # ---------- Output tables ----------
    group_df = pd.DataFrame(group_risks_pct, index=["AnnRisk_%"]).T
    group_df = group_df.sort_values("AnnRisk_%")

    fmt_pct = lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
    pretty_group = group_df.copy()
    pretty_group["AnnRisk_%"] = pretty_group["AnnRisk_%"].map(fmt_pct)

    print(
        f"\n== Annualised risk by "
        f"{'class' if (args.level or 'class')=='class' else 'sub-class'} "
        f"(simple average of instrument vols, assumes ρ = 1 within group) =="
    )
    print(pretty_group.to_string())

    if missing_instruments:
        print("\n[WARN] Instruments listed in asset map but absent from base instrument_weights:")
        for label, mis in missing_instruments.items():
            print(f"  - {label}: {', '.join(mis)}")

    # Detailed per-instrument risk table
    print("\n== Per-instrument annualised risk (%) within each group ==")
    for label, inst_risk_map in per_instrument_risks_pct.items():
        if not inst_risk_map:
            continue
        df_inst = (
            pd.Series(inst_risk_map, name="AnnRisk_%")
            .sort_values(ascending=False)
            .to_frame()
        )
        df_inst["AnnRisk_%"] = df_inst["AnnRisk_%"].map(fmt_pct)
        print(f"\n[{label}]")
        print(df_inst.to_string())

    # ---------- Plots ----------
    if args.plot and len(group_df) > 0:
        # 1) Bar plot of current group risk
        plt.figure(figsize=(10, 5))
        group_df["AnnRisk_%"].plot(kind="barh")
        plt.title(
            f"Annualised Risk by "
            f"{'Class' if (args.level or 'class')=='class' else 'Sub-class'} (%)"
        )
        plt.xlabel("Annualised risk (%)")
        plt.grid(True, axis="x", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.show()

        # 2) Group-level risk curves over time (equal-weight annual risk over time, absolute %)
        if group_risk_curves:
            plt.figure(figsize=(10, 5))
            for label, curve in group_risk_curves.items():
                curve.plot(label=label)
            plt.title(
                f"Annualised Risk over Time by "
                f"{'Class' if (args.level or 'class')=='class' else 'Sub-class'} (equal-weight, %)"
            )
            plt.xlabel("Date")
            plt.ylabel("Annualised risk (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

            # 3) Normalised group-level risk curves (each class scaled by its own mean)
            #    This removes the "equity dominates axis, bonds look flat" problem.
            df_groups = pd.concat(
                [ser for _, ser in group_risk_curves.items()],
                axis=1
            )
            df_groups.columns = list(group_risk_curves.keys())
            df_groups = df_groups.dropna(how="all", axis=1)

            if not df_groups.empty:
                means = df_groups.mean(axis=0)
                # Avoid division by zero: if mean is 0, result becomes NaN for that series
                means = means.replace(0.0, np.nan)
                norm_groups = df_groups.divide(means)

                plt.figure(figsize=(10, 5))
                for col in norm_groups.columns:
                    norm_groups[col].plot(label=col)
                plt.title(
                    f"Normalised Annualised Risk over Time by "
                    f"{'Class' if (args.level or 'class')=='class' else 'Sub-class'} "
                    "(each series / own mean)"
                )
                plt.xlabel("Date")
                plt.ylabel("Normalised risk (1.0 = long-run average)")
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()

        # 4) Per-instrument risk curves inside each group
        for label, inst_map in per_instrument_risk_curves.items():
            if not inst_map:
                continue
            plt.figure(figsize=(10, 5))
            for inst, curve in inst_map.items():
                if not curve.empty:
                    curve.plot(label=inst)
            plt.title(f"{label} — Instrument Annualised Risk over Time (%)")
            plt.xlabel("Date")
            plt.ylabel("Annualised risk (%)")
            plt.grid(True)
            plt.legend(title="Instrument", ncol=2)
            plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    main()
