import ccxt
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
from app.config import Config

class DataFetcher:
    def __init__(self):
        try:
            self.binance = ccxt.binance({"enableRateLimit": True})
        except:
            self.binance = None

    def fetch_crypto(self, symbol: str, timeframe: str = "1d", limit: int = 365) -> pd.DataFrame:
        if self.binance is None:
            return self._generate_fallback_data(symbol, "crypto")
        
        try:
            ohlcv = self.binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["symbol"] = symbol.replace("/", "")
            return df
        except Exception as e:
            print(f"Crypto fetch error: {e}")
            return self._generate_fallback_data(symbol, "crypto")

    def fetch_stock(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if df.empty:
                return self._generate_fallback_data(symbol, "stock")
            df = df.reset_index()
            df["symbol"] = symbol
            df = df.rename(columns={"Date": "timestamp"})
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df[["timestamp", "Open", "High", "Low", "Close", "Volume", "symbol"]].rename(
                columns={"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}
            )
        except Exception as e:
            print(f"Stock fetch error: {e}")
            return self._generate_fallback_data(symbol, "stock")

    def _generate_fallback_data(self, symbol: str, data_type: str) -> pd.DataFrame:
        n = 100
        dates = pd.date_range(end=datetime.now(), periods=n, freq="D")
        
        if data_type == "crypto":
            base_price = 40000 if "BTC" in symbol else 2000
        else:
            base_price = 150 if symbol == "AAPL" else 200
        
        prices = base_price + np.cumsum(np.random.randn(n) * base_price * 0.02)
        prices = np.maximum(prices, base_price * 0.5)
        
        df = pd.DataFrame({
            "timestamp": dates,
            "open": prices * (1 + np.random.randn(n) * 0.01),
            "high": prices * (1 + np.abs(np.random.randn(n)) * 0.02),
            "low": prices * (1 - np.abs(np.random.randn(n)) * 0.02),
            "close": prices,
            "volume": np.random.randint(1000000, 10000000, n),
            "symbol": symbol.replace("/", "")
        })
        return df

    def fetch_all(self, symbol: str) -> pd.DataFrame:
        if "/" in symbol:
            return self.fetch_crypto(symbol)
        else:
            return self.fetch_stock(symbol)

fetcher = DataFetcher()