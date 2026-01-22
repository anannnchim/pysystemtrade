import matplotlib.pyplot as plt
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system

# INPUT
config = Config("private/systems/old/config_v1.yaml")

# Init objects
db_data = dbFuturesSimData()
csv_data = csvFuturesSimData()

s = futures_system(config=config, data=db_data)


if __name__ == '__main__':

    input("Check csv data")
    print(f'Instrument List', csv_data)


    input("Checking DB & Private config")
    s.accounts.portfolio().net.percent.curve().plot(title="System Net % Performance")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.grid(True);
    plt.tight_layout()
    plt.show()
