import copy

import stock_price as sp
import trend_ratio as tr
from QTS.GNQTS import GNQTS

import config
import os
import pandas as pd
import numpy as np

if __name__ == "__main__":
    invest = sp.Stock_Price(config.Investment_start_date, config.Train_test_mode, config.Training_interval,
                            config.Investment_interval)
    Training_start_date, Training_end_date, Investment_start_date, Investment_end_date = invest.get_date()
    print("Training Starting Date: ", Training_start_date)
    print("Training End Date: ", Training_end_date)
    print("Investment Starting Date: ", Investment_start_date)
    print("Investment End Date: ", Investment_end_date)

    s_mode = str()
    if config.Train_test_mode == "continuous":
        s_mode = "con"
    elif config.Train_test_mode == "year-on-year":
        s_mode = "yoy"

    if config.Mode == "Train" or config.Mode == "All":
                #-----Prepare Train and Invest stock price data------#
        stock_price_data = list()

        #----Train data----#
        filename_train = "Stock_Price_Train_" + str(config.Investment_start_date) + "_" + str(config.Training_interval) + "_" + str(config.Investment_interval) + "_" + s_mode + ".csv"
        print(filename_train)
        if os.path.exists(filename_train):
            print("File exists, reading data...")
            stock_price_data = pd.read_csv(filename_train).values.tolist()
        else:
            print("Enquiring data...")
            stock_price_data = invest.get_stock_price(mode="Train", to_CSV=True, filename=filename_train).values.tolist()

        trend_ratio = tr.TrendRatio(stock_price_data, config.Initial_fund)
        stock_amount = len(stock_price_data[0])

        experiment_best = 0
        experiment_best_solution = np.zeros(stock_amount, dtype = int)
        for i in range(config.Experiment):
            gnqts = GNQTS(config.Generation, config.Solution_each_generation, stock_amount, trend_ratio, theta=config.step)
            gnqts.run()
            best, best_solution = gnqts.get_best()

            print(best, best_solution)

            if best > experiment_best:
                experiment_best = copy.deepcopy(best)
                experiment_best_solution = copy.deepcopy(best_solution)

        portfolio_file_filename = ".\Portfolio\Portfolio_" + str(config.Investment_start_date) + "_" + str(config.Training_interval) + "_" + str(config.Investment_interval) + "_" + s_mode + ".txt"
        with open(portfolio_file_filename, "w") as o:
            o.write(str(experiment_best_solution)[1:len(str(experiment_best_solution)) - 1])

    if config.Mode == "Invest" or config.Mode == "All":
        # -----Invest data-----#
        filename_invest = "Stock_Price_Invest_" + str(config.Investment_start_date) + "_" + str(
            config.Training_interval) + "_" + str(config.Investment_interval) + "_" + s_mode + ".csv"
        if os.path.exists(filename_invest):
            print("File exists, skip process...")
        else:
            print("Enquiring data...")
            invest.get_stock_price(mode="Invest", to_CSV=True, filename=filename_invest).values.tolist()

        s_mode = str()
        if config.Train_test_mode == "continuous":
            s_mode = "con"
        elif config.Train_test_mode == "year-on-year":
            s_mode = "yoy"

        filename_invest = "Stock_Price_Invest_" + str(config.Investment_start_date) + "_" + str(config.Training_interval) + "_" + str(config.Investment_interval) + "_" + s_mode + ".csv"
        stock_price_data = pd.read_csv(filename_invest).values.tolist()
        trend_ratio = tr.TrendRatio(stock_price_data, config.Initial_fund)

        #-----get portfolio solution-----#
        portfolio_solution_filename = ".\Portfolio\Portfolio_" + str(config.Investment_start_date) + "_" + str(config.Training_interval) + "_" + str(config.Investment_interval) + "_" + s_mode + ".txt"
        f = open(portfolio_solution_filename, "r")
        portfolio_solution = [int(ele) for ele in f.read().split(" ")]

        sum_selected_stock = np.sum(portfolio_solution)
        if sum_selected_stock == 0:
            print("no stock selected")
        else:
            trend_ratio.get_fitness(portfolio_solution)
            print(trend_ratio.get_return())
