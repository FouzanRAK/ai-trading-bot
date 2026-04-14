import yfinance as yf
import pandas as pd
from xgboost import XGBClassifier

TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA"]

MODELS = {}

def get_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")

    if df is None or df.empty:
        raise Exception(f"No data for {ticker}")

    return df.reset_index()

def create_features(df):
    df = df.copy()

    df["return"] = df["Close"].pct_change()
    df["ma5"] = df["Close"].rolling(5).mean()
    df["ma20"] = df["Close"].rolling(20).mean()
    df["volatility"] = df["return"].rolling(10).std()

    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    df = df.dropna()
    return df

def train_model(df):
    features = ["return", "ma5", "ma20", "volatility"]

    model = XGBClassifier(
        n_estimators=40,
        max_depth=3,
        learning_rate=0.1,
        eval_metric="logloss"
    )

    model.fit(df[features], df["target"])
    return model

def analyze(ticker):
    df = get_data(ticker)
    df = create_features(df)

    model = train_model(df)

    latest = df.iloc[-1][["return","ma5","ma20","volatility"]].values.reshape(1, -1)
    prob = model.predict_proba(latest)[0][1]

    return {
        "ticker": ticker,
        "price": float(df["Close"].iloc[-1]),
        "score": float(prob),
        "df": df.tail(60)
    }

def scan_market():
    results = []

    for t in TICKERS:
        try:
            results.append(analyze(t))
        except Exception as e:
            print(f"{t} failed: {e}")

    if len(results) == 0:
        raise Exception("ALL DATA FAILED — yfinance blocked or no internet")

    return sorted(results, key=lambda x: x["score"], reverse=True)
