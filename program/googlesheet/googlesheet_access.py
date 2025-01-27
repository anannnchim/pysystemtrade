"""
This one will be used to work with Google sheet

FYI
1. Sheet must be shared to manager@automated-system-f1-th.iam.gserviceaccount.com
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

JSON_KEYFILE_PATH = '/Users/nanthawat/Desktop/key/google/system-f1-th/automated-system-f1-th-key.json'


class GoogleSheetAccess:
    def __init__(self, json_keyfile_path=None, scope=None):
        """
        Initialize the GoogleSheetAccess class.

        :param json_keyfile_path: Path to the JSON keyfile.
        :param scope: List of scopes for API access. Default uses common scopes.
        """
        self.json_keyfile_path = json_keyfile_path or JSON_KEYFILE_PATH
        self.scope = scope or SCOPE
        self.client = self.authenticate_gspread()

    def authenticate_gspread(self):
        """
        Authenticate with Google Sheets API using a service account JSON keyfile.

        :return: Authenticated gspread client.
        """
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.json_keyfile_path, self.scope)
            client = gspread.authorize(creds)
            print("Authentication successful!")
            return client
        except Exception as e:
            print(f"Error during authentication: {e}")
            raise

    def get_worksheet_data(self, sheet_url, worksheet_name):
        """
        Retrieve all records from a specific worksheet.

        :param sheet_url: URL of the Google Sheets document.
        :param worksheet_name: Name of the worksheet to access.
        :return: DataFrame containing the worksheet data.
        >>> sheet_access = GoogleSheetAccess()
        >>> df = sheet_access.get_worksheet_data(sheet_url, "sheet_name")
        """
        try:
            sheet = self.client.open_by_url(sheet_url)
            worksheet = sheet.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            if not data:
                print(f"No data found in worksheet '{worksheet_name}'.")
                return pd.DataFrame()  # Return an empty DataFrame
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error accessing worksheet '{worksheet_name}': {e}")
            return pd.DataFrame()

    def list_worksheets(self, sheet_url):
        """
        List all worksheets in the Google Sheets document.

        :param sheet_url: URL of the Google Sheets document.
        :return: List of worksheet names.

        >>> sheet_access = GoogleSheetAccess()
        >>> worksheets = sheet_access.list_worksheets(sheet_url)
        """
        try:
            sheet = self.client.open_by_url(sheet_url)
            worksheets = sheet.worksheets()
            return [ws.title for ws in worksheets]
        except Exception as e:
            print(f"Error listing worksheets: {e}")
            return []

    def write_dataframe_to_sheet(self, sheet_url, worksheet_name, df, start_cell='A1', header=False):
        """
        Write a DataFrame to a specific worksheet starting at the specified cell.

        :param sheet_url: URL of the Google Sheets document.
        :param worksheet_name: Name of the worksheet to write to.
        :param df: DataFrame to write.
        :param start_cell: Starting cell in A1 notation (default: 'A1').
        :param header: Boolean indicating whether to include the DataFrame headers. Default is True.
        """
        try:
            sheet = self.client.open_by_url(sheet_url)
            worksheet = sheet.worksheet(worksheet_name)

            # Include the index as a column in the DataFrame
            df_with_index = df.reset_index()

            # Convert datetime or Timestamp columns to string format
            for col in df_with_index.select_dtypes(include=['datetime64[ns]', 'datetimetz']).columns:
                df_with_index[col] = df_with_index[col].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Convert DataFrame to list of lists
            if header:
                data = [df_with_index.columns.values.tolist()] + df_with_index.astype(str).values.tolist()
            else:
                data = df_with_index.astype(str).values.tolist()

            # Update the worksheet with the data
            worksheet.update(start_cell, data)
            print(f"DataFrame written successfully to '{worksheet_name}' starting at {start_cell}.")
        except Exception as e:
            print(f"Error writing DataFrame to worksheet '{worksheet_name}': {e}")


# Usage example
if __name__ == "__main__":

    # Global variables
    sheet_url = 'https://docs.google.com/spreadsheets/d/13-e4A7HPIZipIGnpYDSyrtFWX6q9fQLPV3kPzsiIxXQ/edit?gid=501859678#gid=501859678'

    # Initialize the class
    sheet_access = GoogleSheetAccess()

    # Data
    df = pd.DataFrame({
        "Time": [1,2]
    })
    print(df)

    # Write to the sheet.
    sheet_access.write_dataframe_to_sheet(sheet_url, "Sheet19", df, start_cell='A1')
