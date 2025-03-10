from program.helper.run_scripts import run_scripts

if __name__ == '__main__':

    # 1. Update futures related data
    scripts = [
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/clean_truncate_backtest_states.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/clean_truncate_echo_files.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/clean_truncate_log_files.py",
    ]

    # Run the scripts
    run_scripts(scripts)