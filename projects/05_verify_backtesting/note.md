# Verification note

1. Verify price from two different source of data
- Mostly all adjusted prices are very similar.
- Statistics are quite similar as well

2. Check how many year we need in order for forecast to be not spiked?
- We need at least two years of data for alignment in forecast from different start time. (Conservative number)

Conclusion: No problem

3. Verify performance for each instrument. 
We test single strategy performance
- MUMMY: Both csv and db start at 2019 (same period)
- COPPER-micro: parquet start in 2023 (short data)
- CAD10: Same period but start since 1995

Conclusion: No problem, both of the performance are consistent. Money is made from some markets. 

4. Check net, gross vs DB
- For slow EMA, there is not much differ in gross and net returnwhile it show different on fast EMA.
- CSV costs and DB cost are the same. 

Conclusion: No problem.

5. Verify portfolio given same period
- Stats for both source on aligned period are the same.
- All instruments have a positive return except MUMMY, RUSSELL.

ุ6. Check backtesting report for both source on a portfolio

Conclusion: Both of them show the similar result.

### Summary
Given different data source for production-db, performance should be similar to backtesting. 



