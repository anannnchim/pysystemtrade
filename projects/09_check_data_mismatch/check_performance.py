#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Goal: Explain why performance differs between the SAME system config run on two different data backends (CSV vs DB).

We check:
1) System performance comparison (curves, relative-diff, drawdowns)
2) Price coverage (start/end, overlap %)
3) Instrument price differences (abs, %)
4) Costs comparison:
   - per-instrument SR cost per trade & holding cost
   - annual Gross/Costs/Net table
5) Quick look at instrument universe differences and last-date weights

Interactive pauses let you step through sections.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Dict, List

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

pd.set_option("display.max_columns", None)
plt.rcParams["figure.figsize"] = (12, 6)


# =========================
# ===== CONFIG & SYS  =====
# =========================
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/diversified_program_config.yaml"
CONFIG_PATH = "/projects/config/jumbo_config.yaml"
config = Config(CONFIG_PATH)

s_csv = futures_system(config=config, data=csvFuturesSimData())
s_db  = futures_system(config=config, data=dbFuturesSimData())


# =========================
# ======= HELPERS =========
# =========================
def _pause(msg: str):
    try:
        input(msg)
    except KeyboardInterrupt:
        print("\nAborted by user."); raise SystemExit(0)

def _curve(obj):
    try:
        return obj.curve()
    except Exception:
        return obj

def get_system_curve_percent(sys_obj) -> pd.Series:
    """Portfolio net performance in percent as a pandas Series."""
    return _curve(sys_obj.accounts.portfolio().net.percent).dropna()

def align_two(a: pd.Series, b: pd.Series, name_a="csv", name_b="db") -> pd.DataFrame:
    return pd.concat([a.rename(name_a), b.rename(name_b)], axis=1, join="inner").dropna().sort_index()

def drawdown_from_pct_curve(curve_pct: pd.Series) -> pd.Series:
    """Compute drawdown (%) from a cumulative % curve."""
    level = (1.0 + curve_pct/100.0).cumprod()
    peak = level.cummax()
    return (level/peak - 1.0) * 100.0

def get_price_series(sys_obj, instrument: str) -> pd.Series:
    """Try common accessors for a daily price series in pysystemtrade stacks."""
    candidates = [
        lambda: sys_obj.rawdata.daily_prices(instrument),
        lambda: sys_obj.rawdata.get_daily_prices(instrument),
        lambda: sys_obj.rawdata.get_instrument_price_series(instrument),
        lambda: sys_obj.rawdata.get_prices_for_instrument(instrument),
    ]
    for getter in candidates:
        try:
            ser = getter()
            if isinstance(ser, pd.Series) and not ser.empty:
                return ser.dropna()
        except Exception:
            continue
    raise AttributeError(f"Could not fetch daily price series for '{instrument}'.")

def build_price_comparison_df(instr: str) -> pd.DataFrame:
    """CSV vs DB aligned with abs/rel diffs for instrument prices."""
    price_csv = get_price_series(s_csv, instr).rename("csv_price")
    price_db  = get_price_series(s_db, instr).rename("db_price")
    df = pd.concat([price_csv, price_db], axis=1, join="inner").sort_index()
    df["abs_diff"] = df["db_price"] - df["csv_price"]
    eps = 1e-12
    denom = df["csv_price"].where(df["csv_price"].abs() > eps, eps)
    df["rel_diff_pct"] = (df["abs_diff"] / denom) * 100.0
    return df

def coverage_row(sys_a, sys_b, instr: str) -> Dict:
    """Start/end/count/overlap for each source for an instrument."""
    a = get_price_series(sys_a, instr)
    b = get_price_series(sys_b, instr)
    idx_a, idx_b = a.index, b.index
    common = idx_a.intersection(idx_b)
    union  = idx_a.union(idx_b)
    return {
        "Instrument": instr,
        "csv_start": idx_a.min(), "csv_end": idx_a.max(), "n_csv": len(idx_a),
        "db_start":  idx_b.min(), "db_end":  idx_b.max(), "n_db":  len(idx_b),
        "first_common": common.min() if len(common) else None,
        "last_common":  common.max() if len(common) else None,
        "n_common":     len(common),
        "n_csv_only":   len(idx_a.difference(idx_b)),
        "n_db_only":    len(idx_b.difference(idx_a)),
        "overlap_pct":  (len(common)/len(union)*100.0) if len(union) else 0.0,
    }

