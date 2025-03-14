from program.googlesheet.update_system_gg import update_market_monitoring, update_portfolio_monitoring, \
    update_system_verification
from program.helper.run_scripts import run_scripts
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/04_check_adding_market_system_f1/config.yaml"
config = Config(CONFIG_PATH)
data = csvFuturesSimData()

s = futures_system(config=config, data=data)

if __name__ == '__main__':

    """
    1. Add data in csv/config.
    2. XXX 
    
    
    """


    a = s.rawdata.get_daily_percentage_volatility("EUR_micro") * 16  # Daily % risk or (number%)
    print(a)


