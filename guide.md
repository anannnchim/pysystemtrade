# Notebook

# Data

1. Parquet
- FX price
- contract price
- multiple price 
- adjusted price

2. CSV
- Roll calenders

3. Database
- spread_costs


# Process


1. Run all day

- stack handler
- capital update processes.

2. Run once a day
 run_daily_price_updates, run_systems, run_strategy_order_generator, run_cleaners, run_backups, run_reports
 




# Example of  how to execute 
python3 -m sysproduction.run_stack_handler

# Test one 
#!/bin/bash
source /Users/nanthawat/PycharmProjects/AnanCapitalFund/project_env.sh
python3 -m sysproduction.run_stack_handler.run_stack_handler


# Run this in terminal 
source /Users/nanthawat/PycharmProjects/pysystemtrade/project_env.sh
/bin/bash /Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/mac/scripts/update_fx_prices


# Overview 
startup()   

run_daily_fx_and_contract_updates: 07:00
- update_fx_prices
- update_sampled_contracts

run_daily_prices_updates: 20:00
- update_historical_prices

run_daily_update_multiple_adjusted_prices: 23:00
- update_multiple_adjusted_prices

run_capital_update: 01:00 ** RUN ALL DAY
- update_total_capital
- update_strategy_capital

run_systems: 20:05
- update_system_backtests

run_strategy_order_generator: 20:10 
- update_strategy_orders 

run_stack_handler: 00:01 *** RUN ALL DAY
- many 

run_backups: 20:15
run_cleaners: 20:20
run_reports: 20:25


# More details 
process_configuration_methods:
  run_capital_update:
    update_total_capital: # every 2 hours throughout the day; in a crisis I like to keep an eye on my account value
      frequency: 120
      max_executions: 10 # nominal figure, since uptime is a little less than 20 hours
    strategy_allocation:
      max_executions: 1 # don't bother updating more often than we run backtests
  run_daily_prices_updates: # all this stuff happens once. the order matters.
    update_fx_prices:
      max_executions: 1
    update_sampled_contracts:
      max_executions: 1
    update_historical_prices:
      max_executions: 1
    update_multiple_adjusted_prices:
      max_executions: 1
  run_stack_handler: # frequency 0 and max_executions -1 means we just keep doing them over and over again until the process stops...
    refresh_additional_sampling_all_instruments:
      frequency: 60
      max_executions: -1
    check_external_position_break:
      frequency: 0
      max_executions: -1
    spawn_children_from_new_instrument_orders:
      frequency: 0
      max_executions: -1
    generate_force_roll_orders:
      frequency: 0
      max_executions: 1
    create_broker_orders_from_contract_orders:
      frequency: 0
      max_executions: -1
    process_fills_stack:
      frequency: 0
      max_executions: -1
    handle_completed_orders:
      frequency: 0
      max_executions: -1
    safe_stack_removal:
      run_on_completion_only: True   # only run this once we're done
  run_reports:  # all this stuff happens once.
    costs_report:
      max_executions: 1
    liquidity_report:
      max_executions: 1
    status_report:
      max_executions: 1
    roll_report:
      max_executions: 1
    daily_pandl_report:
      max_executions: 1
    reconcile_report:
      max_executions: 1
    trade_report:
      max_executions: 1
  run_backups:
    backup_arctic_to_csv:
      max_executions: 1
    backup_files:
      max_executions: 1
    backup_mongo_data_as_dump:
      max_executions: 1
  run_cleaners:  # all this stuff happens once.
    clean_backtest_states:
      max_executions: 1
    clean_echo_files:
      max_executions: 1
    clean_log_files:
      max_executions: 1


# Backtest 

- Live production backtest:
    - Create a yaml config file to run the live production 'backtest'. For speed I recommend you do not estimate parameters, but use fixed parameters, using the [yaml_config_with_estimated_parameters method of systemDiag](/systems/diagoutput.py) function to output these to a .yaml file.
- Scheduling: