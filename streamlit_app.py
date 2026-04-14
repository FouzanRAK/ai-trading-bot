import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from bot import scan_market

st.set_page_config(page_title="NeoTrade Terminal", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
body {
    background: #0b0f19;
    color: white;
}
h1 {
    color: #00ffd5;
    text-align: center;
}
.card {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 NeoTrade AI Terminal")

run = st.button("🚀 Run Scan")

if run:

    df = scan_market()

    top = df[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Top Stock", top["ticker"])
    col2.metric("Price", f"${top['price']:.2f}")
    col3.metric("Score", f"{top['score']:.2f}")

    st.divider()

    # LIST
    for item in df:

        st.markdown(f"""
        <div class="card">
        <h3>{item['ticker']}</h3>
        <p>Price: ${item['price']:.2f}</p>
        <p>Signal Score: {item['score']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        # Candlestick
        fig = go.Figure(data=[go.Candlestick(
            x=item["df"]["Date"],
            open=item["df"]["Open"],
            high=item["df"]["High"],
            low=item["df"]["Low"],
            close=item["df"]["Close"]
        )])

        fig.update_layout(
            paper_bgcolor="#0b0f19",
            plot_bgcolor="#0b0f19",
            font=dict(color="#00ffd5"),
            height=300,
            margin=dict(l=10,r=10,t=30,b=10)
        )

        st.plotly_chart(fig, use_container_width=True)
