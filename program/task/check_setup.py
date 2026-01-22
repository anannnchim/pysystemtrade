import matplotlib.pyplot as plt
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system


if __name__ == '__main__':

    input("1. Check csv data")
    csv_data = csvFuturesSimData()
    print(f'Instrument List', csv_data)

    input("2. Check db data")
    db_data = dbFuturesSimData()
    print(f'Instrument List', db_data)

    input("3. Check private path")
    config = Config("private/systems/old/config_v1.yaml")
    print(config)

    input("4. Check backtesting")
    s = futures_system(config=config, data=db_data)
    s.accounts.portfolio().net.percent.curve().plot(title="System Net % Performance")
    plt.xlabel("Date");
    plt.ylabel("%")
    plt.grid(True);
    plt.tight_layout()
    plt.show()
