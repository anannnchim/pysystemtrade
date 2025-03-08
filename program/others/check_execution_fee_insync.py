if __name__ == '__main__':


    from ib_insync import *
    from sysdata.config.production_config import get_production_config
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=123)

    # Note 1 - Retrieve execution details
    executions = ib.executions()
    # Extract fees and commissions
    for execDetail in executions:
        execution = execDetail.execution
        print(f"Symbol: {execution.symbol}, Commission: {execution.commissionReport.commission}")

    # Note 2 - Get PNL
    account_id = get_production_config().get_element("broker_account")
    pnl = ib.reqPnL(account_id)
    # Display Realized and Unrealized P&L
    print(f"Realized PnL: {pnl.realizedPnL}")
    print(f"Unrealized PnL: {pnl.unrealizedPnL}")
