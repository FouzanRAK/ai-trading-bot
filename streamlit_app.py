import streamlit as st
import plotly.graph_objects as go
from bot import scan_market

st.set_page_config(page_title="NeoTrade Terminal", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
body {
    background-color: #0b0f19;
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
    box-shadow: 0 0 15px rgba(0,255,213,0.1);
}
</style>
""", unsafe_allow_html=True)

st.title("📊 NeoTrade AI Terminal")

run = st.button("🚀 Run Scan")

# ---------------- MAIN ----------------
if run:

    data = scan_market()   # ✅ ALWAYS A LIST

    # safety check
    if not data:
        st.error("No data returned from scan_market()")
        st.stop()

    top = data[0]  # ✅ FIXED

    # ---------------- TOP METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.metric("🏆 Top Stock", top["ticker"])
    col2.metric("💰 Price", f"${top['price']:.2f}")
    col3.metric("🧠 Score", f"{top['score']:.2%}")

    st.divider()

    # ---------------- STOCK LIST ----------------
    for item in data:

        st.markdown(f"""
        <div class="card">
            <h3>{item['ticker']}</h3>
            <p>💰 Price: ${item['price']:.2f}</p>
            <p>📊 Score: {item['score']:.2%}</p>
        </div>
        """, unsafe_allow_html=True)

        df = item["df"]

        # ---------------- CANDLESTICK ----------------
        fig = go.Figure(data=[go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])

        fig.update_layout(
            paper_bgcolor="#0b0f19",
            plot_bgcolor="#0b0f19",
            font=dict(color="#00ffd5"),
            height=300,
            margin=dict(l=10, r=10, t=30, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)
