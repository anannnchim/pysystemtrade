#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run the small-system optimiser:
- Builds a futures_system from your config
- Greedily selects instruments to maximise portfolio SR
- Prints the chosen instruments and suggested max positions

Edit `config_path` below to point at your config.
"""

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
# If you use DB instead, swap the next line:
# from sysdata.sim.db_futures_sim_data import dbFuturesSimData

from systems.provided.futures_chapter15.basesystem import futures_system
from systems.provided.static_small_system_optimise.optimise_small_system import (
    find_best_ordered_set_of_instruments,
    get_correlation_matrix,
    SR_for_instrument_list,
)


def build_system(config_path: str):
    """Load data + config, build the system, and warm up key caches."""
    # 1) Load data and config
    data = csvFuturesSimData()
    # data = dbFuturesSimData()  # uncomment if you use DB
    config = Config(config_path)

    # 2) Build the system
    system = futures_system(data=data, config=config)

    # 3) (Optional) “warm up” some pipeline parts so later calls are faster
    # Touch components used by optimiser to ensure caches are primed
    _ = system.combForecast.get_forecast_cap()
    _ = system.positionSize.avg_abs_forecast()
    ins_list = system.get_instrument_list()
    if ins_list:
        _ = system.accounts.get_SR_cost_per_trade_for_instrument(ins_list[0])

    return system


def main():
    # >>>>>> EDIT THIS to your config file <<<<<<
    config_path = "/projects/config/production/diversified.yaml"

    system = build_system(config_path)

    # Parameters you might want to tune
    capital = 500000                  # sets system.config.notional_trading_capital
    max_instrument_weight = 0.05       # per-instrument risk cap in IDM terms
    starting_idm = 1.0                 # notional diversification multiplier ceiling for weights

    # Step 1: get best-ordered set of instruments (greedy SR adding)
    # NOTE: Don't pass corr_matrix=None; let the function compute it internally.
    chosen = find_best_ordered_set_of_instruments(
        system=system,
        max_instrument_weight=max_instrument_weight,
        notional_starting_IDM=starting_idm,
        capital=capital,
    )
    print("\nSelected instruments (in order):")
    print(", ".join(chosen) if chosen else "(none)")

    if not chosen:
        return

    # Step 2: show suggested position sizes and portfolio SR for the final set
    corr = get_correlation_matrix(system)
    sizes, sr = SR_for_instrument_list(
        system=system,
        corr_matrix=corr,
        instrument_list=chosen,
        minimum_instrument_weight_idm=max_instrument_weight * starting_idm,
    )

    print(f"\nEstimated portfolio SR: {sr:.2f}")
    print("Suggested maximum positions per instrument (contracts approx.):")
    for ins in chosen:
        qty = sizes.get(ins, 0)
        print(f"  {ins:15s}  {qty}")


if __name__ == "__main__":
    main()
