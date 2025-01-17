"""
Get FX prices from csv repo files and write to arctic

WARNING WILL OVERWRITE EXISTING!
"""
from sysdata.csv.csv_spot_fx import csvFxPricesData
from sysdata.parquet.parquet_access import ParquetAccess
from sysdata.parquet.parquet_spotfx_prices import parquetFxPricesData
from sysproduction.data.currency_data import fxPricesData


"""
This will copy csv fx price and override into parquet.
"""

# Note: Add this line
parquet_access = ParquetAccess("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet")
db_fx_price_data = parquetFxPricesData(parquet_access)

# Remove this line.
# db_fx_price_data = fxPricesData()


if __name__ == "__main__":
    input("Will overwrite existing prices are you sure?! CTL-C to abort")

    csv_fx_prices = csvFxPricesData()

    currency_code = input("Currency code? <return for ALL currencies> ")
    if currency_code == "":
        list_of_ccy_codes = csv_fx_prices.get_list_of_fxcodes()
    else:
        list_of_ccy_codes = [currency_code]

    for currency_code in list_of_ccy_codes:
        fx_prices = csv_fx_prices.get_fx_prices(currency_code)
        print(fx_prices)

        db_fx_price_data.add_fx_prices(
            code=currency_code, fx_price_data=fx_prices, ignore_duplication=True
        )
