import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TestBacktestEngine:
    def test_calculate_indicators_rsi(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        close_prices = np.random.uniform(100, 110, 100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": close_prices,
            "symbol": "TEST"
        })
        
        result = engine.calculate_indicators(df)
        assert "rsi" in result.columns
        assert result["rsi"].notna().sum() > 0

    def test_calculate_indicators_sma(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        close_prices = np.linspace(100, 150, 100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": close_prices,
            "symbol": "TEST"
        })
        
        result = engine.calculate_indicators(df)
        assert "sma_20" in result.columns
        assert "sma_50" in result.columns

    def test_generate_signals_buy(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        close_prices = np.linspace(100, 150, 100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": close_prices,
            "symbol": "TEST"
        })
        
        result = engine.generate_signals(df)
        assert "signal" in result.columns

    def test_run_backtest_metrics(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        close_prices = np.linspace(100, 150, 100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": close_prices,
            "symbol": "TEST"
        })
        
        result = engine.run(df, initial_capital=10000)
        assert "final_value" in result
        assert "total_return" in result
        assert "sharpe_ratio" in result
        assert "max_drawdown" in result
        assert "win_rate" in result

    def test_run_backtest_no_trades(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        close_prices = np.ones(100) * 100
        df = pd.DataFrame({
            "timestamp": dates,
            "close": close_prices,
            "symbol": "TEST"
        })
        
        result = engine.run(df, initial_capital=10000)
        assert result["total_trades"] == 0
        assert result["final_value"] == 10000

    def test_run_backtest_profit(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        close_prices = np.linspace(100, 200, 100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": close_prices,
            "symbol": "TEST"
        })
        
        result = engine.run(df, initial_capital=10000)
        assert result["final_value"] >= 10000