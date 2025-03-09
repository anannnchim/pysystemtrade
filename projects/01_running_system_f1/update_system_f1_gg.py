from program.googlesheet.update_system_gg import update_market_monitoring, update_portfolio_monitoring
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
SHEET_URL = "https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1522926356#gid=1522926356"
config = Config(CONFIG_PATH)
data = csvFuturesSimData()

s = futures_system(config=config, data=data)


if __name__ == '__main__':

    # This will override, we can run many times.
    update_market_monitoring(s, SHEET_URL)
    update_portfolio_monitoring(s, SHEET_URL)

