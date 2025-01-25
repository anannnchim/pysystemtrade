import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os


def authenticate_gspread(json_keyfile_path, scope):
    """
    Authenticate with Google Sheets API using a service account JSON keyfile.

    :param json_keyfile_path: Path to the JSON keyfile.
    :param scope: List of scopes for API access.
    :return: Authenticated gspread client.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)
    return client


def get_worksheet_data(client, sheet_url, worksheet_name):
    """
    Retrieve all records from a specific worksheet.

    :param client: Authenticated gspread client.
    :param sheet_url: URL of the Google Sheets document.
    :param worksheet_name: Name of the worksheet to access.
    :return: DataFrame containing the worksheet data.
    """
    try:
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        if not data:
            print(f"No data found in worksheet '{worksheet_name}'.")
            return None
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error accessing worksheet '{worksheet_name}': {e}")
        return None


def process_data(df):
    """
    Process the DataFrame by selecting required columns, converting data types, and formatting dates.

    :param df: DataFrame to process.
    :return: Processed DataFrame.
    """
    required_columns = ['date', 'adj_price']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns in data: {missing_columns}")
        return None

    df_selected = df[required_columns].copy()

    # Convert 'date' to datetime
    df_selected['date'] = pd.to_datetime(df_selected['date'], errors='coerce')

    # Convert 'adj_price' to numeric
    df_selected['adj_price'] = pd.to_numeric(df_selected['adj_price'], errors='coerce')

    # Drop rows with NaN values
    df_selected.dropna(inplace=True)

    # Rename columns
    df_selected.rename(columns={'date': 'DATETIME', 'adj_price': 'price'}, inplace=True)

    # Format 'DATETIME' column
    df_selected['DATETIME'] = df_selected['DATETIME'].dt.strftime('%Y-%m-%d')

    # Reset index
    df_selected.reset_index(drop=True, inplace=True)

    return df_selected


def save_to_csv(df, filename, output_dir):
    """
    Save the DataFrame to a CSV file in the specified directory.

    :param df: DataFrame to save.
    :param filename: Name of the CSV file.
    :param output_dir: Directory where the CSV file will be saved.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(output_dir, filename)

        # Save the DataFrame to CSV
        df.to_csv(file_path, index=False)

        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")


def main():

    # Global variables
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    market_data_url = 'https://docs.google.com/spreadsheets/d/19Rj7iW5xWOe6ZJJRsO9VzsZXyLfFu1S_vtClEE_3DEw'
    json_keyfile_path = '/Users/nanthawat/Desktop/key/google/system-f1-th/automated-system-f1-th-key.json'

    # Output directory
    output_dir = '/Users/nanthawat/PycharmProjects/pysystemtrade/data/futures/adjusted_prices_csv'

    # Authenticate with Google Sheets
    client = authenticate_gspread(json_keyfile_path, scope)

    # List of worksheets to process
    worksheets = ['S50_py', 'USD_py', 'GF10_py']

    # Process each worksheet
    for sheet_name in worksheets:
        print(f"\nProcessing worksheet: {sheet_name}")
        df = get_worksheet_data(client, market_data_url, sheet_name)
        if df is not None:
            df_processed = process_data(df)
            if df_processed is not None:
                # Remove "_py" from the sheet name for the CSV filename
                csv_filename = f"{sheet_name.replace('_py', '')}.csv"
                save_to_csv(df_processed, csv_filename, output_dir)

if __name__ == "__main__":

    main()
