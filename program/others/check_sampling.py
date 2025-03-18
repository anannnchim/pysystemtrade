from sysdata.data_blob import dataBlob
from sysproduction.data.prices import diagPrices
import pandas as pd

data = dataBlob()

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
if __name__ == '__main__':

    # 1. We get instrument list from parquet/multiple price
    a = diagPrices(data).get_list_of_instruments_in_multiple_prices()
    multiple_prices = diagPrices(data).get_multiple_prices("EUR_micro")
    print(multiple_prices)





