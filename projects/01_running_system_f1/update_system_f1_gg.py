from program.googlesheet.update_system_gg import update_market_monitoring, update_portfolio_monitoring, \
    update_system_verification
from program.helper.run_scripts import run_scripts
from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData
from sysdata.sim.db_futures_sim_data import dbFuturesSimData
from systems.provided.futures_chapter15.basesystem import futures_system
CONFIG_PATH = "/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/config.yaml"
SHEET_URL = "https://docs.google.com/spreadsheets/d/17MCh8REdbM1F9J1MOSt_AxWCPZwpntowubivCWTRv94/edit?gid=1522926356#gid=1522926356"
config = Config(CONFIG_PATH)
data = csvFuturesSimData()

s = futures_system(config=config, data=data)
start_date = "2025-02-03"

if __name__ == '__main__':

    # Update data
    run_scripts(["/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/update_data_gg.py"])

    update_market_monitoring(s, SHEET_URL)
    update_portfolio_monitoring(s, SHEET_URL)
    update_system_verification(s, SHEET_URL, start_date)
    # Optional
    # run_scripts(["/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/verify_system.py"])

    # Get buffered position (Optional)
    run_scripts(["/Users/nanthawat/PycharmProjects/pysystemtrade/projects/01_running_system_f1/run_system.py"])
