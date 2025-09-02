#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

pd.set_option("display.max_columns", None)

CONFIG_PATHS: Dict[str, str] = {
    "f1": "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml",
    "diversified": "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/run_backtest/diversified_program_config.yaml",
}

MENU = """
================== MENU ==================
1) Plot P&L % curve by instrument
2) Plot Portfolio Net %
3) Show portfolio stats
4) Check annualised risk gate
5) Show costs table
6) Show portfolio stdev table
7) Change options (tail / save plots / instruments)
0) Exit
==========================================
"""

def prompt_choice(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
    choices_str = "/".join(choices)
    while True:
        raw = input(f"{prompt} [{choices_str}]{' (default: ' + default + ')' if default else ''}: ").strip().lower()
        if not raw and default:
            return default
        if raw in choices:
            return raw
        print(f"Please choose one of: {choices_str}")

def prompt_bool(prompt: str, default: bool = False) -> bool:
    while True:
        raw = input(f"{prompt} [y/n]{' (default: ' + ('y' if default else 'n') + ')' if default is not None else ''}: ").strip().lower()
        if not raw and default is not None:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please type y or n.")

def prompt_int_or_none(prompt: str, default: Optional[int] = None, min_val: Optional[int] = None) -> Optional[int]:
    while True:
        raw = input(f"{prompt} (enter to skip){' [default: ' + str(default) + ']' if default is not None else ''}: ").strip()
        if raw == "":
            return default
        try:
            v = int(raw)
            if min_val is not None and v < min_val:
                print(f"Please enter an integer >= {min_val}")
                continue
            return v
        except ValueError:
            print("Please enter an integer or press Enter to skip.")

def prompt_path_or_none(prompt: str, default: Optional[str] = None) -> Optional[Path]:
    raw = input(f"{prompt} (directory; Enter to skip){' [default: ' + default + ']' if default else ''}: ").strip()
    if not raw:
        return Path(default) if default else None
    p = Path(raw).expanduser()
    try:
        p.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Cannot create directory {p}: {e}")
        return None
    return p

def pick_instruments(all_instr: List[str]) -> List[str]:
    print("\nAvailable instruments:")
    print(", ".join(all_instr))
    print("Pick a subset (comma-separated), or press Enter to use ALL.")
    raw = input("Instruments: ").strip()
    if not raw:
        return all_instr
    wanted = [r.strip() for r in raw.split(",") if r.strip()]
    valid = [i for i in wanted if i in all_instr]
    missing = [i for i in wanted if i not in all_instr]
    if missing:
        print(f"Ignored (not found): {', '.join(missing)}")
    return valid or all_instr

def build_system(db_choice: str, system_choice: str):
    if db_choice == "db":
        data = dbFuturesSimData()
    elif db_choice == "csv":
        data = csvFuturesSimData()
    else:
        raise ValueError("db must be 'db' or 'csv'.")

    cfg_path = CONFIG_PATHS[system_choice]
    if not Path(cfg_path).exists():
        raise FileNotFoundError(f"Config not found: {cfg_path}")

    cfg = Config(cfg_path)
    return futures_system(config=cfg, data=data)

def plot_instrument_pnls(sys, instruments: List[str], tail: Optional[int], save_dir: Optional[Path]):
    plt.figure(figsize=(12, 6))
    for instr in instruments:
        curve = sys.accounts.pandl_for_instrument(instr).percent.curve()
        if tail is not None and tail > 0:
            curve = curve.tail(tail)
        plt.plot(curve, label=instr)
    plt.title("P&L Percentage Curve by Instrument")
    plt.xlabel("Date")
    plt.ylabel("P&L %")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save_dir:
        out = save_dir / "instrument_pnls.png"
        plt.savefig(out, dpi=150)
        print(f"Saved -> {out}")
        plt.close()
    else:
        plt.show()

def plot_portfolio(sys, tail: Optional[int], save_dir: Optional[Path]):
    curve = sys.accounts.portfolio().net.percent.curve()
    if tail is not None and tail > 0:
        curve = curve.tail(tail)
    ax = curve.plot(figsize=(12, 5), grid=True, title="Portfolio Net %")
    ax.set_xlabel("Date")
    ax.set_ylabel("P&L %")
    plt.tight_layout()
    if save_dir:
        out = save_dir / "portfolio_net_percent.png"
        plt.savefig(out, dpi=150)
        print(f"Saved -> {out}")
        plt.close()
    else:
        plt.show()

def print_portfolio_stats(sys):
    stats = sys.accounts.portfolio().percent.stats()
    try:
        df = pd.DataFrame(stats).T if not isinstance(stats, pd.DataFrame) else stats
    except Exception:
        df = pd.DataFrame.from_dict(stats, orient="index")
    print("\n=== Portfolio Stats (percent) ===")
    print(df)

def check_annualised_risk(sys, threshold: float = 5.0, instruments: Optional[List[str]] = None):
    print("\n=== Annualised Risk Check ===")
    instrs = instruments or sys.get_instrument_list()
    for instrument in instrs:
        ann_risk = sys.rawdata.get_daily_percentage_volatility(instrument).mean() * 16
        status = "PASS" if ann_risk >= threshold else "Too safe to trade. Remove"
        print(f"{instrument}: {ann_risk:.4f}% -> {status}")

def collect_costs(sys, instruments: Optional[List[str]] = None) -> pd.DataFrame:
    print("\n=== Costs (per instrument) ===")
    rows = {}
    instrs = instruments or sys.get_instrument_list()
    for instrument in instrs:
        try:
            raw_cost = sys.rawdata.get_raw_cost_data(instrument)
        except Exception as e:
            logging.warning(f"Failed raw cost for {instrument}: {e}")
            raw_cost = None
        rows[instrument] = {
            "Multiplier": sys.rawdata.get_value_of_block_price_move(instrument),
            "rolls_per_year": sys.rawdata.rolls_per_year(instrument),
            "SR_cost_per_trade": sys.accounts.get_SR_cost_per_trade_for_instrument(instrument),
            "SR_holding_cost_only": sys.accounts.get_SR_holding_cost_only(instrument),
            "raw_cost": raw_cost,
        }
        print(f"{instrument}: {raw_cost}")
    return pd.DataFrame.from_dict(rows, orient="index")

def show_portfolio_stdev(sys):
    print("\n=== Portfolio StDev (% by index) ===")
    df = sys.portfolio.get_stdev_df() * 100
    print(df)

def main():
    print("=== Interactive Futures System Diagnostics ===\n(press Ctrl+C anytime to exit)\n")
    logging.basicConfig(level=logging.INFO)

    try:
        # Step 1: pick data backend
        db_choice = prompt_choice("1) Select database", ["db", "csv"], default="db")

        # Step 2: pick system config
        system_choice = prompt_choice("2) Select system", ["f1", "diversified"], default="f1")

        # Step 3: optional options
        tail = prompt_int_or_none("Show only last N points (tail)", default=None, min_val=1)
        save_plots = prompt_bool("Save plots to a folder instead of showing?", default=False)
        save_dir = prompt_path_or_none("Directory to save plots", default="./out") if save_plots else None

        # Build system
        sys_obj = build_system(db_choice, system_choice)
        all_instr = sys_obj.get_instrument_list()
        picked_instr = pick_instruments(all_instr)

        # Annualised risk threshold
        risk_threshold_input = prompt_int_or_none("Annualised risk threshold % (default 5)", default=5, min_val=0)
        risk_threshold = float(risk_threshold_input) if risk_threshold_input is not None else 5.0

        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "1":
                plot_instrument_pnls(sys_obj, picked_instr, tail, save_dir)
            elif choice == "2":
                plot_portfolio(sys_obj, tail, save_dir)
            elif choice == "3":
                print_portfolio_stats(sys_obj)
            elif choice == "4":
                check_annualised_risk(sys_obj, threshold=risk_threshold, instruments=picked_instr)
            elif choice == "5":
                df_costs = collect_costs(sys_obj, instruments=picked_instr)
                print("\n=== Costs Table ===")
                print(df_costs)
            elif choice == "6":
                show_portfolio_stdev(sys_obj)
            elif choice == "7":
                # change options interactively
                tail = prompt_int_or_none("New tail (Enter to keep current)", default=tail, min_val=1)
                save_plots = prompt_bool("Save plots to a folder?", default=save_plots)
                save_dir = prompt_path_or_none("Directory to save plots", default=str(save_dir) if save_dir else "./out") if save_plots else None
                picked_instr = pick_instruments(all_instr)
                risk_threshold_input = prompt_int_or_none("Annualised risk threshold %", default=int(risk_threshold), min_val=0)
                risk_threshold = float(risk_threshold_input) if risk_threshold_input is not None else risk_threshold
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Unknown choice. Please try again.")

    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
