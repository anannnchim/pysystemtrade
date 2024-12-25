import pandas as pd

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines
    pd.set_option('display.max_rows', 100)  # Adjust for rows if needed (20 is just an example)

    # 1. Global capital
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet")
    # print(a)

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/strategy_1.parquet")
    # print(a)

    # b = pd.read_parquet("/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/strategy_1.parquet")
    # print(b)

    # C = pd.read_parquet(
    #     "/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/capital/strategy_2.parquet")
    # print(C)

    # Position
    a = pd.read_parquet( "/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet/optimal_positions/strategy_1 CORN_mini.parquet")
    print(a)


    """
    Next. setup trade limit by interactive_control then 
    update_strategy_order, run report, run_stack_handler
    """

