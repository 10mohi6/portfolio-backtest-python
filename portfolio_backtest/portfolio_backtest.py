import os
from typing import Any, Tuple
import yfinance as yf
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
import sys

# from pypfopt import risk_models
from pypfopt import expected_returns, EfficientSemivariance, EfficientCVaR
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt import HRPOpt
from datetime import datetime, timedelta
import pandas as pd


class Backtest(object):
    def __init__(
        self,
        *,
        tickers: Any,
        start: str = "",
        end: str = "",
        target_return: float = 0,
        target_cvar: float = 0,
        data_dir: str = ".",
    ) -> None:
        self.target_cvar = target_cvar
        self.target_return = target_return
        self.tickers = tickers
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if type(self.tickers) is list:
            self.ticker_keys = self.tickers
            self.ticker_values = []
        elif type(self.tickers) is dict:
            self.ticker_keys = self.tickers.keys()
            self.ticker_values = self.tickers.values()
            if sum(self.ticker_values) != 1:
                raise Exception("total ticker rate must be 1.")
        else:
            raise Exception("tickers must be list or dictionary type.")
        f = "{}/{}-{}-{}.csv".format(
            self.data_dir, "-".join(self.ticker_keys), start, end
        )
        overtime = True
        if os.path.exists(f):
            overtime = datetime.now() > (
                datetime.fromtimestamp(os.path.getmtime(f)) + timedelta(hours=1)
            )
        if overtime:
            if start != "" or end != "":
                if start == "":
                    start = "1985-01-01"
                if end == "":
                    end = datetime.now().strftime("%Y-%m-%d")
                self.df = yf.download(
                    tickers=" ".join(self.ticker_keys),
                    start=start,
                    end=end,
                    interval="1d",
                )["Adj Close"].dropna()
            else:
                self.df = yf.download(
                    tickers=" ".join(self.ticker_keys), period="max", interval="1d"
                )["Adj Close"].dropna()

            self.df.to_csv(f)
        else:
            self.df = pd.read_csv(f, index_col="Date", parse_dates=True)
        self.mu = expected_returns.mean_historical_return(self.df)
        # self.S = risk_models.sample_cov(self.df)
        self.S = CovarianceShrinkage(self.df).ledoit_wolf()

    def _cumulative_return(self) -> None:
        if len(self.ticker_values) > 0:
            df = self._df(self.weights_your)
            plt.plot(df.index, df.values, label="Your Portfolio")
        df = self._df(self.weights_tangency)
        plt.plot(df.index, df.values, label="Tangency Portfolio")
        df = self._df(self.weights_minimum)
        plt.plot(df.index, df.values, label="Minimum Variance Portfolio")
        df = self._df(self.weights_hrp)
        plt.plot(df.index, df.values, label="HRP Portfolio")
        df = self._df(self.weights_minimum_cvar)
        plt.plot(df.index, df.values, label="Minimum CVaR Portfolio")
        if self.target_return != 0:
            df = self._df(self.weights_semi)
            plt.plot(df.index, df.values, label="Semi Variance Portfolio")
        if self.target_cvar != 0:
            df = self._df(self.weights_maximize_cvar)
            plt.plot(df.index, df.values, label="Return Maximize CVaR Portfolio")

        plt.title("Cumulative Return")
        plt.tick_params(right=True, labelright=True)
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return %")
        plt.legend()
        plt.savefig(f"{self.data_dir}/cumulative-return.png")
        plt.clf()
        plt.close()

    def _df(self, weights: Any) -> pd.DataFrame:
        return (
            self.df.pct_change()
            .dot(list(weights.values()))
            .add(1)
            .cumprod()
            .subtract(1)
            .multiply(100)
        )

    def _hrp_portfolio(self) -> None:
        rets = expected_returns.returns_from_prices(self.df)
        hrp = HRPOpt(rets)
        hrp.optimize()
        self.weights_hrp = hrp.clean_weights()
        self._plot_pie(
            p=hrp.portfolio_performance(),
            title="HRP Portfolio",
            weights=self.weights_hrp,
        )

    def _tangency_portfolio(self) -> None:
        ef = EfficientFrontier(self.mu, self.S)
        ef.max_sharpe()
        self.weights_tangency = ef.clean_weights()
        self._plot_pie(
            p=ef.portfolio_performance(),
            title="Tangency Portfolio",
            weights=self.weights_tangency,
        )

    def _minimum_variance_portfolio(self) -> None:
        ef = EfficientFrontier(self.mu, self.S)
        ef.min_volatility()
        self.weights_minimum = ef.clean_weights()
        self._plot_pie(
            p=ef.portfolio_performance(),
            title="Minimum Variance Portfolio",
            weights=self.weights_minimum,
        )

    def _semi_variance_portfolio(self) -> None:
        returns = expected_returns.returns_from_prices(self.df)
        es = EfficientSemivariance(self.mu, returns)
        try:
            es.efficient_return(self.target_return)
        except ValueError as e:
            print(e)
            sys.exit()
        self.weights_semi = es.clean_weights()
        self._plot_pie(
            p=es.portfolio_performance(),
            title="Semi Variance Portfolio (target return {:.1f}%)".format(
                self.target_return * 100
            ),
            weights=self.weights_semi,
        )

    def _minimum_cvar_portfolio(self) -> None:
        returns = expected_returns.returns_from_prices(self.df)
        ec = EfficientCVaR(self.mu, returns)
        ec.min_cvar()
        self.weights_minimum_cvar = ec.clean_weights()
        self._plot_pie(
            p=ec.portfolio_performance(),
            title="Minimum CVaR Portfolio",
            weights=self.weights_minimum_cvar,
        )

    def _return_maximize_cvar_portfolio(self) -> None:
        returns = expected_returns.returns_from_prices(self.df)
        ec = EfficientCVaR(self.mu, returns)
        ec.efficient_risk(target_cvar=self.target_cvar)
        self.weights_maximize_cvar = ec.clean_weights()
        self._plot_pie(
            p=ec.portfolio_performance(),
            title="Return Maximize CVaR Portfolio (target CVaR {:.1f}%)".format(
                self.target_cvar * 100
            ),
            weights=self.weights_maximize_cvar,
        )

    def _your_portfolio(self) -> None:
        ef = EfficientFrontier(self.mu, self.S)
        for k, v in self.tickers.items():
            ef.add_constraint(lambda w: w[ef.tickers.index(k)] == v)
        ef.max_sharpe()
        self.weights_your = ef.clean_weights()
        self._plot_pie(
            p=ef.portfolio_performance(),
            title="Your Portfolio",
            weights=self.weights_your,
        )

    def _plot_pie(self, *, p: Tuple, title: str, weights: dict) -> None:
        if len(p) < 3:
            plt.text(
                -2.1,
                -1.5,
                "Expected annual return: {}\nConditional Value at Risk: {}".format(
                    "{:.1f}%".format(p[0] * 100),
                    "{:.1f}%".format(p[1] * 100),
                ),
            )
        else:
            plt.text(
                -2.1,
                -1.5,
                "Expected annual return: {}\
                    \nAnnual volatility: {}\nSharpe Ratio: {}".format(
                    "{:.1f}%".format(p[0] * 100),
                    "{:.1f}%".format(p[1] * 100),
                    "{:.2f}".format(p[2]),
                ),
            )
        plt.title(title)
        plt.pie(
            weights.values(),
            labels=weights.keys(),
            autopct="%1.1f%%",
            normalize=True,
            # counterclock=False,
            # startangle=90,
            # pctdistance=0.6,
        )
        plt.savefig(f"{self.data_dir}/{title.replace(' ','-').lower()}.png")
        plt.clf()
        plt.close()

    def run(self):
        if len(self.ticker_values) > 0:
            self._your_portfolio()
        self._tangency_portfolio()
        self._minimum_variance_portfolio()
        self._hrp_portfolio()
        self._minimum_cvar_portfolio()
        if self.target_return != 0:
            self._semi_variance_portfolio()
        if self.target_cvar != 0:
            self._return_maximize_cvar_portfolio()
        self._cumulative_return()
