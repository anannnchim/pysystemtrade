from pathlib import Path
from program.helper.run_scripts import run_scripts


# --------------------------------------------------
# Resolve project root dynamically
# --------------------------------------------------

# This file location example:
# pysystemtrade/program/run_daily/run_capital_and_orders.py
# parents[2] -> pysystemtrade/
ROOT_DIR = Path(__file__).resolve().parents[2]


if __name__ == "__main__":
    """
    1. Update total capital
    2. Update strategy capital
    3. Update system backtest
    4. Generate instrument orders
    """

    scripts = [
        ROOT_DIR / "sysproduction/update_total_capital.py",
        ROOT_DIR / "sysproduction/update_strategy_capital.py",
        ROOT_DIR / "sysproduction/update_system_backtests.py",
        ROOT_DIR / "sysproduction/update_strategy_orders.py",

        # Might run separately
        # ROOT_DIR / "sysproduction/run_stack_handler.py",
    ]

    # Convert Path -> str (subprocess-safe)
    run_scripts([str(p) for p in scripts])
