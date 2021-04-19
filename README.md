# portfolio-backtest

[![PyPI](https://img.shields.io/pypi/v/portfolio-backtest)](https://pypi.org/project/portfolio-backtest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/10mohi6/portfolio-backtest-python/branch/main/graph/badge.svg?token=EYDOX015ZS)](https://codecov.io/gh/10mohi6/portfolio-backtest-python)
[![Build Status](https://travis-ci.com/10mohi6/portfolio-backtest-python.svg?branch=main)](https://travis-ci.com/10mohi6/portfolio-backtest-python)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/portfolio-backtest)](https://pypi.org/project/portfolio-backtest/)
[![Downloads](https://pepy.tech/badge/portfolio-backtest)](https://pepy.tech/project/portfolio-backtest)

portfolio-backtest is a python library for backtest portfolio asset allocation on Python 3.7 and above.

## Installation

    $ pip install portfolio-backtest
    $ pip install PyPortfolioOpt

## Usage

### basic run
```python
from portfolio_backtest import Backtest

Backtest(tickers=["VTI", "AGG", "GLD"]).run()
```
![tangency-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/tangency-portfolio.png)
![minimum-variance-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/minimum-variance-portfolio.png)
![hierarchical-risk-parity-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/hierarchical-risk-parity-portfolio.png)
![minimum-cvar-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/minimum-cvar-portfolio.png)
![cumulative-return.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/cumulative-return.png)

### advanced run
```python
from portfolio_backtest import Backtest
import pprint

bt = Backtest(
    tickers={
        "VTI": 0.6,
        "AGG": 0.25,
        "GLD": 0.15,
    },
    target_return=0.1,
    target_cvar=0.025,
    data_dir="data",
    start="2011-04-10",
    end="2021-04-10",
)
pprint.pprint(bt.run(plot=True))
```
```python
[{'Annual volatility': '10.9%',
  'Conditional Value at Risk': '',
  'Cumulative Return': '160.9%',
  'Expected annual return': '9.6%',
  'Sharpe Ratio': '0.70',
  'portfolio': 'Your Portfolio',
  'tickers': {'AGG': 0.25, 'GLD': 0.15, 'VTI': 0.6}},
 {'Annual volatility': '6.3%',
  'Conditional Value at Risk': '',
  'Cumulative Return': '102.3%',
  'Expected annual return': '7.0%',
  'Sharpe Ratio': '0.79',
  'portfolio': 'Tangency Portfolio',
  'tickers': {'AGG': 0.67099, 'GLD': 0.0, 'VTI': 0.32901}},
 {'Annual volatility': '4.3%',
  'Conditional Value at Risk': '',
  'Cumulative Return': '53.3%',
  'Expected annual return': '4.3%',
  'Sharpe Ratio': '0.53',
  'portfolio': 'Minimum Variance Portfolio',
  'tickers': {'AGG': 0.91939, 'GLD': 0.00525, 'VTI': 0.07536}},
 {'Annual volatility': '4.0%',
  'Conditional Value at Risk': '',
  'Cumulative Return': '48.7%',
  'Expected annual return': '4.1%',
  'Sharpe Ratio': '0.51',
  'portfolio': 'Hierarchical Risk Parity Portfolio',
  'tickers': {'AGG': 0.89041, 'GLD': 0.05695, 'VTI': 0.05263}},
 {'Annual volatility': '',
  'Conditional Value at Risk': '0.5%',
  'Cumulative Return': '52.1%',
  'Expected annual return': '4.2%',
  'Sharpe Ratio': '',
  'portfolio': 'Minimum CVaR Portfolio',
  'tickers': {'AGG': 0.93215, 'GLD': 0.0, 'VTI': 0.06785}},
 {'Annual volatility': '7.7%',
  'Conditional Value at Risk': '',
  'Cumulative Return': '166.5%',
  'Expected annual return': '10.0%',
  'Sharpe Ratio': '1.04',
  'portfolio': 'Semi Variance Portfolio (target return 10.0%)',
  'tickers': {'AGG': 0.39504, 'GLD': 0.0, 'VTI': 0.60496}},
 {'Annual volatility': '',
  'Conditional Value at Risk': '2.5%',
  'Cumulative Return': '251.3%',
  'Expected annual return': '13.3%',
  'Sharpe Ratio': '',
  'portfolio': 'Return Maximize CVaR Portfolio (target CVaR 2.5%)',
  'tickers': {'AGG': 0.08851, 'GLD': 0.0, 'VTI': 0.91149}}]
```
![advanced-your-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-your-portfolio.png)
![advanced-tangency-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-tangency-portfolio.png)
![advanced-minimum-variance-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-minimum-variance-portfolio.png)
![advanced-hierarchical-risk-parity-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-hierarchical-risk-parity-portfolio.png)
![advanced-minimum-cvar-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-minimum-cvar-portfolio.png)
![advanced-return-maximize-cvar-portfolio-(target-cvar-2.5%).png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-return-maximize-cvar-portfolio-(target-cvar-2.5%25).png)
![advanced-semi-variance-portfolio-(target-return-10.0%).png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-semi-variance-portfolio-(target-return-10.0%25).png)
![advanced-cumulative-return.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-cumulative-return.png)

## Supported Portfolio
- Your Portfolio
- Hierarchical Risk Parity Portfolio
- Tangency Portfolio
- Minimum Variance Portfolio
- Minimum CVaR Portfolio
- Semi Variance Portfolio
- Return Maximize CVaR Portfolio
