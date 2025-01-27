"""
Make a trade via ib_insync
"""
from ib_insync import *

if __name__ == '__main__':

    # Note 1 - Connection
    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=13)

    # Note 2 - Define future
    mxp_future = Future(symbol='ZC', lastTradeDateOrContractMonth='202512', exchange='CBOT', currency='USD')
    print(mxp_future)

    # Note 3 - Check Portfolio data
    # Get portfolio positions
    positions = ib.positions()
    print("Current Portfolio Holdings:")
    for position in positions:
        print(f"Instrument: {position.contract.symbol}, Quantity: {position.position}, Avg Cost: {position.avgCost}")
    print("----------------------------------------------------------------")
    # Get account summary
    account_summary = ib.accountSummary()
    print("\nAccount Summary:")
    for item in account_summary:
        print(f"{item.tag}: {item.value} {item.currency}")

    print("----------------------------------------------------------------")
    # Get Netliquidation
    net_liquidation = next((item.value for item in account_summary if item.tag == 'NetLiquidation'), None)
    print(net_liquidation)
    print("----------------------------------------------------------------")


    # # # Note 4 - ***Place the market order***
    # order = MarketOrder('SELL', 2)  # 'BUY' or 'SELL', and specify the quantity
    # trade = ib.placeOrder(mxp_future, order)
    # print("this is trade: ", trade)
    #
    # # 4. Monitor the order status
    # print(f"Order status: {trade.orderStatus.status}")



    # Check status for open trade

    # 2. Get all open trades
    open_trades = ib.trades()
    # 3. Check the status of each trade
    if not open_trades:
        print("No open trades found.")
    else:
        for trade in open_trades:
            print(f"Contract: {trade.contract}")
            print(f"Action: {trade.order.action}")
            print(f"Quantity: {trade.order.totalQuantity}")
            print(f"Order Status: {trade.orderStatus.status}")
            print(f"Filled Quantity: {trade.orderStatus.filled}")
            print(f"Remaining Quantity: {trade.orderStatus.remaining}")
            print(f"Average Fill Price: {trade.orderStatus.avgFillPrice}")
            print(f"Why Held: {trade.orderStatus.whyHeld}")
            print(f"Trade Log:")
            for log_entry in trade.log:
                print(f"{log_entry.time}: {log_entry.status} - {log_entry.message}")
            print("-" * 40)

