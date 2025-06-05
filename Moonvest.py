import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Moonvest - Smart Stock Analyzer", layout="wide")
st.title("🌕 Moonvest: Smart Stock Analyzer")

# 📄 Mission Statement / Overview
st.markdown("""
Moonvest is an intelligent stock analysis engine designed to empower modern investors with data-driven insights and strategic clarity.  

Using real-time market data and quantitative trend analysis, Moonvest delivers actionable BUY, HOLD, or SELL recommendations—instantly and intuitively.  
Whether you're managing a personal portfolio or exploring new investment opportunities, Moonvest helps you make confident, informed decisions without the noise.

🚀 Backed by logic.  
📈 Built for clarity.  
🌕 Designed to guide your investments to the moon.
""")

# 🌍 Mission + Differentiators
st.markdown("---")

st.markdown("### 🌍 Our Mission")
st.markdown("""
At Moonvest, our mission is to democratize financial strategy.  
We believe that anyone — from first-time investors to experienced traders — deserves access to powerful, transparent, and intuitive tools that drive confident decision-making.

Our platform transforms complex data into clear, human-readable insights so you can stop guessing and start growing.
""")

st.markdown("""> Moonvest isn't just a tool — it's your personal strategy engine.""")

# 🧾 Sidebar Inputs
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Capital Preservation", "Balanced Strategy"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000)

# 🔍 Launch Analysis
if st.sidebar.button("🚀 Launch Analysis"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5y")

        st.subheader(f"📈 {ticker.upper()} - 5 Year Performance")

        # 📊 Interactive Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            name="Close Price"
        ))
        fig.update_layout(
            title=f"{ticker.upper()} - Historical Price Chart",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # 📐 Moving Averages
        ma_short = hist["Close"].rolling(window=20).mean()
        ma_long = hist["Close"].rolling(window=50).mean()

        # 📌 Signal Logic
        if ma_short.iloc[-1] < ma_long.iloc[-1]:
            signal = "🔻 SELL"
            explanation = "Short-term momentum has declined below the long-term trend. Risk is elevated."
        elif ma_short.iloc[-1] > ma_long.iloc[-1]:
            signal = "🚀 BUY"
            explanation = "The 20-day trend is above the 50-day trend, indicating strong upward momentum."
        else:
            signal = "⏸ HOLD"
            explanation = "The market lacks a clear direction. A cautious hold is advised."

        st.markdown(f"### Recommendation: {signal}")
        with st.expander("📌 Moonvest Insight"):
            st.markdown(explanation)

        with st.expander("🧾 Show Historical Data"):
            st.dataframe(hist.tail(30))

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
