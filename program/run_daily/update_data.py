from program.helper.run_scripts import run_scripts

if __name__ == '__main__':
    # List of script file paths
    """
    1. Update by appending data in FX parquet
    2. Update expiry date in MongoDB of instruments in contract price (parquet)
    3. Update by appending data in Contract price parquet.
    4. Update by appending data in Adjusted & Multiple parquet
    """

    # 1. Update futures related data
    scripts = [
        "/Users/nanthawat/PycharmProjects/pysystemtrade/program/run_daily/run_startup.py",
        "/Users/nanthawat/PycharmProjects/pysy"
        "stemtrade/sysproduction/update_fx_prices.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_sampled_contracts.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_historical_prices.py",
        "/Users/nanthawat/PycharmProjects/pysystemtrade/sysproduction/update_multiple_adjusted_prices.py"
    ]

    # Run the scripts
    run_scripts(scripts)