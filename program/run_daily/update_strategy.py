import subprocess
# import os
'''
This one will update strategy. 
'''


def run_scripts(scripts):
    """
    Run a list of Python scripts sequentially.
    :param scripts: List of script file paths to execute.
    """
    for script in scripts:
        try:
            print(f"Running script: {script}")
            subprocess.run(["python3", script], check=True)
            print(f"Completed: {script}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error while running script {script}: {e}")
            break


if __name__ == '__main__':
    # List of script file paths
    """
    1. Update total capital
    2. Update strategy capital
    3. Update system backtest
    4. Update by appending data in Adjusted & Multiple parquet
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