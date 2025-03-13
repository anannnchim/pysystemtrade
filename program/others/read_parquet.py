import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Adjust pandas options to display all rows and columns
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to new lines

    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/spreads/EUR_micro.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/__global_capital.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/capital/system_01.parquet")
    # a = pd.read_parquet("/data/parquet/futures_contract_prices/Day@EUR_micro#20250300.parquet")
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/EUR_micro#20250300.parquet")
    # a = pd.read_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/data/futures/adjusted_prices_csv/EUR_micro.csv")
    # a = pd.read_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/V2X#20220100.parquet")

    # a = pd.read_parquet(
    #     "/data/parquet/capital/__global_capital.parquet")
    # print(a)



    """

    # Global cap
    2025-02-25 09:52:29.347225   9694.58      -305.42   9694.58   9694.58
    2025-02-26 10:18:01.740415   9634.60      -365.40   9634.60   9634.60
    2025-02-27 10:29:10.178886   9657.97      -342.03   9657.97   9657.97
    2025-02-28 10:54:08.029011   9657.97      -342.03   9657.97   9657.97
    2025-03-01 21:15:31.150516   9687.19      -312.81   9687.19   9687.19
    2025-03-04 09:40:11.552803   9547.26      -452.74   9547.26   9547.26
    2025-03-05 12:21:16.745840   9380.45      -619.55   9380.45   9380.45
    2025-03-06 20:52:21.892452   9287.15      -712.85   9287.15   9287.15
    
    2025-02-24 10:00:47.670817   9703.38
    2025-02-25 09:52:31.046975   9694.58
    2025-02-26 10:18:03.404301   9634.60
    2025-02-27 10:29:10.513232   9657.97
    2025-02-28 10:54:09.434175   9657.97
    2025-03-01 21:15:32.696264   9687.19
    2025-03-04 09:40:11.863498   9547.26
    2025-03-05 12:21:18.172267   9380.45
    2025-03-06 20:52:23.464524   9287.15
    
    2025-02-26 10:18:10.344207       -0.476836       -0.085402           1.0521           20250300
    2025-02-27 10:31:06.201359       -0.546763       -0.148476           1.0502           20250300
    2025-02-28 10:54:39.512962       -1.106600       -0.727107           1.0413           20250300
    2025-03-01 21:15:40.566657       -1.587417       -1.202987           1.0375           20250300
    2025-03-04 10:39:16.373364       -0.785755       -0.438814           1.0496           20250300
    2025-03-05 12:21:38.175041        0.002185        0.326655           1.0608           20250300
    2025-03-06 20:52:30.908515        0.687403        0.970098           1.0794           20250300
    """
    # a = pd.read_parquet("/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_contract_prices/Day@VIX_mini#20250500.parquet")
    # print(a)

    a = pd.read_parquet(
        "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/futures_multiple_prices/ETHER-micro.parquet")
    print(a)

    # 2256.0/ 16484.0

    # Note - Delete some row
    # a.to_csv("/Users/nanthawat/PycharmProjects/pysystemtrade/program/output_csv/price.csv")
    # file_path = "/Users/nanthawat/PycharmProjects/pysystemtrade/data/parquet/optimal_positions/system_01 EUR_micro.parquet"
    # df = pd.read_parquet(file_path, engine="pyarrow")  # or engine="fastparquet"
    # df = df.drop(df.index[-3])
    #
    # df.to_parquet(file_path, index=True, engine="pyarrow")
    # print(df)

    """
    V2X
                         CARRY CARRY_CONTRACT  PRICE PRICE_CONTRACT  FORWARD FORWARD_CONTRACT
                         
    index                                                                                    
    2021-12-22 07:00:00  24.20       20220200    NaN       20220300      NaN         20220400
    2021-12-22 08:00:00  24.25       20220200  26.35       20220300      NaN         20220400
    2021-12-22 09:00:00  24.25       20220200  26.40       20220300      NaN         20220400
    2021-12-22 10:00:00  24.10       20220200  26.35       20220300    25.80         20220400
    2021-12-22 11:00:00  24.05       20220200  26.25       20220300      NaN         20220400
    ...                    ...            ...    ...            ...      ...              ...
    2025-03-11 17:00:00    NaN       20250300  22.90       20250400    22.40         20250500
    2025-03-11 18:00:00    NaN       20250300  22.05       20250400    21.75         20250500
    2025-03-11 19:00:00    NaN       20250300  22.15       20250400    21.65         20250500
    2025-03-11 20:00:00    NaN       20250300  22.25       20250400    21.85         20250500
    2025-03-11 23:00:00  23.25       20250300  22.75       20250400    22.25         20250500
    
    EUR_micro
                          CARRY CARRY_CONTRACT   PRICE PRICE_CONTRACT  FORWARD FORWARD_CONTRACT
    index                                                                                      
    2009-06-12 02:00:00     NaN       20091200  1.4098       20090900      NaN         20091200
    2009-06-12 03:00:00     NaN       20091200  1.4108       20090900      NaN         20091200
    2009-06-12 04:00:00     NaN       20091200  1.4065       20090900      NaN         20091200
    2009-06-12 05:00:00     NaN       20091200  1.3998       20090900      NaN         20091200
    2009-06-12 06:00:00     NaN       20091200  1.4099       20090900      NaN         20091200
    ...                     ...            ...     ...            ...      ...              ...
    2025-03-11 17:00:00  1.0991       20250600  1.0938       20250300   1.0991         20250600
    2025-03-11 18:00:00  1.0988       20250600  1.0934       20250300   1.0988         20250600
    2025-03-11 19:00:00  1.0979       20250600  1.0924       20250300   1.0979         20250600
    2025-03-11 20:00:00  1.0976       20250600  1.0922       20250300   1.0976         20250600
    2025-03-11 23:00:00  1.0989       20250600  1.0935       20250300   1.0989         20250600
    """
