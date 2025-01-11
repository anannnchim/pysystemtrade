import pandas as pd
import matplotlib.pyplot as plt

from sysbrokers.IB.ib_trading_hours import get_GMT_offset_hours
from syscore.dateutils import DAILY_PRICE_FREQ
from sysdata.config.production_config import get_production_config
from sysdata.data_blob import dataBlob
from sysproduction.data.broker import dataBroker
from sysproduction.data.prices import diagPrices

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

# REMOVE 5 rows
# a = a.iloc[:-3]
# a.to_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
# print(a)
# REF
# syscore/dateutil

if __name__ == '__main__':

    # Contract price - DAY
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN_mini#20250300.parquet")
    # print(a)
    """
    2025-01-07 06:00:00  456.125  458.375  453.125  458.00     760
    2025-01-08 06:00:00  457.875  459.125  453.625  454.00     467
    2025-01-09 06:00:00  453.875  457.125  453.000  456.00     396
    2025-01-10 06:00:00  456.000  472.500  455.625  470.50    2215 (Settlemet price or CT 13:00 , UTC 19:00
    
    NEW
    2025-01-10 23:00:00  455.750  472.500  455.750  471.25  2025.0 (Close at CT 13:00) 
    
    """
    # Contract price - HOUR
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
    # print(a)

    """
    2025-01-10 14:00:00  455.750  457.125  455.750  457.125      42
    2025-01-10 15:00:00  457.125  457.875  456.875  457.500      78
    2025-01-10 16:00:00  457.375  458.500  456.750  457.500     111
    2025-01-10 17:00:00  459.000  472.500  458.375  468.625    1365
    2025-01-10 18:00:00  468.375  469.750  466.875  469.125     276
    2025-01-10 19:00:00  469.375  471.625  469.375  471.250     154
    """

    # Contract price - MIXED
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN_mini#20250300.parquet")
    # print(a)
    """
    2025-01-10 12:00:00  457.500  457.500  456.875  457.375      11
    2025-01-10 13:00:00  457.000  457.250  455.875  455.875      28
    2025-01-10 14:00:00  455.750  457.125  455.750  457.125      42
    2025-01-10 15:00:00  457.125  457.875  456.875  457.500      78
    2025-01-10 16:00:00  457.375  458.500  456.750  457.500     111
    2025-01-10 17:00:00  459.000  472.500  458.375  468.625    1365
    2025-01-10 18:00:00  468.375  469.750  466.875  469.125     276
    2025-01-10 19:00:00  469.375  471.625  469.375  471.250     154
    
    NEW 
    2025-01-10 23:00:00  455.750  472.500  455.750  471.250  2025.0
    """

    # Roll calendar
    # a = pd.read_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/roll_calendars/CORN_mini.csv")
    # print(a)
    """
                 DATE_TIME  current_contract  next_contract  carry_contract
    0  2024-02-14 01:00:00          20240300       20240500        20240500
    1  2024-04-15 00:00:00          20240500       20240700        20240700
    2  2024-06-14 00:00:00          20240700       20240900        20240900
    3  2024-08-16 00:00:00          20240900       20241200        20241200
    4  2024-11-15 01:00:00          20241200       20250300        20250300
    5  2025-01-10 01:00:00          20250300       20250500        20250500
    """

    # Multiple price from MIXED or DAY
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN_mini.parquet")
    # print(a)
    """
                           PRICE  FORWARD    CARRY PRICE_CONTRACT FORWARD_CONTRACT CARRY_CONTRACT
    index                                                                                        
    
    
    2025-01-10 06:00:00  479.500  482.000  482.000       20250500         20250700       20250700
    2025-01-10 11:00:00  465.625      NaN      NaN       20250500         20250700       20250700
    2025-01-10 14:00:00  464.625      NaN      NaN       20250500         20250700       20250700
    2025-01-10 15:00:00  465.500  469.125  469.125       20250500         20250700       20250700
    2025-01-10 16:00:00  466.000  469.750  469.750       20250500         20250700       20250700
    2025-01-10 17:00:00  477.625  479.250  479.250       20250500         20250700       20250700
    2025-01-10 18:00:00  478.125  480.000  480.000       20250500         20250700       20250700
    2025-01-10 19:00:00  479.625  482.500  482.500       20250500         20250700       20250700
    
    
                       CARRY CARRY_CONTRACT    PRICE PRICE_CONTRACT  FORWARD FORWARD_CONTRACT
        index                                                                                        
    2025-01-10 17:00:00  479.250       20250700  477.625       20250500  479.250         20250700
    2025-01-10 18:00:00  480.000       20250700  478.125       20250500  480.000         20250700
    2025-01-10 19:00:00  482.500       20250700  479.625       20250500  482.500         20250700
    2025-01-10 23:00:00  482.500       20250700  479.625       20250500  482.500         20250700
    """


    # Adjusted price
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    print(a)
    """
    2025-01-10 05:00:00  464.500
    2025-01-10 06:00:00  479.500
    2025-01-10 11:00:00  465.625
    2025-01-10 14:00:00  464.625
    2025-01-10 15:00:00  465.500
    2025-01-10 16:00:00  466.000
    2025-01-10 17:00:00  477.625
    2025-01-10 18:00:00  478.125
    2025-01-10 19:00:00  479.625
    
    NEW
    2025-01-10 23:00:00  479.625
    """