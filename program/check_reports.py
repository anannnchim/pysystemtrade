from sysproduction.reporting.minimum_capital_report import minimum_capital_report

if __name__ == '__main__':


    from sysproduction.data.reports import dataReports
    print(dataReports().get_default_reporting_config_dict().keys())