def per_instrument_costs(sys_obj, instr: str) -> Dict[str, Optional[float]]:
    """SR cost per trade & holding cost only (if available)."""
    try:
        sr_trade = float(sys_obj.accounts.get_SR_cost_per_trade_for_instrument(instr))
    except Exception:
        sr_trade = None
    try:
        sr_hold = float(sys_obj.accounts.get_SR_holding_cost_only(instr))
    except Exception:
        sr_hold = None
    return {"SR_cost_per_trade": sr_trade, "SR_holding_cost_only": sr_hold}

def annual_costs_table(sys_obj) -> Optional[pd.DataFrame]:
    try:
        p = sys_obj.accounts.portfolio()
        return pd.DataFrame({
            "Gross": p.gross.annual.percent,
            "Costs": p.costs.annual.percent,
            "Net":   p.net.annual.percent
        })
    except Exception:
        return None

def get_weights_last(sys_obj) -> Optional[pd.Series]:
    """Try to get instrument weights at the last available point."""
    try:
        w = sys_obj.portfolio.get_instrument_weights()
    except Exception:
        return None
    # If time-varying, try to pick last row; otherwise return as is
    try:
        if hasattr(w.index, "dtype") and "datetime" in str(w.index.dtype).lower():
            return w.loc[w.index.max()]
    except Exception:
        pass
    return w


