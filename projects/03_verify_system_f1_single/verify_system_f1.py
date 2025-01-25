"""
For verifying system F1 , single instrument

ref: https://docs.google.com/spreadsheets/d/1FfdHbwofm_Admn7Q-9TuHsFCY1Wir_MiakrBDbo3dzE/edit?gid=0#gid=0
"""
import pandas as pd
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
import matplotlib.pyplot as plt
import os

config = Config("/Users/nanthawat/PycharmProjects/pysystemtrade/projects/03_verify_system_f1_single/single_config.yaml")

data = csvFuturesSimData()
s = futures_system(config=config, data=data)
c1 = "USD"

# Adjust pandas options to display all rows and columns
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines


# ------------------------------------ Save to csv ----------------------------

if __name__ == '__main__':

    path = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/03_verify_system_f1_single/output_csv"

    # Note 1: Equity and daily return
    a = pd.DataFrame({
        "portfolio": s.accounts.portfolio(),
        "portfolio.curve": s.accounts.portfolio().curve(),
        "portfolio.percent.curve": s.accounts.portfolio().percent.curve(),
        "capital": s.accounts.portfolio().capital
    })
    a.to_csv(os.path.join(path, "a.csv"))

    # Note 2. : Analyse Cost
    b = s.accounts.portfolio().to_ncg_frame()
    b.to_csv(os.path.join(path, "b.csv"))

    # Note 3 : Buffered position
    # Target position
    c = pd.DataFrame({
        "bufferd_position": s.accounts.get_buffered_position("USD")
    })
    c.to_csv(os.path.join(path, "c.csv"))

    # Get bounds
    d = s.accounts.get_buffers_for_position("USD")
    d.to_csv(os.path.join(path, "d.csv"))

    # Note 4. Analyse gross return
    price = s.rawdata.get_daily_prices("USD")
    price.to_csv(os.path.join(path, "price.csv"))

