import os
import pandas as pd
from datetime import datetime
from program.googlesheet.googlesheet_access import GoogleSheetAccess
from sysdata.mongodb.mongo_margin import mongoMarginData
from sysdata.parquet.parquet_access import ParquetAccess
from sysdata.parquet.parquet_capital import parquetCapitalData
from private.gg_config_path import csv_gg_path, parquet_store


sheet_access = GoogleSheetAccess()
parquet_access = ParquetAccess(parquet_store)
capital_data = parquetCapitalData(parquet_access)
mongo_margin_data = mongoMarginData()



def update_market_monitoring(s, sheet_url):
    """
    Updates market monitoring data in Google Sheets.
    """
    df = pd.DataFrame({
        instrument: s.combForecast.get_combined_forecast(instrument)
        for instrument in s.get_instrument_list()
    })

    # Remove NA (in case we update data late, Japan already have new data but US doesn't)
    df = df.dropna()


    df = df.tail(252)  # Keep last 252 rows (1 year of trading days)


    sheet_access.write_dataframe_to_sheet(sheet_url, "A-Forecast", df, start_cell="B21", header=True)


def update_portfolio_monitoring(s, sheet_url):

    # 1. Target position # FIXME (This should get actual position)
    df_1 = {}
    for instr in s.get_instrument_list():
        df_1[instr] = s.accounts.get_buffered_position(instr)  # which one to use?
    df_1 = pd.DataFrame(df_1).dropna().tail(1)

    # 2. % Annual Risk
    df_2 = s.portfolio.get_stdev_df().tail(1)

    # 3. Notional Exposure # FIXME Need to reflect acutal pos
    df_3 = {}
    for instr in s.get_instrument_list():
        value_per_cont = s.portfolio.get_baseccy_value_per_contract(instr)
        num_of_holdings = s.accounts.get_buffered_position(instr)
        df_3[instr] = abs(value_per_cont * num_of_holdings)
    df_3 = pd.DataFrame(df_3).dropna().tail(1)


    # 4. Correlation matrix
    corr_df = s.portfolio.get_instrument_correlation_matrix().corr_list[-1].values
    labels = s.get_instrument_list()
    corr_df = pd.DataFrame(corr_df, index=labels, columns=labels)

    # 5. Last updated price
    df_4 = {}
    for instr in s.get_instrument_list():
        df_4[instr] = s.rawdata.get_daily_prices(instr)  # which one to use?
    df_4 = pd.DataFrame(df_4).dropna().tail(1)

    # Combine
    df = pd.concat([df_1, df_2, df_3, df_4])

    # Send data to sheet
    sheet_access.write_dataframe_to_sheet(sheet_url, "B-Monitoring", df, start_cell="C22", header=True)
    sheet_access.write_dataframe_to_sheet(sheet_url, "B-Monitoring", corr_df, start_cell="D30", header=True)


