# TradePredict AI

An end-to-end ML trading system with real-time data ingestion, LSTM price prediction, backtesting engine, and interactive dashboard.

## Features

- **Real-time Data**: Crypto (Binance) and Stock (Yahoo Finance) data via CCXT/yfinance
- **ML Predictions**: LSTM neural network with technical indicators (RSI, MACD, SMA, Bollinger Bands)
- **Backtesting**: Strategy backtesting with Sharpe ratio, max drawdown, win rate metrics
- **API**: FastAPI with `/predict`, `/signals`, `/backtest`, `/historical` endpoints
- **Dashboard**: Streamlit visualization with candlestick charts and signal alerts

## Quick Start

```bash
# Clone and setup
cd personalProject

# Build and run with Docker
docker-compose up --build

# Or run locally (after installing dependencies)
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run dashboard/app.py
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/predict/{symbol}` | Get price prediction |
| `GET /api/signals/{symbol}` | Get trading signals |
| `POST /api/backtest` | Run backtest |
| `GET /api/historical/{symbol}` | Get historical data |
| `GET /api/health` | Health check |

## Supported Symbols

- Crypto: BTC/USDT, ETH/USDT, SOL/USDT
- Stocks: AAPL, TSLA

## Tech Stack

- Python 3.10 | FastAPI | Streamlit
- TensorFlow/Keras (LSTM) | scikit-learn
- CCXT | yfinance | TA-Lib
- SQLite | Docker

## Project Structure

```
├── app/              # FastAPI backend
├── dashboard/        # Streamlit UI
├── models/           # ML models
├── services/         # Data, database, backtest
├── tests/            # Unit tests
└── data/             # SQLite database
```

## Demo

1. Open `http://localhost:8501` in browser
2. Select asset (BTC/USDT, ETH/USDT, etc.)
3. View predictions, signals, and run backtests