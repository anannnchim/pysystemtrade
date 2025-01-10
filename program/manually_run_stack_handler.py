from sysdata.data_blob import dataBlob
from sysexecution.stack_handler.stack_handler import stackHandler

if __name__ == '__main__':
  stack_handler_data = dataBlob(log_name="stack_handler")
  stack_handler = stackHandler(stack_handler_data)
  stack_handler.create_broker_orders_from_contract_orders()

  list_of_contract_order_ids = stack_handler.contract_stack.get_list_of_order_ids()
  stack_handler.log.debug("Contract order IDs: %s", list_of_contract_order_ids)

  for contract_order_id in list_of_contract_order_ids:
    stack_handler.create_broker_order_for_contract_order(contract_order_id)
    print(contract_order_id)
    # https://chatgpt.com/g/g-p-675cea3ad94c8191be53cc7eef529721-anan-capital/c/677f562e-27dc-8004-b004-f7f008e5b341
