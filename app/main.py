from fastapi import FastAPI
from app.routes import predictions

app = FastAPI(title="TradePredict AI", version="1.0.0")
app.include_router(predictions.router, prefix="/api", tags=["predictions"])

@app.get("/")
def root():
    return {"message": "TradePredict AI API", "docs": "/docs"}