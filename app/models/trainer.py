import numpy as np
import pandas as pd
from typing import Optional, Tuple
from datetime import datetime
from app.models.lstm_model import MLPPredictor
from app.config import Config


class ModelTrainer:
    def __init__(self, model_path: str = None):
        self.predictor = MLPPredictor(model_path)
        self.trained = False

    def train(self, df: pd.DataFrame, epochs: int = 100) -> dict:
        if len(df) < 100:
            return {"success": False, "error": "Insufficient data for training (need at least 100 rows)"}
        
        try:
            success = self.predictor.train(df, epochs=epochs)
            if success:
                self.trained = True
                return {
                    "success": True,
                    "message": "Model trained successfully",
                    "data_points": len(df),
                    "epochs": epochs
                }
            else:
                return {"success": False, "error": "Training failed - insufficient data"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def train_on_symbol(self, symbol: str) -> dict:
        from app.services.data_fetcher import fetcher
        df = fetcher.fetch_all(symbol)
        if df.empty:
            return {"success": False, "error": f"Could not fetch data for {symbol}"}
        return self.train(df)

    def predict(self, df: pd.DataFrame) -> Optional[float]:
        if not self.trained:
            try:
                pred = self.predictor.predict(df)
                return pred
            except:
                return None
        return self.predictor.predict(df)

    def evaluate(self, df: pd.DataFrame, predictions: np.ndarray, actuals: np.ndarray) -> dict:
        mse = np.mean((predictions - actuals) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(predictions - actuals))
        mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
        
        return {
            "mse": float(mse),
            "rmse": float(rmse),
            "mae": float(mae),
            "mape": float(mape)
        }


trainer = ModelTrainer()