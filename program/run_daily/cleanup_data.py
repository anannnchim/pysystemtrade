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

    # 1. Update futures related data
    scripts = [
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/clean_truncate_backtest_states.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/clean_truncate_echo_files.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/clean_truncate_log_files.py",
    ]

    # Run the scripts
    run_scripts(scripts)