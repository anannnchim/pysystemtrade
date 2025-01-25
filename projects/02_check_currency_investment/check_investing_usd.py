

if __name__ == '__main__':
    import pandas as pd
    # Load the CSV file
    file_path = '/projects/02_check_currency_investment/USDTHB.csv'
    df = pd.read_csv(file_path)

    # Ensure the 'Time' column is a datetime type
    df['Time'] = pd.to_datetime(df['Time'])

    # Extract the year from 'Time'
    df['Year'] = df['Time'].dt.year

    # Group by year and take the LAST “Last” price for each year
    yearly_price = df.groupby('Year')['Last'].last()

    # Compute the percentage change (year-over-year returns)
    yearly_return = yearly_price.pct_change() * 100.0  # multiplied by 100 for percentage

    # Combine into a single DataFrame
    result = pd.DataFrame({
        'Year': yearly_price.index,
        'Return (%)': yearly_return.round(2)  # Round to 2 decimal places for readability
    })

    # Optionally drop the first row if it contains NaN (no prior year to compare)
    result.dropna(inplace=True)

    print(result.to_string(index=False))

    result.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/02_check_currency_investment")

