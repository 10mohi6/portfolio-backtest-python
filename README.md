# portfolio-backtest

[![PyPI](https://img.shields.io/pypi/v/portfolio-backtest)](https://pypi.org/project/portfolio-backtest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/10mohi6/portfolio-backtest-python/branch/main/graph/badge.svg?token=ZFgiyy2cc2)](undefined)
[![Build Status](https://travis-ci.com/10mohi6/portfolio-backtest-python.svg?branch=main)](https://travis-ci.com/10mohi6/portfolio-backtest-python)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/portfolio-backtest)](https://pypi.org/project/portfolio-backtest/)
[![Downloads](https://pepy.tech/badge/portfolio-backtest)](https://pepy.tech/project/portfolio-backtest)

portfolio-backtest is a python library for backtest portfolio asset allocation on Python 3.6 and above.

## Installation

    $ pip install portfolio-backtest

## Usage

### basic run
```python
from portfolio_backtest import Backtest

Backtest(tickers=["VTI", "AGG", "GLD"]).run()
```
![tangency-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/tangency-portfolio.png)
![minimum-variance-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/minimum-variance-portfolio.png)
![hrp-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/hrp-portfolio.png)
![minimum-cvar-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/minimum-cvar-portfolio.png)
![cumulative-return.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/cumulative-return.png)

### advanced run
```python
from portfolio_backtest import Backtest

Backtest(
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
).run()
```
![advanced-your-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-your-portfolio.png)
![advanced-tangency-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-tangency-portfolio.png)
![advanced-minimum-variance-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-minimum-variance-portfolio.png)
![advanced-hrp-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-hrp-portfolio.png)
![advanced-minimum-cvar-portfolio.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-minimum-cvar-portfolio.png)
![advanced-return-maximize-cvar-portfolio-(target-cvar-2.5%).png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-return-maximize-cvar-portfolio-(target-cvar-2.5%).png)
![advanced-semi-variance-portfolio-(target-return-10.0%).png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-semi-variance-portfolio-(target-return-10.0%).png)
![advanced-cumulative-return.png](https://raw.githubusercontent.com/10mohi6/portfolio-backtest-python/main/tests/advanced-cumulative-return.png)

## Supported Portfolio
- Your Portfolio
- Hierarchical Risk Parity (HRP) Portfolio
- Tangency Portfolio
- Minimum Variance Portfolio
- Minimum CVaR Portfolio
- Semi Variance Portfolio
- Return Maximize CVaR Portfolio
