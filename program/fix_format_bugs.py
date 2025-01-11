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

if __name__ == '__main__':

    # FX PRICE (DONE)
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spotfx_prices/AUDUSD.parquet")
    # print(a)
    """
    2025-01-07 23:00:00  0.626445
    2025-01-08 23:00:00  0.622910
    2025-01-09 23:00:00  0.620515 
    
    Updated ---
    2025-01-10 23:00:00  0.618825
    
    Note -- 
    NEXT DAY Should be 0.6192 but it's fine.
    """

    # Contract price - DAY
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@CORN_mini#20250300.parquet")
    # print(a)
    """
    2025-01-08 06:00:00  457.875  459.125  453.625  454.00     467
    2025-01-09 06:00:00  453.875  457.125  453.000  456.00     396
    2025-01-10 06:00:00  456.000  457.125  455.625  456.50      58
    
    Updated -- 
    Note --
    (RTH=FALSE) correct
    2025-01-10 23:00:00  456.000  472.500  455.625  470.50  2215.0
    
    (RTH=True)
    2025-01-10 23:00:00  455.750  472.500  455.750  471.25  2025.0
    """
    # Contract price - HOUR
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
    # print(a)

    # REMOVE 5 rows
    # a = a.iloc[:-3]
    # a.to_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Hour@CORN_mini#20250300.parquet")
    # print(a)
    # REF
    # syscore/dateutil
    """
    2025-01-10 01:00:00  456.000  456.625  455.625  456.250      41
    2025-01-10 02:00:00  456.500  457.125  456.500  456.875      18
    2025-01-10 03:00:00  456.500  456.500  456.500  456.500       1    
    
    Updated -- 
    
    2025-01-10 08:00:00  456.000  456.625  455.625  456.250    39.0
    2025-01-10 09:00:00  456.500  457.125  456.500  456.875    18.0
    2025-01-10 10:00:00  456.500  456.500  456.500  456.500     2.0
    2025-01-10 11:00:00  456.500  456.500  455.750  455.750    20.0
    2025-01-10 12:00:00  456.000  456.250  455.875  456.125    10.0
    2025-01-10 13:00:00  456.125  456.125  456.125  456.125     4.0
    2025-01-10 14:00:00  456.625  457.000  456.625  457.000    18.0
    2025-01-10 15:00:00  457.125  457.625  457.125  457.500     8.0
    Note -- 
    1. It's TH time but suppose to be UTC     

    """


    # Contract price - MIXED
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/CORN_mini#20250300.parquet")
    # print(a)
    """
    2025-01-09 17:00:00  455.375  457.125  455.375  455.750      48
    2025-01-09 18:00:00  455.875  456.750  455.875  456.250      19
    2025-01-10 01:00:00  456.000  456.625  455.625  456.250      41
    2025-01-10 02:00:00  456.500  457.125  456.500  456.875      18
    2025-01-10 03:00:00  456.500  456.500  456.500  456.500       1
    2025-01-10 06:00:00  456.000  457.125  455.625  456.500      58
    
    Updated -- 
    2025-01-10 08:00:00  456.000  456.625  455.625  456.250    39.0
    2025-01-10 09:00:00  456.500  457.125  456.500  456.875    18.0
    2025-01-10 10:00:00  456.500  456.500  456.500  456.500     2.0
    2025-01-10 11:00:00  456.500  456.500  455.750  455.750    20.0
    2025-01-10 12:00:00  456.000  456.250  455.875  456.125    10.0
    2025-01-10 13:00:00  456.125  456.125  456.125  456.125     4.0
    """

    # Roll calendar
    # a = pd.read_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/data/temp/roll_calendars/CORN_mini.csv")
    # print(a)

    # Multiple price from MIXED or DAY
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/CORN_mini.parquet")
    # print(a)
    """
    2025-01-07 17:00:00  456.250      NaN      NaN       20250300         20250500       20250500
    2025-01-07 18:00:00  457.750  465.250  465.250       20250300         20250500       20250500
    2025-01-07 19:00:00  457.625  465.375  465.375       20250300         20250500       20250500
    2025-01-08 01:00:00  457.625  465.375  465.375       20250300         20250500       20250500
    2025-01-08 06:00:00  465.375  468.000  468.000       20250500         20250700       20250700
    
    2025-01-08 09:00:00      NaN       20250700  466.250       20250500      NaN         20250700
    2025-01-08 10:00:00      NaN       20250700  466.625       20250500      NaN         20250700
    2025-01-08 11:00:00      NaN       20250700  465.250       20250500      NaN         20250700
    2025-01-08 13:00:00      NaN       20250700  464.500       20250500      NaN         20250700
    2025-01-08 15:00:00      NaN       20250700  463.250       20250500      NaN         20250700
    2025-01-08 16:00:00      NaN       20250700  464.000       20250500      NaN         20250700
    2025-01-08 17:00:00  466.250       20250700      NaN       20250500  466.250         20250700
    2025-01-08 18:00:00      NaN       20250700  462.000       20250500      NaN         20250700
    2025-01-08 19:00:00      NaN       20250700  462.000       20250500      NaN         20250700
    2025-01-08 23:00:00  465.750       20250700  462.500       20250500  465.750         20250700
    2025-01-09 01:00:00      NaN       20250700  462.125       20250500      NaN         20250700
    2025-01-09 05:00:00      NaN       20250700  462.375       20250500      NaN         20250700
    2025-01-09 13:00:00      NaN       20250700  463.250       20250500      NaN         20250700
    2025-01-09 15:00:00  464.875       20250700  463.250       20250500  464.875         20250700
    2025-01-09 16:00:00      NaN       20250700  462.875       20250500      NaN         20250700
    2025-01-09 17:00:00      NaN       20250700  465.250       20250500      NaN         20250700
    2025-01-09 23:00:00  468.000       20250700  464.500       20250500  468.000         20250700
    2025-01-10 01:00:00  468.000       20250700  463.875       20250500  468.000         20250700
    2025-01-10 04:00:00      NaN       20250700  464.500       20250500      NaN         20250700
    2025-01-10 05:00:00  467.500       20250700      NaN       20250500  467.500         20250700
    2025-01-10 11:00:00      NaN       20250700  465.625       20250500      NaN         20250700
    2025-01-10 14:30:00      NaN       20250700  464.625       20250500      NaN         20250700
    2025-01-10 15:00:00  469.125       20250700  465.500       20250500  469.125         20250700
    2025-01-10 16:00:00  469.750       20250700  466.000       20250500  469.750         20250700
    2025-01-10 17:00:00  479.250       20250700  477.625       20250500  479.250         20250700
    2025-01-10 18:00:00  480.000       20250700  478.125       20250500  480.000         20250700
    2025-01-10 19:00:00  482.500       20250700  479.625       20250500  482.500         20250700
    2025-01-10 23:00:00  482.000       20250700  479.500       20250500  482.000         20250700
    """

    # Adjusted price
    a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_adjusted_prices/CORN_mini.parquet")
    print(a)
    """
    2025-01-07 16:00:00  462.500
    2025-01-07 17:00:00  464.000
    2025-01-07 18:00:00  465.500
    2025-01-07 19:00:00  465.375
    2025-01-08 01:00:00  465.375
    2025-01-08 06:00:00  465.375
    """


    # Note : Timezone
    # Search RTH or timezone
    import pytz
    from datetime import datetime

    # NOT WORK
    # Set the timezone to UTC
    # utc = pytz.UTC
    # now = datetime.now()
    # utc_time = utc.localize(now)
    # print("UTC Time:", utc_time)

    # THIS WORK!
    # from datetime import datetime
    from zoneinfo import ZoneInfo
    #
    # # Set the timezone to UTC
    # utc_time = datetime.now(ZoneInfo("UTC"))
    # print("UTC Time:", utc_time)
