from fastapi import FastAPI
from engine.analyze import run_analysis
from engine.logger import save_analysis
from memory.history import save_history, load_history, get_recent_history, get_symbol_history, average_confidence

app = FastAPI(title="Market Analysis Engine")


@app.get("/")
def home():
    return {
        "status": "running",
        "engine": "Market Analysis Engine",
        "pairs": [
            "GBPUSD",
            "XAUUSD",
            "EURUSD",
            "USDJPY",
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/analysis/{symbol}")
def analyze(symbol: str):
    result = run_analysis(symbol)
    save_analysis(symbol, result)
    return result

@app.get("/history")
def history(n: int = 10):
    return get_recent_history(n)