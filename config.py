#----------Train-Invest Configuration-------------#
Mode="Invest" #"Train": only do training, with output of best solution and value
           #"Invest": only do investment, with output of trend ratio, nett return and solution
           #"All": do from training to test

#----------Train-Investment Interval Details-------------#
Investment_start_date = "2022-10-01"
Train_test_mode = "year-on-year" #continuous, year-on-year
Training_interval = "1M" #continuous = [1M, 3M, 6M, 1Y], year-on-year = [1M, 3M , 6M]
Investment_interval = "1M" #continuous = [1M, 3M, 6M, 1Y], year-on-year = [1M, 3M , 6M]

#----------Investment Details----------#
Initial_fund = 10000

#------------Algorithm Details------------#
Experiment = 50
Generation = 10000
Solution_each_generation = 10
theta = 0.001
theta_upper = 0.00125
theta_lower = 0.00045