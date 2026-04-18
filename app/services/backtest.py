import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class BacktestEngine:
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["sma_20"] = df["close"].rolling(window=20).mean()
        df["sma_50"] = df["close"].rolling(window=50).mean()
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.calculate_indicators(df)
        df["signal"] = 0
        
        df.loc[(df["sma_20"] > df["sma_50"]) & (df["rsi"] < 70), "signal"] = 1
        df.loc[(df["sma_20"] < df["sma_50"]) | (df["rsi"] > 80), "signal"] = -1
        
        return df

    def run(self, df: pd.DataFrame, initial_capital: Optional[float] = None) -> Dict:
        capital = initial_capital or self.initial_capital
        df = self.generate_signals(df)
        
        position = 0
        cash = capital
        trades = []
        equity = [capital]
        
        for i in range(1, len(df)):
            price = df.iloc[i]["close"]
            signal = df.iloc[i]["signal"]
            
            if signal == 1 and position == 0:
                position = cash / price
                cash = 0
                trades.append({"type": "BUY", "price": price, "index": i})
            elif signal == -1 and position > 0:
                cash = position * price
                trades.append({"type": "SELL", "price": price, "index": i})
                position = 0
            
            portfolio_value = cash + position * price
            equity.append(portfolio_value)
        
        final_value = cash + position * df.iloc[-1]["close"]
        returns = (final_value - capital) / capital * 100
        
        equity_series = pd.Series(equity)
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        wins = [t for t in trades if t["type"] == "SELL"]
        win_count = 0
        for i in range(0, len(wins) - 1, 2):
            if i + 1 < len(trades):
                buy_price = wins[i]["price"]
                sell_price = wins[i + 1]["price"] if i + 1 < len(wins) else final_value
                if sell_price > buy_price:
                    win_count += 1
        
        total_trades = len([t for t in trades if t["type"] == "BUY"])
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
        
        returns_arr = np.diff(equity) / equity[:-1]
        returns_arr = returns_arr[~np.isnan(returns_arr)]
        sharpe = (returns_arr.mean() / returns_arr.std() * np.sqrt(252)) if len(returns_arr) > 0 and returns_arr.std() > 0 else 0
        
        return {
            "initial_capital": capital,
            "final_value": round(final_value, 2),
            "total_return": round(returns, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe, 2),
            "total_trades": total_trades,
            "win_rate": round(win_rate, 2),
            "equity_curve": equity,
            "trades": trades
        }

engine = BacktestEngine()