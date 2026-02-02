from pathlib import Path
from program.helper.run_scripts import run_scripts


# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------

# This file: pysystemtrade/program/run_daily/run_all.py
# parents[2] -> pysystemtrade/
ROOT_DIR = Path(__file__).resolve().parents[2]


if __name__ == "__main__":
    """
    1. Update by appending data in FX parquet
    2. Update expiry date in MongoDB of instruments in contract price (parquet)
    3. Update by appending data in Contract price parquet
    4. Update by appending data in Adjusted & Multiple parquet
    """

    # --------------------------------------------------
    # 1. Update futures-related data
    # --------------------------------------------------

    scripts = [
        ROOT_DIR / "program/run_daily/run_startup.py",
        ROOT_DIR / "sysproduction/update_fx_prices.py",
        ROOT_DIR / "sysproduction/update_sampled_contracts.py",
        ROOT_DIR / "sysproduction/update_historical_prices.py",
    ]

    run_scripts([str(p) for p in scripts])

    input(
        "Check if there is a spike. "
        "If spiked, investigate before updating multiple/adjusted prices."
    )

    # # --------------------------------------------------
    # # 2. Update adjusted & multiple prices
    # # --------------------------------------------------

    scripts_2 = [
        ROOT_DIR / "sysproduction/update_multiple_adjusted_prices.py"
    ]

    run_scripts([str(p) for p in scripts_2])
