#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

# Optional Pandas display settings if desired:
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.expand_frame_repr', False)

def main():
    # Prompt the user for the symbol first
    symbol = input("Enter the symbol (e.g. ETHER-micro, CORN): ").strip()

    while True:
        print("\nChoose data to print:")
        print(" 1) contract  - Contract price (user-specified date)")
        print(" 2) roll      - Roll calendars")
        print(" 3) multiple  - Multiple price")
        print(" 4) adjusted  - Adjusted price")
        print(" 5) exit      - Quit the program\n")

        choice = input("Enter your choice: ").lower().strip()

        # Exit condition
        if choice in ["exit", "5", "q"]:
            print("Exiting program...")
            break

        elif choice in ["1", "contract"]:
            # Prompt for the contract date, e.g. "202501" -> "20250100"
            contract_date = input("Enter the contract date (e.g. 202501 for 20250100): ").strip()
            contract_date_full = contract_date + "00"  # Append "00" to match file pattern

            print(f"\nContract price for {contract_date} ------------")
            # Construct path for the contract price file
            contract_path = (
                f"/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/"
                f"futures_contract_prices/Hour@{symbol}#{contract_date_full}.parquet"
            )
            try:
                df_contract = pd.read_parquet(contract_path)
                print(df_contract)
            except FileNotFoundError:
                print(f"Error: File not found at {contract_path}")

        elif choice in ["2", "roll"]:
            print("\nRoll calendars ------------")
            # Construct path for the roll calendars CSV
            roll_path = (
                f"/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/"
                f"roll_calendars/{symbol}.csv"
            )
            try:
                df_roll = pd.read_csv(roll_path)
                print(df_roll)
            except FileNotFoundError:
                print(f"Error: File not found at {roll_path}")

        elif choice in ["3", "multiple"]:
            print("\nMultiple price ------------")
            # Construct path for the multiple prices Parquet
            multiple_path = (
                f"/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/"
                f"futures_multiple_prices/{symbol}.parquet"
            )
            try:
                df_multiple = pd.read_parquet(multiple_path)
                print(df_multiple)
            except FileNotFoundError:
                print(f"Error: File not found at {multiple_path}")

        elif choice in ["4", "adjusted"]:
            print("\nAdjusted price ------------")
            # Construct path for the adjusted prices Parquet
            adjusted_path = (
                f"/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/"
                f"futures_adjusted_prices/{symbol}.parquet"
            )
            try:
                df_adjusted = pd.read_parquet(adjusted_path)
                print(df_adjusted)
            except FileNotFoundError:
                print(f"Error: File not found at {adjusted_path}")

        else:
            print(f"Invalid choice: '{choice}'. Please choose one of the options above.")

if __name__ == "__main__":
    main()
