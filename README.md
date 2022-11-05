# Table of Contents
1. [Introduction](#introduction)
    1. [Supported Stock Combinations](#supported-stock-combinations)
2. [How to use the code](#how-to-use-the-code)
    1. [Dependencies](#dependencies)
    2. [config.py](#configpy)
    3. [Guide](#guide)
3. [References](#references)

# Introduction
[This paper](https://ieeexplore.ieee.org/document/8616267) proposed to use Quantum-inspired Tabu Search algorithm improved by the quantum-not-gate (GNQTS) and trend ratio to approache portfolio optimization problem.

This is a replication of the [the paper](https://ieeexplore.ieee.org/document/8616267) for real time investment portfolio optimization, uses GNQTS and trend ratio. The code acquire up-to-date stock price data to train and test. Users could define prefered investment date and the best training result will be saved. When investment interval starts, users could use the code to check current investment return.

However, the source of data and the stocks combinations to choose from might be different from the paper, therefore, the results of this code might not be consistant with the result of the paper. The data are acquired from yahoo finance, and the supported stocks [combinations](#supported-stock-combinations) are shown below.

## Supported Stock Combinations
1. KLSE

# How to use the code
## Dependencies
1. beautifulsoup4
2. yfinance
3. QTS 
## config.py
1. Change setting in config.py to fit your preference.
    - **Mode**: The mode to run. Supports three modes. 
        - All: Run train then test. 
        - Train: Run train only.
        - Test: Run Test only.

    - **Investment_start_date**: The start date of your investment period. A reference for all other date, including train start date, train end date and investment end date. 

    - **Train_test_mode**: The mode of train and test interval. 
        - continuous: This mode uses the data from an interval before investment start date to train. Refer cited [reference](#reference) M2M, Q2Q, H2H, Y2Y, etc.
        - year-on-year: This mode uses the data a year before as the investment start date. Refer cited [reference](#reference) M*, Q*, H*.

    - **Training_interval**: The interval of train. Supports 3 training interval for year-on-year train test mode, and 4 training interval for continuous mode.
        - 1M: 1 month, takes one month data to train. Available for both train test mode. 
        - 3M: 3 months, take three months data to train. Available for both train test mode.
        - 6M: 6 months, take six months data to train. Available for two train test mode.
        - 1Y: 1 year, take one year datat to train. Only available for "Continuous" type train test mode. Uses the data one year before from the investment start date.

    - **Initial_fund**: The initial fund of investment.

    - **Experiment**: The amount of experiment in one execution. Choose the best from totoal experiments.

    - **Generation**: Total generation in one experiment.

    - **Solution_each_generation**: The amount of solution in one generation (iteration).

    - **theta**: The size of step to update beta-matrix, use in QTS, NQTS, GQTS and GNQTS.

    - **theta_upper**: The upper bound of the size of step to update beta-matrix, use in ANQTS and ANGQTS.

    - **theta_lower**: The lower bound of the size of step to update beta-matrix, use in ANQTS and ANGQTS.

## Guide
1. Git clone the repository to your local computer.
2. Install the dependencies if you have not.
```python
   > pip install beautifulsoup4
   > pip install yfinance
```
3. Follow [QTS](https://github.com/xjcheam/quantum-inspired-tabu-search) package installation.
4. Navigate to the directory in terminal, change config.py details to match your experiment preferences and run.
```python
   > python main.py
```
\* Users do not require to download stock price manually. When the code is executed, it automatically acquire stock data according to details in config.py.

# References
1. Y. -C. Jiang, X. J. Cheam, C. -Y. Chen, S. -Y. Kuo and Y. -H. Chou, "A Novel Portfolio Optimization with Short Selling Using GNQTS and Trend Ratio," 2018 IEEE International Conference on Systems, Man, and Cybernetics (SMC), 2018, pp. 1564-1569, doi: 10.1109/SMC.2018.00271.