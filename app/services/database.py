from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
from app.config import Config

Base = declarative_base()

class PriceData(Base):
    __tablename__ = "price_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    __table_args__ = (UniqueConstraint("symbol", "timestamp", name="uix_symbol_timestamp"),)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    predicted_price = Column(Float, nullable=False)
    actual_price = Column(Float, nullable=True)
    model_version = Column(String, default="v1")

engine = create_engine(Config.DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_price_data(df: pd.DataFrame):
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            existing = db.query(PriceData).filter(
                PriceData.symbol == row["symbol"],
                PriceData.timestamp == row["timestamp"]
            ).first()
            if not existing:
                price_data = PriceData(
                    symbol=row["symbol"],
                    timestamp=row["timestamp"],
                    open=row["open"],
                    high=row["high"],
                    low=row["low"],
                    close=row["close"],
                    volume=row["volume"]
                )
                db.add(price_data)
        db.commit()
    finally:
        db.close()

def get_price_data(symbol: str, limit: int = 365) -> pd.DataFrame:
    db = SessionLocal()
    try:
        data = db.query(PriceData).filter(
            PriceData.symbol == symbol
        ).order_by(PriceData.timestamp.desc()).limit(limit).all()
        df = pd.DataFrame([{
            "timestamp": d.timestamp,
            "open": d.open,
            "high": d.high,
            "low": d.low,
            "close": d.close,
            "volume": d.volume,
            "symbol": d.symbol
        } for d in data])
        return df.sort_values("timestamp")
    finally:
        db.close()

def save_prediction(symbol: str, predicted_price: float, actual_price: float = None):
    db = SessionLocal()
    try:
        pred = Prediction(symbol=symbol, predicted_price=predicted_price, actual_price=actual_price)
        db.add(pred)
        db.commit()
    finally:
        db.close()