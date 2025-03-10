from program.helper.run_scripts import run_scripts

if __name__ == '__main__':
    # List of script file paths
    """
    1. Update total capital
    2. Update strategy capital
    3. Update system backtest
    4. Generate instrument order
    """

    # 1. Update futures related data
    scripts = [
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_total_capital.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_strategy_capital.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_system_backtests.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_strategy_orders.py",

        # Might run separately
        # "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/run_stack_handler.py"
    ]

    # Run the scripts
    run_scripts(scripts)