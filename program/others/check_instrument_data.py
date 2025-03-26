
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
from systems.rawdata import RawData
import matplotlib.pyplot as plt

data = csvFuturesSimData()
#data = dbFuturesSimData()



# Adjust pandas options to display all rows and columns
# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.max_rows', None)  # Show all rows
# pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

if __name__ == '__main__':
    a = data.daily_prices("JP-REALESTATE")

    a.plot()
    plt.show()