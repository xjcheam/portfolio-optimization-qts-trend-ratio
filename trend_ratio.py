import numpy as np
import math

class TrendRatio:
    def __init__(self, price_data, initial_fund):
        self.price_data = price_data
        self.initial_fund = initial_fund
        self.solution = np.empty(0)

        self.amount_of_stock_to_choose = len(self.price_data[0])
        self.amount_of_stock_to_invest = np.sum(self.solution)
        self.total_investment_day = len(self.price_data)
        self.everyday_stocks_fund = np.empty(self.total_investment_day, self.amount_of_stock_to_invest )
        self.everyday_total_fund = np.empty(self.total_investment_day)

        self.trend_ratio = 0

    def fund_standardization(self):
        self.everyday_stock_fund = np.zeros((self.total_investment_day, self.amount_of_stock_to_invest))

        allocated_fund_for_each_stock = self.initial_fund / self.amount_of_stock_to_invest
        remain_from_all_stock = self.initial_fund - allocated_fund_for_each_stock * self.amount_of_stock_to_invest

        chosen_stock_index = 0
        num_of_lots = np.empty(self.amount_of_stock_to_invest)
        remains_from_one_stock = np.empty(self.amount_of_stock_to_invest)

        for row_index in range(self.total_investment_day):
            if row_index == 0:  #first day of investment
                for stock_index in range(self.amount_of_stock_to_choose):
                    if self.solution[stock_index] == 1:
                        charges = (allocated_fund_for_each_stock * 0.01) + 10
                        available_fund_for_each_stock_after_charges = allocated_fund_for_each_stock - charges
                        lot_price = self.price_data[0][stock_index] * 100
                        num_of_lots[chosen_stock_index] = available_fund_for_each_stock_after_charges // lot_price
                        remains_from_one_stock[chosen_stock_index] = available_fund_for_each_stock_after_charges - (lot_price * num_of_lots[chosen_stock_index])
                        self.everyday_stock_fund[row_index][chosen_stock_index] = available_fund_for_each_stock_after_charges
                        chosen_stock_index += 1
                chosen_stock_index = 0
            else:
                for stock_index in range(self.amount_of_stock_to_choose):
                    if self.solution[stock_index] == 1:
                        if num_of_lots[chosen_stock_index] > 0:
                            fund_on_sell = self.price_data[row_index][stock_index] * 100 * num_of_lots[chosen_stock_index]
                            charges = (fund_on_sell * 0.01) + 10
                            self.everyday_stock_fund[row_index][chosen_stock_index] = fund_on_sell - charges + remains_from_one_stock[chosen_stock_index]
                        else:
                            self.everyday_stock_fund[row_index][chosen_stock_index] = remains_from_one_stock[chosen_stock_index]
                        chosen_stock_index += 1
                chosen_stock_index = 0

            self.everyday_total_fund[row_index] = np.sum(self.everyday_stock_fund[row_index]) + remain_from_all_stock

    def linear_trend_ratio(self):
        assumption_fund = np.empty(self.total_investment_day)
        squared_difference = 0

        numerator = 0
        denominator = 0

        for day_index in range(self.total_investment_day):
            x_i = day_index + 1
            numerator += (x_i * self.everyday_total_fund[day_index] - x_i * self.initial_fund)
            denominator += x_i * x_i

        slope = numerator / denominator

        for day_index in range(self.total_investment_day):
            assumption_fund[day_index] = slope * (day_index + 1) + self.initial_fund
            squared_difference += ((self.everyday_total_fund[day_index] - assumption_fund[day_index]) * (self.everyday_total_fund[day_index] - assumption_fund[day_index]))

        risk = math.sqrt(squared_difference / (self.total_investment_day))

        self.trendRatio = slope/risk #slope is the daily expected return; risk is daily risk

        return self.trendRatio

    def get_fitness(self, solution):
        self.solution = solution
        self.amount_of_stock_to_invest = np.sum(self.solution)
        self.fund_standardization()
        self.linear_trend_ratio()
        return self.trendRatio

    def get_stock_amount(self):
        return self.amount_of_stock_to_choose

    def get_everyday_stock_fund(self):
        return self.everyday_stock_fund

    def get_everyday_total_fund(self):
        return self.everyday_total_fund

    def get_return(self):
        last_day_fund = self.everyday_total_fund[len(self.everyday_total_fund) - 1]
        nett_return = last_day_fund - self.initial_fund
        return nett_return