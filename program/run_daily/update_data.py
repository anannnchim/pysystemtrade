import subprocess
# import os
'''
This one will update futures database
'''


def run_scripts(scripts):
    """
    Run a list of Python scripts sequentially.
    :param scripts: List of script file paths to execute.
    """
    for script in scripts:
        try:
            print(f"Running script: {script}")
            subprocess.run(["python", script], check=True)
            print(f"Completed: {script}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error while running script {script}: {e}")
            break


if __name__ == '__main__':
    # List of script file paths
    """
    1. Update by appending data in FX parquet
    2. Update expiry date in MongoDB of instruments in contract price (parquet)
    3. Update by appending data in Contract price parquet.
    4. Update by appending data in Adjusted & Multiple parquet
    """

    # Update futures related data

    scripts = [
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_fx_prices.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_sampled_contracts.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_historical_prices.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_multiple_adjusted_prices.py"
    ]

    # Run the scripts
    run_scripts(scripts)