from sysdata.parquet.parquet_access import ParquetAccess
from sysdata.parquet.parquet_spotfx_prices import parquetFxPricesData


if __name__ == '__main__':
    parquet_access = ParquetAccess("/Users/nanthawat/PycharmProjects/private-pysystemtrade/src/data/parquet")
    db_fx_price_data = parquetFxPricesData(parquet_access)
    print(db_fx_price_data.get_list_of_fxcodes())
