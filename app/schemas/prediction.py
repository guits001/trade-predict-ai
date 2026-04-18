from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    symbol: str

class PredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predicted_price: float
    timestamp: datetime

class BacktestRequest(BaseModel):
    symbol: str
    initial_capital: Optional[float] = 10000
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class BacktestResponse(BaseModel):
    symbol: str
    initial_capital: float
    final_value: float
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    total_trades: int
    win_rate: float

class SignalResponse(BaseModel):
    symbol: str
    current_price: float
    signal: str
    rsi: Optional[float]
    sma_20: Optional[float]
    sma_50: Optional[float]