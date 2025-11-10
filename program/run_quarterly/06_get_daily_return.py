from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.pyplot as plt

# INPUT: Select data and system
# data = csvFuturesSimData()
data = dbFuturesSimData()

# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/system_f1_config.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/diversified.yaml")
config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/production/diversified.yaml")
# config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/config/new/new_sytem_f1.yaml")

s = futures_system(config=config, data=data)

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

"""
1. Check stats
2. Equity curve
3. Drawdown
4. Performance based on market
"""

if __name__ == '__main__':

    # # 1. Statistic
    stats_output = s.accounts.portfolio().percent.stats()
    metrics = stats_output[0]
    df = pd.DataFrame(metrics, columns=["Metric", "Value"])
    print(df.to_string(index=False))


    # INPUT: Select type of return
    system_return = s.accounts.portfolio_with_multiplier().percent
    # system_return = s.accounts.portfolio().percent

    # Plot
    system_return.curve().plot(title="System Net % Performance")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.grid(True);
    plt.tight_layout()
    plt.show()

    # Print
    print(system_return)
    df = pd.DataFrame(system_return/100)
    df.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/run_quarterly/ri.csv")
