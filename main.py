from fastapi import FastAPI
from engine.analyze import run_analysis

app = FastAPI(title="Market Analysis Engine")


@app.get("/")
def home():
    return {
        "status": "running",
        "engine": "Market Analysis Engine",
        "pairs": [
            "GBPUSD",
            "XAUUSD"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/analysis/{symbol}")
def analyze(symbol: str):
    return run_analysis(symbol)