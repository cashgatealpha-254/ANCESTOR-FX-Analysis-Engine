from fastapi import FastAPI
from engine.analyze import run_analysis
from engine.logger import save_analysis
from memory.history import load_history, get_symbol_history, append_analysis, get_recent_history, average_confidence

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
    print(f"Received request to analyze {symbol}")
    return run_analysis(symbol)

@app.get("/history/{symbol}")
def history(symbol: str):
    history = get_symbol_history(symbol)
    return {
        "symbol": symbol.upper(),
        "history": history
    }

@app.get("/recent_history")
def recent_history(n: int = 10):
    history = get_recent_history(n)
    return {
        "recent_history": history
    }

@app.get("/average_confidence/{symbol}")
def average_confidence_endpoint(symbol: str):
    avg_confidence = average_confidence(symbol)
    return {
        "symbol": symbol.upper(),
        "average_confidence": avg_confidence
    }
