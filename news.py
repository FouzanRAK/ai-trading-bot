import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# 🔥 SAFE FIX: auto-download lexicon if missing
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def fake_news_sentiment(ticker):
    try:
        url = f"https://news.google.com/rss/search?q={ticker}+stock"
        text = requests.get(url).text

        chunks = text.split("<title>")[1:6]

        scores = []
        for c in chunks:
            scores.append(sia.polarity_scores(c)["compound"])

        return sum(scores) / len(scores) if scores else 0

    except:
        return 0
