if __name__ == '__main__':
    from ib_insync import *

    # Connect to IB
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=100000)

    # Retrieve account summary
    print("=== Account Summary ===")
    account_summary = ib.accountSummary()
    for item in account_summary:
        print(f"{item.tag}: {item.value} {item.currency}")

    # Retrieve specific account values
    print("\n=== Account Values ===")
    account_values = ib.accountValues()
    for item in account_values:
        print(f"Account: {item.account}, Tag: {item.tag}, Value: {item.value}, Currency: {item.currency}")

    # Retrieve portfolio data
    print("\n=== Portfolio ===")
    portfolio = ib.portfolio()
    for position in portfolio:
        print(f"Symbol: {position.contract.symbol}, Position: {position.position}, Avg Cost: {position.avgCost}")

    # Retrieve profit and loss (PnL)
    print("\n=== PnL ===")
    accounts = ib.accounts()
    for account in accounts:
        pnl = ib.reqPnL(account=account)
        print(f"Account: {account}, Unrealized PnL: {pnl.unrealizedPnL}, Realized PnL: {pnl.realizedPnL}")

    # Disconnect
    ib.disconnect()

     # OR
    # from sysdata.config.production_config import get_production_config
    # broker_account = get_production_config().get_element('broker_account')
    # account_summary = ib.accountSummary(broker_account)
    # print("\nAccount Summary:")
    # for item in account_summary:
    #     print(f"{item.tag}: {item.value} {item.currency}")