def update_accounting_ib(sheet_url, account_summary):

    # This will update globally data.

    # 1. Parquet: Capital data
    c1 = capital_data.get_df_of_all_global_capital()
    sheet_access.write_dataframe_to_sheet(sheet_url, "C-Accounting", c1, start_cell='F32', header=False)

    # # 2. MongoDB: Margin
    m1 = mongo_margin_data.get_series_of_total_margin()
    sheet_access.write_dataframe_to_sheet(sheet_url, "C-Accounting", m1, start_cell='K32', header=False)

    # 3. TWS to CSV to Google Sheet: tws_data_csv
    selected_tags = [
        'AccruedCash',
        'TotalCashValue',
        'NetLiquidation',
        'GrossPositionValue',
        'AvailableFunds',
        'InitMarginReq'
    ]
    account_data = {item.tag: item.value for item in account_summary if item.tag in selected_tags}
    account_data['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tws_data = pd.DataFrame([account_data])
    tws_data = tws_data[['Date'] + selected_tags]

    # Reset index for cleaner view
    tws_data = tws_data.reset_index(drop=True)

    # Define CSV path
    target_file = os.path.join(csv_gg_path, "tws_data.csv")

    # Ensure the directory exists
    os.makedirs(csv_gg_path, exist_ok=True)

    # Extract date from tws_data
    tws_date = pd.to_datetime(tws_data["Date"]).dt.strftime('%Y-%m-%d').values[0]

    # Extract last date from c1
    c1_tail_date = c1.index[-1].strftime('%Y-%m-%d')

    if os.path.exists(target_file):
        existing_data = pd.read_csv(target_file)

        if not existing_data.empty:
            # Get last existing date in CSV
            existing_last_date = pd.to_datetime(existing_data["Date"].tail(1).values[0]).strftime('%Y-%m-%d')

            # Append only if the date doesn't exist and matches c1's last date
            if existing_last_date != tws_date and tws_date == c1_tail_date:
                tws_data.to_csv(target_file, mode='a', header=False, index=False)
                print(f"Data appended to {target_file}")
            else:
                print(f"Skipping append: Data for {tws_date} already exists or does not match c1's last date")
        else:
            tws_data.to_csv(target_file, mode='w', header=True, index=False)
            print(f"New file created at {target_file}")
    else:
        tws_data.to_csv(target_file, mode='w', header=True, index=False)
        print(f"New file created at {target_file}")

    # Read
    tws_data_csv = pd.read_csv(target_file)

    # Write
    sheet_access.write_dataframe_to_sheet(sheet_url, "C-Accounting", tws_data_csv, start_cell='N32', header=False)


def update_system_diagnostic(s, sheet_url, symbol):
    df = pd.DataFrame({

        # A) Instrument level
        # Price
        "Price": s.accounts.get_instrument_prices_for_position_or_forecast(symbol),
        "ChangePerCont": s.accounts.get_instrument_prices_for_position_or_forecast(symbol).diff(
            1) * s.accounts.get_value_of_block_price_move(symbol),
        "DailyRisk": s.rawdata.daily_returns_volatility(symbol),

        # CombineForecast
        "Forecast": s.combForecast.get_combined_forecast(symbol),

        # B) Subsystem level

        # 1. VolScalar
        "VolScalar": s.positionSize.get_average_position_at_subsystem_level(symbol),
        # vol_scalar =  target vol / instru vol

        # 2. SubsystemPosition
        "SubSystemPosition": s.positionSize.get_subsystem_position(symbol),
        # Main: (vol_scalr * combForecast)/10 [assume full fixed cap]

        # C) Portfolio level
        # 1. IDM
        "IDM": s.portfolio.get_instrument_diversification_multiplier(),

        # 2. Portfolio weight
        "Weight": s.portfolio.get_instrument_weights()[symbol],

        # 3. NotionalPosition
        "Position": s.portfolio.get_notional_position(symbol),

        # 4,5,6 Buffer
        "Buffer": s.portfolio.get_buffers(symbol),
        "TopBuffer": s.portfolio.get_buffers_for_position(symbol).iloc[:, 0],
        "BotBuffer": s.portfolio.get_buffers_for_position(symbol).iloc[:, 1],

        # D) Account level
        "BufferedPos": s.accounts.get_buffered_position(symbol),

        # E) Calculate PNL

        # Individual PNL
        "Gross": s.accounts.pandl_for_instrument(symbol).gross,
        "Costs": s.accounts.pandl_for_instrument(symbol).costs,
        "Net": s.accounts.pandl_for_instrument(symbol).net,

        # Portfolio PNL
        "PNL": s.accounts.portfolio(),
    })

    df = df.tail(20)
    df = df.fillna("")

    # Write to sheet
    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "D-Diagnostic",
        df,
        "B22",
        header=False)

    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "D-Diagnostic",
        pd.DataFrame({symbol}),
        "C18",
        header=False)


def update_system_verification(s, sheet_url, start_date):

    df = pd.DataFrame({
        "ActualCapital": s.accounts.get_actual_capital(),
        "PNL": s.accounts.portfolio_with_multiplier(),
    })

    df_subset = df.loc[start_date:]
    df_subset.fillna("")

    sheet_access.write_dataframe_to_sheet(
        sheet_url,
        "E-Verifying",
        df_subset, "B12",
        header=False)
