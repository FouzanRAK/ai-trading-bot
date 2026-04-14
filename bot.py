import yfinance as yf
import pandas as pd
from xgboost import XGBClassifier

# ---------------- STOCKS ----------------
TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA"]

MODELS = {}

# ---------------- DOWNLOAD DATA ----------------
def get_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")

    if df is None or df.empty:
        raise Exception(f"No data for {ticker}")

    df = df.dropna()
    df = df.reset_index()

    return df

# ---------------- FEATURES ----------------
def create_features(df):
    df = df.copy()

    df["return"] = df["Close"].pct_change()
    df["ma5"] = df["Close"].rolling(5).mean()
    df["ma20"] = df["Close"].rolling(20).mean()
    df["volatility"] = df["return"].rolling(10).std()

    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    df = df.dropna()

    if len(df) < 30:
        raise Exception("Not enough data after feature engineering")

    return df

# ---------------- MODEL ----------------
def train_model(df):
    features = ["return", "ma5", "ma20", "volatility"]

    model = XGBClassifier(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1,
        eval_metric="logloss"
    )

    model.fit(df[features], df["target"])
    return model

# ---------------- GET MODEL ----------------
def get_model(ticker, df):
    if ticker in MODELS:
        return MODELS[ticker]

    model = train_model(df)
    MODELS[ticker] = model
    return model

# ---------------- ANALYZE ONE STOCK ----------------
def analyze(ticker):
    df = get_data(ticker)
    df = create_features(df)

    model = get_model(ticker, df)

    latest = df.iloc[-1][["return", "ma5", "ma20", "volatility"]].values.reshape(1, -1)

    prob = model.predict_proba(latest)[0][1]

    return {
        "ticker": ticker,
        "price": float(df["Close"].iloc[-1]),
        "score": float(prob),
        "df": df.tail(60)
    }

# ---------------- SCAN MARKET ----------------
def scan_market():
    results = []

    for t in TICKERS:
        try:
            results.append(analyze(t))
        except Exception as e:
            print(f"[ERROR] {t}: {e}")

    if len(results) == 0:
        raise Exception("ALL TICKERS FAILED — check internet or yfinance")

    return sorted(results, key=lambda x: x["score"], reverse=True)
