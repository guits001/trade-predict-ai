import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TestPredictor:
    def test_add_indicators(self):
        from app.models.lstm_model import MLPPredictor
        predictor = MLPPredictor()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        df = pd.DataFrame({
            "timestamp": dates,
            "open": np.random.uniform(100, 110, 100),
            "high": np.random.uniform(105, 120, 100),
            "low": np.random.uniform(95, 105, 100),
            "close": np.random.uniform(100, 110, 100),
            "volume": np.random.uniform(1000, 5000, 100),
            "symbol": "TEST"
        })
        
        result = predictor.add_indicators(df)
        assert "rsi" in result.columns
        assert "macd" in result.columns
        assert "sma_20" in result.columns

    def test_create_features(self):
        from app.models.lstm_model import MLPPredictor
        predictor = MLPPredictor()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        df = pd.DataFrame({
            "timestamp": dates,
            "open": np.random.uniform(100, 110, 100),
            "high": np.random.uniform(105, 120, 100),
            "low": np.random.uniform(95, 105, 100),
            "close": np.random.uniform(100, 110, 100),
            "volume": np.random.uniform(1000, 5000, 100),
            "symbol": "TEST"
        })
        
        X, y, processed = predictor.create_features(df)
        assert X.shape[0] > 0
        assert len(y) == X.shape[0]


class TestBacktest:
    def test_calculate_indicators(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": np.random.uniform(100, 110, 100),
            "symbol": "TEST"
        })
        
        result = engine.calculate_indicators(df)
        assert "sma_20" in result.columns
        assert "rsi" in result.columns

    def test_run_backtest(self):
        from app.services.backtest import BacktestEngine
        engine = BacktestEngine()
        
        dates = pd.date_range(end=datetime.now(), periods=100)
        df = pd.DataFrame({
            "timestamp": dates,
            "close": np.linspace(100, 150, 100),
            "symbol": "TEST"
        })
        
        result = engine.run(df, initial_capital=10000)
        assert "total_return" in result
        assert "sharpe_ratio" in result
        assert "max_drawdown" in result
        assert result["initial_capital"] == 10000