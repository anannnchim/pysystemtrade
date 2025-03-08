from sysdata.data_blob import dataBlob
from sysproduction.data.capital import dataCapital

if __name__ == '__main__':
    strategy_name = "system_01"
    data = dataBlob()
    capital_data = dataCapital(data)
    print(capital_data.get_current_capital_for_strategy(strategy_name))