# =========================
# ========= MAIN ==========
# =========================
if __name__ == "__main__":
    # Select instruments to analyze
    raw = input("Instrument code (e.g., 'EDOLLAR', 'S50', 'GOLD') or 'ALL' (Enter for ALL): ").strip()
    if not raw or raw.upper() == "ALL":
        set_csv = set(s_csv.get_instrument_list())
        set_db  = set(s_db.get_instrument_list())
        instruments = sorted(set_csv.intersection(set_db))
        if not instruments:
            raise RuntimeError("No common instruments between CSV and DB.")
        print(f"Using ALL common instruments ({len(instruments)}): {', '.join(instruments)}")
    else:
        instruments = [raw]

    th_str = input("Relative price-difference threshold (percent, default 1.0): ").strip()
    rel_th = float(th_str) if th_str else 1.0

    # 0) Quick universe check
    print("\n=== Instrument universe check ===")
    only_csv = sorted(set(s_csv.get_instrument_list()) - set(s_db.get_instrument_list()))
    only_db  = sorted(set(s_db.get_instrument_list()) - set(s_csv.get_instrument_list()))
    print("Only in CSV:", only_csv if only_csv else "—")
    print("Only in DB :", only_db  if only_db  else "—")

    # 1) System performance comparison
    _pause("\nSYSTEM performance comparison (curves, rel-diff, drawdown). Press Enter…")
    curve_csv = get_system_curve_percent(s_csv)
    curve_db  = get_system_curve_percent(s_db)
    sys_df    = align_two(curve_csv, curve_db)

    print("\nSystem curves describe():")
    print(sys_df.describe().round(4))

    # Plot curves
    ax = sys_df.plot(title="System Net % — CSV vs DB")
    ax.set_xlabel("Date"); ax.set_ylabel("%"); ax.grid(True)
    plt.tight_layout(); plt.show()

    # Relative diff (portfolio)
    eps = 1e-12
    denom = sys_df["csv"].where(sys_df["csv"].abs() > eps, eps)
    sys_rel_diff = ((sys_df["db"] - sys_df["csv"]) / denom) * 100.0
    print("\nSystem relative difference stats (DB - CSV) %:")
    print(sys_rel_diff.describe().round(4))

    ax = sys_rel_diff.plot(title="System Net % — Relative Difference (DB - CSV) %")
    ax.set_xlabel("Date"); ax.set_ylabel("%"); ax.grid(True)
    plt.tight_layout(); plt.show()

    # Drawdowns
    dd_csv = drawdown_from_pct_curve(sys_df["csv"])
    dd_db  = drawdown_from_pct_curve(sys_df["db"])
    dd_df  = pd.concat([dd_csv.rename("csv_dd"), dd_db.rename("db_dd")], axis=1)
    ax = dd_df.plot(title="System Drawdown % — CSV vs DB")
    ax.set_xlabel("Date"); ax.set_ylabel("%"); ax.grid(True)
    plt.tight_layout(); plt.show()

    # 2) Price coverage (start/end/overlap)
    _pause("\nPRICE coverage (start/end/overlap). Press Enter…")
    cov_rows = []
    for ins in instruments:
        try:
            cov_rows.append(coverage_row(s_csv, s_db, ins))
        except Exception as e:
            print(f"[{ins}] coverage failed: {e}")
    cov_df = pd.DataFrame(cov_rows).set_index("Instrument").sort_index()
    print("\n=== Price coverage (CSV vs DB) ===")
    print(cov_df)

    if len(instruments) == 1:
        ins = instruments[0]
        a = get_price_series(s_csv, ins); b = get_price_series(s_db, ins)
        only_a = a.index.difference(b.index); only_b = b.index.difference(a.index)
        if len(only_a):
            print(f"\nDates ONLY in CSV ({len(only_a)}). First 10:"); print(pd.Index(only_a).sort_values()[:10])
            print("Last 10:"); print(pd.Index(only_a).sort_values()[-10:])
        else:
            print("\nNo exclusive CSV dates.")
        if len(only_b):
            print(f"\nDates ONLY in DB ({len(only_b)}). First 10:"); print(pd.Index(only_b).sort_values()[:10])
            print("Last 10:"); print(pd.Index(only_b).sort_values()[-10:])
        else:
            print("\nNo exclusive DB dates.")
        # optional tiny availability plot
        try:
            union = pd.date_range(start=min(a.index.min(), b.index.min()),
                                  end=max(a.index.max(), b.index.max()), freq="D")
            m = pd.DataFrame(index=union)
            m["CSV"] = m.index.isin(a.index).astype(int)
            m["DB"]  = m.index.isin(b.index).astype(int)
            ax = m["CSV"].rolling(7, min_periods=1).mean().plot(title=f"{ins} — Availability (7d rolling mean)")
            m["DB"].rolling(7, min_periods=1).mean().plot(ax=ax)
            ax.set_xlabel("Date"); ax.set_ylabel("Availability (0–1)")
            ax.grid(True); plt.tight_layout(); plt.show()
        except Exception as e:
            print("Availability plot unavailable:", e)

    # 3) Price differences by instrument (abs / %)
    _pause("\nINSTRUMENT price differences. Press Enter…")
    price_summary = []
    for ins in instruments:
        try:
            dfp = build_price_comparison_df(ins)
            stats = dfp[["abs_diff", "rel_diff_pct"]].describe().round(6)
            print(f"\n[{ins}] price diff stats:\n", stats)
            # flag big diffs
            big = dfp[dfp["rel_diff_pct"].abs() >= rel_th]
            if len(big):
                print(f"  ⚠ {len(big)} rows with |rel_diff_pct| >= {rel_th:.2f}% (showing up to 10):")
                print(big[["csv_price", "db_price", "abs_diff", "rel_diff_pct"]].head(10))
            price_summary.append({
                "Instrument": ins,
                "n_common": len(dfp),
                "mean_abs_rel_diff_%": dfp["rel_diff_pct"].abs().mean(),
                "max_abs_rel_diff_%":  dfp["rel_diff_pct"].abs().max(),
            })
        except Exception as e:
            print(f"[{ins}] price comparison failed: {e}")

    if price_summary:
        price_sum_df = pd.DataFrame(price_summary).set_index("Instrument").sort_values("max_abs_rel_diff_%", ascending=False)
        print("\n=== Price diff summary (by instrument) ===")
        print(price_sum_df.round(4))

    # 4) COSTS: per-instrument SR costs + annual Gross/Costs/Net
    _pause("\nCOSTS comparison. Press Enter…")
    cost_rows = []
    for ins in instruments:
        c_csv = per_instrument_costs(s_csv, ins)
        c_db  = per_instrument_costs(s_db,  ins)
        cost_rows.append({
            "Instrument": ins,
            "csv_SR_cost_per_trade": c_csv["SR_cost_per_trade"],
            "db_SR_cost_per_trade":  c_db["SR_cost_per_trade"],
            "csv_SR_holding_cost_only": c_csv["SR_holding_cost_only"],
            "db_SR_holding_cost_only":  c_db["SR_holding_cost_only"],
        })
    cost_df = pd.DataFrame(cost_rows).set_index("Instrument")
    print("\n=== Per-instrument SR costs ===")
    print(cost_df.round(6))

    # Annual costs table (portfolio level)
    ann_csv = annual_costs_table(s_csv)
    ann_db  = annual_costs_table(s_db)
    if ann_csv is not None and ann_db is not None:
        ann_cmp = pd.concat(
            [ann_csv.rename(columns=lambda c: f"csv_{c}"),
             ann_db.rename(columns=lambda c: f"db_{c}")],
            axis=1, join="inner"
        ).sort_index()
        print("\n=== Annual Gross/Costs/Net (common years) ===")
        print(ann_cmp.round(4))
        print("\nAverages over common years:")
        print(ann_cmp.mean().round(4))
    else:
        print("\nAnnual costs table not available in one or both systems.")

    # 5) Weights at last common date (sanity check)
    _pause("\nWEIGHTS at last common date (rough check). Press Enter…")
    try:
        last_dt = sys_df.index.max()
        w_csv = get_weights_last(s_csv)
        w_db  = get_weights_last(s_db)
        if isinstance(w_csv, pd.Series) and isinstance(w_db, pd.Series):
            # If time-varying with DateTimeIndex, try to locate last date
            try:
                if hasattr(w_csv.index, "dtype") and "datetime" in str(w_csv.index.dtype).lower():
                    w_csv = w_csv.loc[last_dt]
            except Exception:
                pass
            try:
                if hasattr(w_db.index, "dtype") and "datetime" in str(w_db.index.dtype).lower():
                    w_db = w_db.loc[last_dt]
            except Exception:
                pass
            w_cmp = pd.concat([w_csv.rename("csv_w"), w_db.rename("db_w")], axis=1).fillna(0.0)
            w_cmp["delta_w"] = w_cmp["db_w"] - w_cmp["csv_w"]
            print(w_cmp.sort_values("db_w", ascending=False).round(4).head(30))
        else:
            print("Weights not available in both systems.")
    except Exception as e:
        print("Weights comparison failed:", e)

    # 6) Quick “Likely Causes” summary
    print("\n================ Likely Causes Summary ================")
    # Price coverage risk
    if not cov_df.empty:
        low_overlap = cov_df[cov_df["overlap_pct"] < 95]
        if not low_overlap.empty:
            print(f"- Low price overlap in {len(low_overlap)}/{len(cov_df)} instruments (overlap < 95%).")
    # Large price diffs
    if price_summary:
        many_big = [r for r in price_summary if r["max_abs_rel_diff_%"] and r["max_abs_rel_diff_%"] >= rel_th]
        if many_big:
            print(f"- Large per-instrument price differences seen in {len(many_big)} instruments (>= {rel_th:.2f}% rel diff).")
    # Cost diffs
    if not cost_df.empty:
        diffs = (cost_df["csv_SR_cost_per_trade"] != cost_df["db_SR_cost_per_trade"]) | \
                (cost_df["csv_SR_holding_cost_only"] != cost_df["db_SR_holding_cost_only"])
        if diffs.any():
            print("- Per-instrument SR costs differ between CSV and DB sources.")
    # System-level differences
    if not sys_rel_diff.empty and sys_rel_diff.abs().median() > 0.05:
        print(f"- System curve relative difference median is {sys_rel_diff.abs().median():.3f}% — investigate above drivers.")
    print("=======================================================\n")

    # Optional export
    save = input("Export all tables (coverage, price diffs summary, per-instrument costs, annual tables, system diffs)? [y/N]: ").strip().lower()
    if save in ("y", "yes"):
        outdir = Path.cwd() / "csv_vs_db_diagnostics"
        outdir.mkdir(parents=True, exist_ok=True)
        sys_df.to_csv(outdir / "system_curves.csv")
        sys_rel_diff.to_csv(outdir / "system_relative_diff_pct.csv")
        dd_df.to_csv(outdir / "system_drawdowns.csv")
        cov_df.to_csv(outdir / "price_coverage.csv")
        if price_summary:
            price_sum_df.to_csv(outdir / "price_diff_summary.csv")
        cost_df.to_csv(outdir / "per_instrument_sr_costs.csv")
        if ann_csv is not None and ann_db is not None:
            ann_cmp.to_csv(outdir / "annual_gross_costs_net.csv")
        print(f"Saved -> {outdir}")
