import pytest
from portfolio_backtest import Backtest


@pytest.fixture(scope="module", autouse=True)
def scope_module():
    yield Backtest(
        # tickers=["VTI", "AGG", "GLD"]
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


@pytest.fixture(scope="function", autouse=True)
def backtest(scope_module):
    yield scope_module


# @pytest.mark.skip
def test_backtest(backtest):
    backtest.run()
