import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor
import joblib
import os
from typing import Optional
from app.config import Config

class MLPPredictor:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or str(Config.MODEL_PATH / "mlp_model.pkl")
        self.scaler = MinMaxScaler()
        self.sequence_length = 60
        self.model = None

    def add_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        close = df["close"].values

        delta = np.diff(close, prepend=close[0])
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = np.zeros_like(close)
        avg_loss = np.zeros_like(close)
        for i in range(14, len(close)):
            avg_gain[i] = np.mean(gain[i-14:i+1])
            avg_loss[i] = np.mean(loss[i-14:i+1])
        rs = avg_gain / (avg_loss + 1e-10)
        df["rsi"] = 100 - (100 / (1 + rs))

        ema12 = np.zeros_like(close)
        ema26 = np.zeros_like(close)
        ema12[0] = close[0]
        ema26[0] = close[0]
        for i in range(1, len(close)):
            ema12[i] = 0.1538 * close[i] + 0.8462 * ema12[i-1]
            ema26[i] = 0.0379 * close[i] + 0.9621 * ema26[i-1]
        macd_line = ema12 - ema26
        df["macd"] = macd_line

        df["sma_20"] = df["close"].rolling(window=20).mean()
        df["sma_50"] = df["close"].rolling(window=50).mean()

        sma20 = df["close"].rolling(window=20).mean()
        std20 = df["close"].rolling(window=20).std()
        df["bb_upper"] = sma20 + 2 * std20
        df["bb_middle"] = sma20
        df["bb_lower"] = sma20 - 2 * std20

        high = df["high"].values
        low = df["low"].values
        close_pr = df["close"].values
        tr = np.maximum(high - low, np.maximum(np.abs(high - np.roll(close_pr, 1)), np.abs(low - np.roll(close_pr, 1))))
        tr[0] = high[0] - low[0]
        atr = np.zeros_like(tr)
        atr[0] = tr[0]
        for i in range(1, len(tr)):
            atr[i] = (atr[i-1] * 13 + tr[i]) / 14
        df["atr"] = atr

        df = df.fillna(0)
        return df

    def create_features(self, df: pd.DataFrame):
        df = self.add_indicators(df)
        features = ["open", "high", "low", "close", "volume", "rsi", "macd", "sma_20", "sma_50", "bb_upper", "bb_lower", "atr"]
        
        feature_data = df[features].values
        scaled_data = self.scaler.fit_transform(feature_data)
        
        X = []
        y = []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i - self.sequence_length:i].flatten())
            y.append(scaled_data[i, 3])
        
        return np.array(X), np.array(y), df

    def train(self, df: pd.DataFrame, epochs: int = 100):
        X, y, _ = self.create_features(df)
        if len(X) < 100:
            return False
        
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.model.fit(X, y)
        
        joblib.dump({"model": self.model, "scaler": self.scaler}, self.model_path)
        return True

    def predict(self, df: pd.DataFrame) -> Optional[float]:
        if not os.path.exists(self.model_path):
            return None
        
        try:
            data = joblib.load(self.model_path)
            self.model = data["model"]
            self.scaler = data["scaler"]
            
            df = self.add_indicators(df)
            features = ["open", "high", "low", "close", "volume", "rsi", "macd", "sma_20", "sma_50", "bb_upper", "bb_lower", "atr"]
            last_n = df[features].values[-self.sequence_length:]
            scaled = self.scaler.transform(last_n)
            X = scaled.flatten().reshape(1, -1)
            pred = self.model.predict(X)[0]
            
            dummy = np.zeros((1, len(features)))
            dummy[0, 3] = pred
            return self.scaler.inverse_transform(dummy)[0, 3]
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

predictor = MLPPredictor()