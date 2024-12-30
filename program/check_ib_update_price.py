# Adjust pandas options to display all rows and columns
import pandas as pd

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':

    """
    MXP
    2024-12-24 02:00:00  0.04874  0.04876  0.04869  0.04869   2211.0
    2024-12-24 03:00:00  0.04870  0.04875  0.04867  0.04875   1149.0
    2024-12-24 04:00:00  0.04874  0.04883  0.04871  0.04879    802.0
    2024-12-24 21:30:00  0.04886  0.04895  0.04886  0.04888   1429.0
    2024-12-24 22:00:00  0.04889  0.04894  0.04880  0.04884   4059.0
    2024-12-24 23:00:00  0.04875  0.04875  0.04861  0.04870   3703.0
    2024-12-25 01:00:00  0.04889  0.04891  0.04883  0.04885    710.0
    2024-12-25 23:00:00  0.04883  0.04890  0.04881  0.04890   1452.0
    
    DAY
    2024-12-17 06:00:00  0.04891  0.04905  0.04850  0.04865  59783.0
    2024-12-18 06:00:00  0.04876  0.04899  0.04809  0.04825  61980.0
    2024-12-19 06:00:00  0.04822  0.04846  0.04796  0.04843  64298.0
    2024-12-19 23:00:00  0.04825  0.04846  0.04796  0.04839  29951.0
    2024-12-20 23:00:00  0.04878  0.04919  0.04878  0.04907  35512.0
    2024-12-23 23:00:00  0.04898  0.04904  0.04861  0.04879  20881.0
    2024-12-24 23:00:00  0.04886  0.04895  0.04877  0.04885   8997.0
    
    HOUR
    2024-12-24 23:00:00  0.04875  0.04875  0.04861  0.04870   3703.0
    2024-12-24 01:00:00  0.04869  0.04875  0.04865  0.04874   1278.0
    2024-12-24 02:00:00  0.04874  0.04876  0.04869  0.04869   2211.0
    2024-12-24 03:00:00  0.04870  0.04875  0.04867  0.04875   1149.0
    2024-12-24 04:00:00  0.04874  0.04883  0.04871  0.04879    802.0
    2024-12-24 21:30:00  0.04886  0.04895  0.04886  0.04888   1429.0
    2024-12-24 22:00:00  0.04889  0.04894  0.04880  0.04884   4059.0
    2024-12-24 23:00:00  0.04884  0.04884  0.04877  0.04883   1347.0
    2024-12-25 23:00:00  0.04883  0.04890  0.04881  0.04890   1452.0
    2024-12-25 01:00:00  0.04889  0.04891  0.04883  0.04885    710.0
    
    """
    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/MXP#20250300.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@MXP#20250300.parquet"
    # path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@MXP#20250300.parquet"
    a = pd.read_parquet(path)
    print(a)

    # Note: Delete data
    # a = a[:-10]
    # print(a)
    # a.to_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@MXP#20250300.parquet", index=True)

