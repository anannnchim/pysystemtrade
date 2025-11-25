#!/usr/bin/env python3
"""
check_instrument_code.py

Given a list of instrument codes, return a table of:

- Instrument (instrument code)
- IBCode        (IBSymbol from ib_config_futures.csv)
- BarchartCode  (code from CONTRACT_MAP in bcutils.config)
- TVCode        (empty for now)
- Exchange      (IBExchange from ib_config_futures.csv)
- Underlying    (Description from instrumentconfig.csv)
- AssetClass    (AssetClass from moreinstrumentinfo.csv)
- SubClass      (SubClass from moreinstrumentinfo.csv)
- Currency      (Currency from instrumentconfig.csv)

Usage (CLI):
    python check_instrument_code.py AEX AUD_micro CORN
    python check_instrument_code.py AEX AUD_micro -o /tmp/instrument_map.csv

Usage (interactive, e.g. PyCharm run button):
    python check_instrument_code.py
    # then type: AEX AUD_micro CORN
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]  # /Users/nanthawat/PycharmProjects/pysystemtrade

IB_CONFIG_PATH = PROJECT_ROOT / "sysbrokers" / "IB" / "config" / "ib_config_futures.csv"
INSTRUMENT_CONFIG_PATH = (
    PROJECT_ROOT / "data" / "futures" / "csvconfig" / "instrumentconfig.csv"
)
MORE_INSTRUMENT_INFO_PATH = (
    PROJECT_ROOT / "data" / "futures" / "csvconfig" / "moreinstrumentinfo.csv"
)

# Default CSV output path (always used if -o not specified)
DEFAULT_OUTPUT_CSV = PROJECT_ROOT / "instrument_code_check.csv"

BC_UTILS_PROJECT_ROOT = PROJECT_ROOT.parent / "bc-utils"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_ib_config() -> pd.DataFrame:
    """
    Load IB futures config and index by Instrument.
    """
    df = pd.read_csv(IB_CONFIG_PATH)
    if "Instrument" not in df.columns:
        raise ValueError(f"'Instrument' column not found in {IB_CONFIG_PATH}")
    df = df.set_index("Instrument")
    return df


def load_instrument_config() -> pd.DataFrame:
    """
    Load instrumentconfig.csv and index by Instrument.
    Provides Description (Underlying) and Currency.
    """
    df = pd.read_csv(INSTRUMENT_CONFIG_PATH)
    if "Instrument" not in df.columns:
        raise ValueError(f"'Instrument' column not found in {INSTRUMENT_CONFIG_PATH}")
    df = df.set_index("Instrument")
    return df


def load_more_instrument_info() -> pd.DataFrame:
    """
    Load moreinstrumentinfo.csv and index by Instrument.
    Provides AssetClass, SubClass, etc.
    """
    df = pd.read_csv(MORE_INSTRUMENT_INFO_PATH)
    if "Instrument" not in df.columns:
        raise ValueError(f"'Instrument' column not found in {MORE_INSTRUMENT_INFO_PATH}")
    df = df.set_index("Instrument")
    return df


def load_barchart_contract_map() -> Dict[str, Dict[str, str]]:
    """
    Load CONTRACT_MAP from bcutils.config.

    Tries normal 'bcutils' import first. If that fails, it adds
    BC_UTILS_PROJECT_ROOT to sys.path and retries.
    """
    try:
        from bcutils.config import CONTRACT_MAP  # type: ignore
        return CONTRACT_MAP  # type: ignore[name-defined]
    except ImportError:
        # Try adding the expected project path
        sys.path.append(str(BC_UTILS_PROJECT_ROOT))
        try:
            from bcutils.config import CONTRACT_MAP  # type: ignore
            return CONTRACT_MAP  # type: ignore[name-defined]
        except ImportError as e:
            raise ImportError(
                "Could not import bcutils.config.CONTRACT_MAP. "
                "Make sure bc-utils project is available or installed."
            ) from e


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def get_instrument_row(
    instrument: str,
    ib_df: pd.DataFrame,
    inst_df: pd.DataFrame,
    moreinfo_df: pd.DataFrame,
    bc_map: Dict[str, Dict[str, str]],
) -> Dict[str, Optional[str]]:
    """
    Build a single row (dict) of instrument info.
    """
    # IB info
    if instrument in ib_df.index:
        ib_symbol = str(ib_df.loc[instrument].get("IBSymbol", ""))  # type: ignore[arg-type]
        ib_exchange = str(ib_df.loc[instrument].get("IBExchange", ""))  # type: ignore[arg-type]
    else:
        ib_symbol = ""
        ib_exchange = ""

    # Instrument config (Underlying, Currency)
    if instrument in inst_df.index:
        underlying = str(inst_df.loc[instrument].get("Description", ""))  # type: ignore[arg-type]
        currency = str(inst_df.loc[instrument].get("Currency", ""))  # type: ignore[arg-type]
    else:
        underlying = ""
        currency = ""

    # More instrument info (AssetClass, SubClass)
    if instrument in moreinfo_df.index:
        asset_class = str(moreinfo_df.loc[instrument].get("AssetClass", ""))  # type: ignore[arg-type]
        sub_class = str(moreinfo_df.loc[instrument].get("SubClass", ""))  # type: ignore[arg-type]
    else:
        asset_class = ""
        sub_class = ""

    # Barchart code
    bc_entry = bc_map.get(instrument, {})
    barchart_code = str(bc_entry.get("code", ""))

    # TV code (empty for now)
    tv_code = ""

    return {
        "Instrument": instrument,
        "IBCode": ib_symbol,
        "BarchartCode": barchart_code,
        "TVCode": tv_code,
        "Exchange": ib_exchange,
        "Underlying": underlying,
        "AssetClass": asset_class,
        "SubClass": sub_class,
        "Currency": currency,
    }


def build_instrument_table(instruments: List[str]) -> pd.DataFrame:
    """
    Given a list of instrument codes, build the output DataFrame.
    """
    ib_df = load_ib_config()
    inst_df = load_instrument_config()
    moreinfo_df = load_more_instrument_info()
    bc_map = load_barchart_contract_map()

    rows: List[Dict[str, Optional[str]]] = []
    for instr in instruments:
        # Clean each instrument: strip whitespace and trailing commas
        instr = instr.strip().strip(",")
        if not instr:
            continue
        row = get_instrument_row(instr, ib_df, inst_df, moreinfo_df, bc_map)
        rows.append(row)

    df = pd.DataFrame(rows, columns=[
        "Instrument",
        "IBCode",
        "BarchartCode",
        "TVCode",
        "Exchange",
        "Underlying",
        "AssetClass",
        "SubClass",
        "Currency",
    ])

    return df


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check instrument codes against IB / Barchart / config files."
    )
    # Make instruments optional; if none given, we'll prompt interactively
    parser.add_argument(
        "instruments",
        nargs="*",
        help="Instrument codes to check (e.g., AEX AUD_micro CORN)",
    )
    parser.add_argument(
        "-o",
        "--output-csv",
        dest="output_csv",
        help="Optional path to save CSV output. "
             "If not provided, a default file will be used.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    instruments = args.instruments

    # If no instruments passed on the command line, ask interactively
    if not instruments:
        try:
            user_input = input(
                "Enter instrument codes separated by spaces or commas "
                "(e.g. AEX AUD_micro CORN or AEX,AUD_micro,CORN): "
            ).strip()
        except EOFError:
            user_input = ""

        if not user_input:
            print("No instruments provided. Exiting.", file=sys.stderr)
            return

        # Allow both comma and space separated input: normalize to spaces then split
        for sep in [",", ";"]:
            user_input = user_input.replace(sep, " ")
        instruments = [tok for tok in user_input.split() if tok]

    df = build_instrument_table(instruments)

    if df.empty:
        print("No instruments found.", file=sys.stderr)
        return

    # --- Print CSV to stdout (so you see it in terminal / PyCharm) ---
    df.to_csv(sys.stdout, index=False)

    # --- Always write CSV to file ---
    if args.output_csv:
        output_path = Path(args.output_csv).expanduser().resolve()
    else:
        output_path = DEFAULT_OUTPUT_CSV

    df.to_csv(output_path, index=False)
    print(f"\nSaved CSV to: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
