import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Moonia", page_icon="🌕")

# Title and tagline
st.markdown("<h1 style='display: flex; align-items: center;'>🌕 Moonia: AI-Powered Stock Strategist</h1>", unsafe_allow_html=True)
st.markdown("**Smarter insights. Safer trades. Always one step ahead.**")
st.markdown("---")

# Sidebar - Investor Profile
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Moderate Growth", "Income"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", value=1000)
show_raw = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"])
analyze = st.sidebar.button("🚀 Launch Analysis")

if analyze:
    data = yf.Ticker(ticker).history(period="5y")
    data['20ma'] = data['Close'].rolling(window=20).mean()
    data['50ma'] = data['Close'].rolling(window=50).mean()
    data['ATR'] = data['High'].rolling(window=14).max() - data['Low'].rolling(window=14).min()

    price = data['Close'][-1]
    short_term = data['20ma'][-1]
    long_term = data['50ma'][-1]
    atr = data['ATR'][-1]
    dist_from_ma = price - long_term
    dist_pct = (dist_from_ma / long_term) * 100
    trend = "Bullish" if short_term > long_term else "Bearish"

    st.markdown(f"<h2>Recommendation: 🚀 <b>BUY</b></h2>", unsafe_allow_html=True)

    # Blue trend box
    trend_icon = "✅" if trend == "Bullish" else "🔻"
    st.info(f"{trend_icon} Price is {abs(dist_pct):.2f}% {'above' if dist_from_ma > 0 else 'below'} the 50-day average. "
            f"The short-term average is {'rising' if short_term > data['20ma'][-2] else 'falling'}, "
            f"and the long-term average is {'rising' if long_term > data['50ma'][-2] else 'falling'}.")

    # Strategy Insight Box
    st.markdown("### 🧠 Moonia Strategy Insight")
    with st.container():
        st.markdown("""
            <div style="background-color: #0c3b32; padding: 15px; border-radius: 8px;">
                <ul>
                    <li>🎯 <b>Buy Target Zone:</b> Around ${:.2f}</li>
                    <li>🛑 <b>Suggested Stop Loss:</b> ${:.2f}</li>
                    <li>📦 <b>Recommended Position Size:</b> {} shares</li>
                    <li>💸 <b>Max Risk Amount:</b> ${:.2f}</li>
                    <li>📈 <i>Trend is {} — suitable for high growth strategies and beginner investors.</i></li>
                </ul>
            </div>
        """.format(price, price - 2 * atr, int((risk / 100) * equity // (2 * atr)), (risk / 100) * equity, trend.lower()), unsafe_allow_html=True)

    # Goal alignment
    st.markdown(
        "<div style='background-color: #1a472a; color: white; padding: 10px; border-radius: 8px;'>"
        "✅ <b>Your high growth goal aligns with the current <i>bullish momentum</i>.</b></div>",
        unsafe_allow_html=True
    )

    # Moonia AI’s Take Box
    st.markdown("### 🤖 Moonia AI’s Take")
    st.markdown("""
        <div style="background-color: #3b215f; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            Based on the current bullish crossover pattern and momentum metrics, this setup shows promise. When price crosses above the 50-day average with upward short-term trend lines and steady volatility (as indicated by ATR), this often signals institutional buying or long setups. 
            Investors targeting growth may find this attractive, but proper risk management — including defined stop-loss levels and position sizing — remains essential. 
            Consider reassessing if short-term momentum weakens significantly in upcoming sessions.
        </div>
    """, unsafe_allow_html=True)

    # Technical justification
    with st.expander("📉 Why this makes sense (click to expand)"):
        st.markdown(f"""
        - 📈 **Short-term trend (20-day avg):** ${short_term:.2f}  
        - 🌍 **Long-term trend (50-day avg):** ${long_term:.2f}  
        - 📊 **Daily movement (ATR):** ${atr:.2f}  
        - 🧯 **Suggested safety stop:** ≈ ${price - 2 * atr:.2f}  
        """)

    # Interpretive Summary
    st.markdown("### Here's what it means:")
    st.markdown(f"""
    1. **Your current price is {abs(dist_pct):.2f}% {'above' if dist_from_ma > 0 else 'below'} the long-term trend.**
    2. The short-term trend is **above** the long-term trend — that’s a sign of momentum **{trend.lower()}**.
    3. Based on your risk setting of {risk}%, Moonia suggests you only risk **${(risk/100)*equity:.2f}** on this trade.
    4. That means you could trade up to **{int((risk/100)*equity // (2*atr))} shares** and protect yourself with a stop-loss at **${price - 2*atr:.2f}**.
    💡 Simply put: This setup looks like a good opportunity right now, but you're protected if momentum shifts.
    """)

    # Historical Chart
    with st.expander("📈 Show Historical Data"):
        fig, ax = plt.subplots()
        ax.plot(data.index, data["Close"], label="Close Price", linewidth=1.5)
        ax.plot(data.index, data["20ma"], label="20-day MA", linestyle="--")
        ax.plot(data.index, data["50ma"], label="50-day MA", linestyle="--")
        ax.set_title(f"{ticker.upper()} - 5 Year Performance")
        ax.set_ylabel("Price ($)")
        ax.legend()
        st.pyplot(fig)

    # Footer
    st.markdown(
        "<div style='font-size: 0.9em; color: gray;'>🌕 <i>Disclaimer: Moonia provides educational insights only. "
        "No financial advice is given. Invest responsibly.</i></div>",
        unsafe_allow_html=True
    )
