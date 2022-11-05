from bs4 import BeautifulSoup as bs
from datetime import date
import yfinance as yf
import requests
import re
import config

class Stock_Price:
    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(self, investment_start_date, train_test_mode, training_interval, investment_interval):
        self.investment_start_date = investment_start_date
        self.investment_end_date = [int(ele) for ele in self.investment_start_date.split("-")]
        self.training_start_date = [int(ele) for ele in self.investment_start_date.split("-")]
        self.training_end_date = [int(ele) for ele in self.investment_start_date.split("-")]

        self.train_test_mode = train_test_mode
        self.training_interval = training_interval
        self.investment_interval = investment_interval

        self.__investment_period()
        
    def get_stock_price(self, mode="Train", to_CSV=False, filename=""):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        r = requests.get('https://finance.yahoo.com/quote/%5EKLSE/components/',headers=headers)
        soup = bs(r.content,'lxml')
        stock_set = []
        for line in soup:
            stock_set = re.findall(r'[0-9]{4}\.KL', str(line))
        stock_set = " ".join(list(set(stock_set)))

        start_date = list()
        end_date = list()

        if mode == "Train":
            start_date = self.training_start_date
            end_date = self.training_end_date
        elif mode == "Invest":
            start_date = self.investment_start_date
            end_date = self.investment_end_date

        print("Start date: ", start_date, "  End date: ", end_date, "  Mode: ", mode)
        data = yf.download(stock_set, start=start_date, end=end_date)
        data = data.loc[:, ['Adj Close']]
        data.columns = [col[1] for col in data.columns.values]

        self.stock_amount = len(data.dropna().values.tolist()[0])

        if to_CSV:
            print("Writing data to ", filename)
            data.dropna().to_csv(filename, index=False)

        return(data.dropna())

    def get_date(self):
        return self.training_start_date, self.training_end_date, self.investment_start_date, self.investment_end_date

    def __investment_period(self):
        
        #---Find Train Date---#
        if self.train_test_mode == "continuous":
            #---Find Training End Date---#
            self.training_end_date[2] -= 1
            self.training_end_date = self.check_date(self.training_end_date)

            #---Find Training Start Date---#
            if self.training_interval == "1M":
                if self.check_last_day_of_month(self.training_start_date):
                    self.training_start_date[1] -= 1
                    if self.training_start_date[1] == 0:
                        self.training_start_date[2] = Stock_Price.days_in_months[11]
                    else:
                        self.training_start_date[2] = Stock_Price.days_in_months[self.training_start_date[1] - 1]
                else:
                    self.training_start_date[1] -= 1
            elif self.training_interval == "3M":
                if self.check_last_day_of_month(self.training_start_date):
                    self.training_start_date[1] -= 3
                    if self.training_start_date[1] <= 0:
                        self.training_start_date[1] += 12
                        self.training_start_date[2] = Stock_Price.days_in_months[self.training_start_date[1] - 1]
                    else:
                        self.training_start_date[2] = Stock_Price.days_in_months[self.training_start_date[1] - 1]
                else:
                    self.training_start_date[1] -= 3
            elif self.training_interval == "6M":
                if self.check_last_day_of_month(self.training_start_date):
                    self.training_start_date[1] -= 6
                    if self.training_start_date[1] <= 0:
                        self.training_start_date[1] += 12
                        self.training_start_date[2] = Stock_Price.days_in_months[self.training_start_date[1] - 1]
                    else:
                        self.training_start_date[2] = Stock_Price.days_in_months[self.training_start_date[1] - 1]
                else:
                    self.training_start_date[1] -= 6
            elif self.training_interval == "1Y":
                self.training_start_date[0] -= 1

            self.training_start_date = self.check_date(self.training_start_date)
        elif self.train_test_mode == "year-on-year":
            #---Find Training Start Date---#
            self.training_start_date[0] -= 1
            self.check_date(self.training_start_date)

            #--- Find Training Interval---#
            if self.training_interval == "1M":
                if self.training_end_date[2] == 1:
                    self.training_end_date[0] -= 1
                    self.training_end_date[2] = Stock_Price.days_in_months[self.training_end_date[1] - 1]
                else:
                    if self.check_last_day_of_month(self.training_end_date):
                        self.training_end_date[0] -= 1
                        self.training_end_date[1] += 1
                        if self.training_end_date[1] > 12:
                            self.training_end_date[1] -= 12
                            self.training_end_date[0] += 1
                        self.training_end_date[2] = Stock_Price.days_in_months[self.training_end_date[1] - 1] - 1
                    else:
                        self.training_end_date[0] -= 1
                        self.training_end_date[1] += 1
                        if self.training_end_date[1] > 12:
                            self.training_end_date[1] -= 12
                            self.training_end_date[0] += 1
                        self.training_end_date[2] -= 1
            elif self.training_interval == "3M":
                if self.training_end_date[2] == 1:
                    self.training_end_date[0] -= 1
                    self.training_end_date[1] += 2
                    if self.training_end_date[1] > 12:
                        self.training_end_date[1] -= 12
                        self.training_end_date[0] += 1
                    self.training_end_date[2] = Stock_Price.days_in_months[self.training_end_date[1] - 1]
                else:
                    if self.check_last_day_of_month(self.training_end_date):
                        self.training_end_date[0] -= 1
                        self.training_end_date[1] += 3
                        if self.training_end_date[1] > 12:
                            self.training_end_date[1] -= 12
                            self.training_end_date[0] += 1
                        self.training_end_date[2] = Stock_Price.days_in_months[self.training_end_date[1] - 1] - 1
                    else:
                        self.training_end_date[0] -= 1
                        self.training_end_date[1] += 3
                        if self.training_end_date[1] > 12:
                            self.training_end_date[1] -= 12
                            self.training_end_date[0] += 1
                        self.training_end_date[2] -= 1
            elif self.training_interval == "6M":
                if self.training_end_date[2] == 1:
                    self.training_end_date[0] -= 1
                    self.training_end_date[1] += 5
                    if self.training_end_date[1] > 12:
                        self.training_end_date[1] -= 12
                        self.training_end_date[0] += 1
                    self.training_end_date[2] = Stock_Price.days_in_months[self.training_end_date[1] - 1]
                else:
                    if self.check_last_day_of_month(self.training_end_date):
                        self.training_end_date[0] -= 1
                        self.training_end_date[1] += 6
                        if self.training_end_date[1] > 12:
                            self.training_end_date[1] -= 12
                            self.training_end_date[0] += 1
                        self.training_end_date[2] = Stock_Price.days_in_months[self.training_end_date[1] - 1] - 1
                    else:
                        self.training_end_date[0] -= 1
                        self.training_end_date[1] += 6
                        if self.training_end_date[1] > 12:
                            self.training_end_date[1] -= 12
                            self.training_end_date[0] += 1
                        self.training_end_date[2] -= 1

            self.training_end_date = self.check_date(self.training_end_date)

        # --- Find Investment Interval---#
        if self.investment_interval == "1M":
            if self.investment_end_date[2] == 1:
                self.investment_end_date[2] = Stock_Price.days_in_months[self.investment_end_date[1] - 1]
            else:
                if self.check_last_day_of_month(self.investment_end_date):
                    self.investment_end_date[1] += 1
                    if self.investment_end_date[1] > 12:
                        self.investment_end_date[1] -= 12
                        self.investment_end_date[0] += 1
                    self.investment_end_date[2] = Stock_Price.days_in_months[self.investment_end_date[1] - 1] - 1
                else:
                    self.investment_end_date[1] += 1
                    if self.investment_end_date[1] > 12:
                        self.investment_end_date[1] -= 12
                        self.investment_end_date[0] += 1
                    self.investment_end_date[2] -= 1
        elif self.investment_interval == "3M":
            if self.investment_end_date[2] == 1:
                self.investment_end_date[1] += 2
                if self.investment_end_date[1] > 12:
                    self.investment_end_date[1] -= 12
                    self.investment_end_date[0] += 1
                self.investment_end_date[2] = Stock_Price.days_in_months[self.investment_end_date[1] - 1]
            else:
                if self.check_last_day_of_month(self.training_end_date):
                    self.investment_end_date[1] += 3
                    if self.training_end_date[1] > 12:
                        self.investment_end_date[1] -= 12
                        self.investment_end_date[0] += 1
                    self.investment_end_date[2] = Stock_Price.days_in_months[self.investment_end_date[1] - 1] - 1
                else:
                    self.investment_end_date[1] += 3
                    if self.investment_end_date[1] > 12:
                        self.investment_end_date[1] -= 12
                        self.investment_end_date[0] += 1
                    self.investment_end_date[2] -= 1
        elif self.investment_interval == "6M":
            if self.investment_end_date[2] == 1:
                self.investment_end_date[1] += 5
                if self.investment_end_date[1] > 12:
                    self.investment_end_date[1] -= 12
                    self.investment_end_date[0] += 1
                self.investment_end_date[2] = Stock_Price.days_in_months[self.investment_end_date[1] - 1]
            else:
                if self.check_last_day_of_month(self.investment_end_date):
                    self.investment_end_date[1] += 6
                    if self.investment_end_date[1] > 12:
                        self.investment_end_date[1] -= 12
                        self.investment_end_date[0] += 1
                    self.investment_end_date[2] = Stock_Price.days_in_months[self.investment_end_date[1] - 1] - 1
                else:
                    self.investment_end_date[1] += 6
                    if self.investment_end_date[1] > 12:
                        self.investment_end_date[1] -= 12
                        self.investment_end_date[0] += 1
                    self.investment_end_date[2] -= 1

        self.investment_end_date = self.check_date(self.investment_end_date)

        self.training_start_date = str(date(*self.training_start_date))
        self.training_end_date = str(date(*self.training_end_date))
        self.investment_end_date = str(date(*self.investment_end_date))

    def check_last_day_of_month(self, date):
        if date[2] == Stock_Price.days_in_months[date[1] - 1]:
            return True
        else:
            return False

    def check_date(self, date):

        if date[2] == 0:
            date[1] -= 1
            date[2] = Stock_Price.days_in_months[date[1]-1]

        if date[2] == 2 and date[0] // 4 == 0:
            date[2] += 1

        if date[1] <= 0:
            date[1] += 12
            date[0] -= 1

        if date[1] >= 13:
            date[1] = 12 - date[1]
            date[0] += 1

        if date[2] > Stock_Price.days_in_months[date[1] - 1]:
            date[2] = Stock_Price.days_in_months[date[1] - 1]

        return date