# Trading & Prediction System - Specification

## 1. Project Overview

**Project Name:** TradePredict AI  
**Type:** End-to-End ML Trading System  
**Core Functionality:** Real-time cryptocurrency data ingestion, ML-based price prediction, backtesting engine, and interactive dashboard with trading signals  
**Target Users:** Recruiters (demonstrating full-stack ML engineering skills)

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit Dashboard                     │
│  (Charts, Predictions, Backtest Results, Signal Alerts)     │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                     FastAPI Backend                         │
│  /predict, /backtest, /historical, /signals, /health        │
└─────────────────────────────┬───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Data Ingestion│    │ ML Pipeline   │    │ Backtest     │
│ (CCXT)        │    │ (TensorFlow)  │    │ Engine       │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  SQLite DB      │
                    │  (historical)   │
                    └─────────────────┘
```

---

## 3. Tech Stack

- **Language:** Python 3.10+
- **Data:** CCXT (crypto data), yfinance (stocks)
- **ML:** TensorFlow/Keras (LSTM), scikit-learn
- **Backend:** FastAPI
- **Dashboard:** Streamlit
- **Storage:** SQLite
- **Container:** Docker

---

## 4. Features

### 4.1 Data Ingestion
- Fetch real-time OHLCV data from Binance (crypto) / Yahoo Finance (stocks)
- Support multiple symbols: BTC, ETH, SOL, AAPL, TSLA
- Automatic data storage in SQLite
- Scheduled data updates

### 4.2 ML Prediction Model
- LSTM neural network for time-series prediction
- Features: OHLCV + technical indicators (RSI, MACD, SMA)
- 24-hour price prediction horizon
- Model versioning and persistence

### 4.3 Backtesting Engine
- Strategy: Moving average crossover + RSI signals
- Metrics: Sharpe ratio, max drawdown, win rate, total return
- Visual equity curve

### 4.4 API Endpoints
- `GET /predict/{symbol}` - Get price prediction
- `GET /historical/{symbol}` - Get historical data
- `GET /signals/{symbol}` - Get buy/sell signals
- `POST /backtest` - Run backtest
- `GET /health` - Health check

### 4.5 Dashboard
- Real-time price charts with predictions
- Technical indicators visualization
- Backtest results with metrics
- Signal alerts panel

---

## 5. Data Schema

### Price Data (SQLite)
```sql
CREATE TABLE price_data (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    open REAL, high REAL, low REAL, close REAL, volume REAL,
    UNIQUE(symbol, timestamp)
);
```

### Predictions
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    predicted_price REAL,
    actual_price REAL,
    model_version TEXT
);
```

---

## 6. Acceptance Criteria

- [ ] Docker container runs successfully
- [ ] FastAPI returns predictions for BTC/ETH
- [ ] Streamlit dashboard displays charts and signals
- [ ] Backtest engine produces metrics
- [ ] Project has README with setup instructions
- [ ] Code has inline documentation
- [ ] Unit tests cover core functions

---

## 7. File Structure

```
/personalProject/
├── SPEC.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py           # Settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── lstm_model.py   # ML model
│   │   └── trainer.py      # Training logic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py # CCXT/YFinance
│   │   ├── database.py     # SQLite
│   │   ├── predictor.py    # Prediction service
│   │   └── backtest.py     # Backtest engine
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predictions.py
│   │   └── backtest.py
│   └── schemas/
│       ├── __init__.py
│       └── prediction.py
├── dashboard/
│   ├── __init__.py
│   └── app.py              # Streamlit
├── tests/
│   ├── __init__.py
│   ├── test_predictor.py
│   └── test_backtest.py
└── notebooks/
    └── model_training.ipynb
```