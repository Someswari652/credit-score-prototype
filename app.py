import streamlit as st
import yfinance as yf
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

st.title("📊 Credit Score Prototype")

# Step 1: Choose company
companies = {"Infosys": "INFY.NS", "Reliance": "RELIANCE.NS"}
company = st.selectbox("Choose a company", list(companies.keys()))
ticker = companies[company]

# Step 2: Get stock data (last 1 month)
data = yf.Ticker(ticker).history(period="1mo")
first = data["Close"].iloc[0]
last = data["Close"].iloc[-1]
price_change = (last - first) / first  # % change

# Step 3: Get news headlines + sentiment
feed = feedparser.parse(f"https://news.google.com/rss/search?q={company}")
analyzer = SentimentIntensityAnalyzer()
sentiments = []
for entry in feed.entries[:5]:
    score = analyzer.polarity_scores(entry.title)["compound"]
    sentiments.append(score)
avg_sentiment = float(np.mean(sentiments)) if sentiments else 0.0

# Step 4: Simple scoring rules
score = 70
if price_change > 0: score += 10
else: score -= 10
if avg_sentiment > 0: score += 10
else: score -= 10
score = max(0, min(100, score))  # keep score between 0 and 100

# Step 5: Show results
st.metric("Credit Score (0–100)", f"{score}")
st.line_chart(data["Close"])
st.subheader("📰 Recent News")
for entry in feed.entries[:5]:
    st.write("-", entry.title)