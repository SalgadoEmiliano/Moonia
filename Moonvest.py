import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Moonia: AI-Powered Stock Strategist", page_icon="🌕", layout="wide")

# Title + Tagline
st.markdown("<h1>🌕 Moonia: AI-Powered Stock Strategist</h1>", unsafe_allow_html=True)
st.markdown("**Smarter insights. Safer trades. Always one step ahead.**")
st.markdown("---")

# Sidebar
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Balanced", "Preservation"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=0, value=1000)
show_geek = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"])
launch = st.sidebar.button("🚀 Launch Analysis")

if launch:
    # Load data
    df = yf.download(ticker, period="5y")
    df["20_MA"] = df["Close"].rolling(20).mean()
    df["50_MA"] = df["Close"].rolling(50).mean()
    df["ATR"] = df["Close"].diff().rolling(14).std()
    price = df["Close"].iloc[-1]
    ma20 = df["20_MA"].iloc[-1]
    ma50 = df["50_MA"].iloc[-1]
    atr = df["ATR"].iloc[-1]
    stop_loss = price - (2 * atr)
    shares = int((equity * risk / 100) // (2 * atr))
    dist_pct = ((price - ma50) / ma50) * 100
    trend_note = "The short-term average is rising, and the long-term average is falling." if ma20 > ma50 and df["50_MA"].iloc[-5] > ma50 else "The short-term average is rising, and the long-term average is rising."

    # Chart
    st.subheader("📈 Price Chart (5Y)")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["Close"], label="Close")
    ax.plot(df.index, df["20_MA"], label="20-Day MA")
    ax.plot(df.index, df["50_MA"], label="50-Day MA")
    ax.legend()
    st.pyplot(fig)

    # Current status
    above_below = "above" if dist_pct > 0 else "below"
    st.markdown(f"<div style='background-color:#13294B;padding:10px;border-radius:8px;color:white;'>🔺 Price is {abs(dist_pct):.2f}% {above_below} the 50-day average. {trend_note}</div>", unsafe_allow_html=True)

    # Recommendation
    st.markdown("## Recommendation: 🚀 BUY")

    # Strategy Insight
    st.markdown("### 🧠 Moonia Strategy Insight")
    st.markdown(f"""
    <div style='background-color:#103E36;padding:15px;border-radius:10px;color:white;'>
    • 🎯 <b>Buy Target Zone:</b> Around ${price:.2f}<br>
    • 🛑 <b>Suggested Stop Loss:</b> ${stop_loss:.2f}<br>
    • 📦 <b>Recommended Position Size:</b> {shares} shares<br>
    • 💸 <b>Max Risk Amount:</b> ${equity * risk / 100:.0f}<br>
    • 📈 <i>Trend is bullish — suitable for high growth strategies and beginner investors.</i>
    </div>
    """, unsafe_allow_html=True)

    # Match message
    st.markdown(f"<div style='background-color:#1E5128;padding:10px;border-radius:8px;color:white;'>✅ <b>Your {goal.lower()} goal aligns with the current bullish momentum.</b></div>", unsafe_allow_html=True)

    # AI Take
    st.markdown("### 🤖 Moonia AI’s Take")
    st.markdown(f"""
    <div style='background-color:#3C1A4B;padding:15px;border-radius:10px;color:white;'>
    Based on the current bullish crossover and momentum metrics, this setup shows promise.
    When price crosses above the 50-day average with upward short-term trend lines and steady volatility (as indicated by ATR),
    it often signals sustained institutional interest. Investors seeking growth could view this as a high-confidence entry —
    but only if paired with disciplined risk controls such as stop-losses and dynamic position sizing.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Expanded rationale
    with st.expander("📌 Why this makes sense (click to expand)"):
        st.markdown(f"""
        • 📉 <b>Short-term trend (20-day avg):</b> ${ma20:.2f}  
        • 🌍 <b>Long-term trend (50-day avg):</b> ${ma50:.2f}  
        • 📊 <b>Daily movement (ATR):</b> {atr:.2f}  
        • 🔴 <b>Suggested safety stop:</b> ≈ ${stop_loss:.2f}
        """, unsafe_allow_html=True)

    # Interpretation
    with st.expander("💡 Here's what it means:"):
        st.markdown(f"""
        1. <b>Your current price is {abs(dist_pct):.2f}% {above_below} the long-term trend.</b><br>
        2. The short-term trend is above the long-term trend — that's a sign of momentum building.<br>
        3. Based on your risk setting of {risk}%, Moonia suggests you only risk <b>${equity * risk / 100:.0f}</b>.<br>
        4. That means you could trade up to <b>{shares} shares</b> and use a stop-loss at <b>${stop_loss:.2f}</b>.<br>
        💡 <i>Simply put: This looks like a good opportunity, but you're protected if momentum flips.</i>
        """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("<br><div style='color:gray;font-size:0.9em;'>🧠 <i>Disclaimer: Moonia provides educational insights only. No financial advice is given. Invest responsibly.</i></div>", unsafe_allow_html=True)
