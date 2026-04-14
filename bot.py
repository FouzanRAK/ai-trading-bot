import yfinance as yf
import pandas as pd
from xgboost import XGBClassifier
from news import fake_news_sentiment

TICKERS = ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA"]

MODELS = {}

# ---------------- DATA ----------------
def get_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    df.dropna(inplace=True)
    return df

# ---------------- FEATURES ----------------
def create_features(df):
    df = df.copy()

    df["return"] = df["Close"].pct_change()
    df["ma5"] = df["Close"].rolling(5).mean()
    df["ma20"] = df["Close"].rolling(20).mean()
    df["volatility"] = df["return"].rolling(10).std()

    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    df.dropna(inplace=True)
    return df

# ---------------- MODEL ----------------
def train_model(df):
    features = ["return", "ma5", "ma20", "volatility"]

    model = XGBClassifier(
        n_estimators=60,
        max_depth=3,
        learning_rate=0.1,
        eval_metric="logloss"
    )

    model.fit(df[features], df["target"])
    return model

def get_model(ticker, df):
    if ticker in MODELS:
        return MODELS[ticker]

    model = train_model(df)
    MODELS[ticker] = model
    return model

# ---------------- ANALYSIS ----------------
def analyze(ticker):
    df = create_features(get_data(ticker))

    model = get_model(ticker, df)

    latest = df.iloc[-1][["return","ma5","ma20","volatility"]].values.reshape(1,-1)

    prob = model.predict_proba(latest)[0][1]

    sentiment = fake_news_sentiment(ticker)

    # combine ML + news
    final_score = (prob * 0.7) + ((sentiment + 1) / 2 * 0.3)

    return {
        "ticker": ticker,
        "price": float(df["Close"].iloc[-1]),
        "prob": float(prob),
        "sentiment": float(sentiment),
        "score": float(final_score),
        "df": df.tail(60)
    }

def scan_market():
    return sorted([analyze(t) for t in TICKERS], key=lambda x: x["score"], reverse=True)