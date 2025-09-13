import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
import matplotlib.pyplot as plt
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# INPUT: Select data and system
data = csvFuturesSimData()
# data = dbFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/new_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/single_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/static_three.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/static/AFTS_four.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v2.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/diversified_v2.yaml")


s = futures_system(config=config, data=data)

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

"""
1. Check IDM overtime
2. Correlation matrix 
"""
if __name__ == '__main__':

    # 1. IDM overtime
    a = s.portfolio.get_instrument_diversification_multiplier() # Estimated IDM
    print(a)
    a.plot()
    plt.show()
    print(a.mean())

    # 2. Correlation
    correlation = s.portfolio.get_instrument_correlation_matrix().corr_list[-1]
    print(correlation)
