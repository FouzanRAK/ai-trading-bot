import requests
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

# simple free news source (no API key needed)
def get_news(ticker):
    url = f"https://news.google.com/rss/search?q={ticker}+stock"
    return requests.get(url).text

def sentiment_score(text):
    return sia.polarity_scores(text)["compound"]

def fake_news_sentiment(ticker):
    """
    NOTE: RSS parsing kept simple for stability.
    In real apps you'd parse XML properly.
    """
    news = get_news(ticker)

    # crude chunking (works for demo)
    chunks = news.split("<title>")[1:6]

    scores = []
    for c in chunks:
        scores.append(sentiment_score(c))

    if not scores:
        return 0

    return sum(scores) / len(scores)