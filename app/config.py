import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR}/trading.db"

BINANCE_SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
STOCK_SYMBOLS = ["AAPL", "TSLA"]

DEFAULT_TIMEFRAME = "1d"
DEFAULT_LIMIT = 365

class Config:
    DATABASE_URL = DATABASE_URL
    BINANCE_SYMBOLS = BINANCE_SYMBOLS
    STOCK_SYMBOLS = STOCK_SYMBOLS
    DEFAULT_TIMEFRAME = DEFAULT_TIMEFRAME
    DEFAULT_LIMIT = DEFAULT_LIMIT
    MODEL_PATH = DATA_DIR / "models"
    MODEL_PATH.mkdir(exist_ok=True)