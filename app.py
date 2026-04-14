import streamlit as st
import plotly.graph_objects as go
import time
from bot import scan_market

# ---------------- CONFIG ----------------
st.set_page_config(page_title="NeoTrade Terminal X", layout="wide")

# ---------------- FLASH UI ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #05070d, #0b0f19);
}

h1 {
    color: #00ffd5;
    text-align: center;
    font-size: 42px;
}

.card {
    background: linear-gradient(135deg, #111827, #0f172a);
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 25px rgba(0,255,213,0.15);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 NeoTrade Terminal X")

run = st.button("🚀 Run Live Scan")

auto = st.checkbox("⚡ Live Mode (5s)")

# ---------------- CANDLE CHART ----------------
def candle_chart(df, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )])

    fig.update_layout(
        title=f"{ticker} Candlestick Chart",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        font=dict(color="#00ffd5")
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- MAIN ----------------
if run or auto:

    data = scan_market()

    top = data[0]

    # TOP METRICS
    col1, col2, col3 = st.columns(3)

    col1.metric("🏆 Top Stock", top["ticker"])
    col2.metric("💰 Price", f"${top['price']:.2f}")
    col3.metric("🧠 Score", f"{top['score']:.2f}")

    st.divider()

    # ---------------- LIST ----------------
    for item in data:

        st.markdown(f"""
        <div class="card">
            <h3>{item['ticker']}</h3>
            <p>Price: ${item['price']:.2f}</p>
            <p>ML Probability: {item['prob']:.2%}</p>
            <p>News Sentiment: {item['sentiment']:.2f}</p>
            <p><b>Final Score: {item['score']:.2f}</b></p>
        </div>
        """, unsafe_allow_html=True)

        candle_chart(item["df"], item["ticker"])

    if auto:
        time.sleep(5)
        st.rerun()