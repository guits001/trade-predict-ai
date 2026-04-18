from fastapi import APIRouter, HTTPException
from app.schemas.prediction import (
    PredictionResponse, BacktestRequest, BacktestResponse, SignalResponse
)
from app.services.data_fetcher import fetcher
from app.services.database import get_price_data, save_price_data
from app.models.lstm_model import predictor
from app.services.backtest import engine
import pandas as pd

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "service": "TradePredict AI"}

def normalize_symbol(symbol: str) -> str:
    crypto_symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    if symbol.upper() in crypto_symbols or "/" not in symbol:
        return symbol.upper().replace("USDT", "/USDT")
    return symbol

@router.get("/predict/{symbol}", response_model=PredictionResponse)
def predict(symbol: str):
    try:
        symbol = normalize_symbol(symbol)
        df = fetcher.fetch_all(symbol)
        
        if df is None or len(df) == 0:
            raise HTTPException(status_code=404, detail="No data found")
        
        current_price = float(df.iloc[-1]["close"])
        predicted_price = predictor.predict(df)
        
        if predicted_price is None:
            predicted_price = current_price
        
        return PredictionResponse(
            symbol=symbol,
            current_price=current_price,
            predicted_price=float(predicted_price),
            timestamp=df.iloc[-1]["timestamp"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical/{symbol}")
def historical(symbol: str, limit: int = 365):
    try:
        symbol = normalize_symbol(symbol)
        df = fetcher.fetch_all(symbol)
        save_price_data(df)
        df = df.tail(limit)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals/{symbol}", response_model=SignalResponse)
def signals(symbol: str):
    try:
        symbol = normalize_symbol(symbol)
        df = fetcher.fetch_all(symbol)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No data found")
        
        df = engine.calculate_indicators(df)
        latest = df.iloc[-1]
        
        current_price = latest["close"]
        rsi = latest["rsi"]
        sma_20 = latest["sma_20"]
        sma_50 = latest["sma_50"]
        
        if sma_20 > sma_50 and rsi < 70:
            signal = "BUY"
        elif sma_20 < sma_50 or rsi > 80:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        return SignalResponse(
            symbol=symbol,
            current_price=float(current_price),
            signal=signal,
            rsi=float(rsi) if pd.notna(rsi) else None,
            sma_20=float(sma_20) if pd.notna(sma_20) else None,
            sma_50=float(sma_50) if pd.notna(sma_50) else None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backtest", response_model=BacktestResponse)
def backtest(request: BacktestRequest):
    try:
        df = fetcher.fetch_all(request.symbol)
        if len(df) < 60:
            raise HTTPException(status_code=400, detail="Not enough data for backtest")
        
        result = engine.run(df, request.initial_capital)
        
        return BacktestResponse(
            symbol=request.symbol,
            initial_capital=result["initial_capital"],
            final_value=result["final_value"],
            total_return=result["total_return"],
            max_drawdown=result["max_drawdown"],
            sharpe_ratio=result["sharpe_ratio"],
            total_trades=result["total_trades"],
            win_rate=result["win_rate"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))