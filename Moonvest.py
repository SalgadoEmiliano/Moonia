import streamlit as st
import pandas as pd
import yfinance as yf

# App config
st.set_page_config(page_title="Moonia", page_icon="🌕", layout="wide")

# Header
st.markdown("<h1 style='font-size: 2.5em;'>🌕 Moonia: AI-Powered Stock Strategist</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #bbb;'>Smarter insights. Safer trades. Always one step ahead.</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar inputs
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Balanced Strategy", "Capital Preservation"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000, step=100)
geek_mode = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"])
clicked = st.sidebar.button("🚀 Launch Analysis")

# Logic
if clicked:
    stock = yf.Ticker(ticker)
    data = stock.history(period="5y")
    data["20d"] = data["Close"].rolling(window=20).mean()
    data["50d"] = data["Close"].rolling(window=50).mean()
    data["ATR"] = data["Close"].rolling(window=14).apply(lambda x: x.max() - x.min())

    price = data["Close"].iloc[-1]
    ma_20 = data["20d"].iloc[-1]
    ma_50 = data["50d"].iloc[-1]
    atr = data["ATR"].iloc[-1]
    dist_from_ma = ((price - ma_50) / ma_50) * 100
    stop_loss = round(price - 2 * atr, 2)
    max_risk = round((risk / 100) * equity, 2)
    position_size = int(max_risk // (2 * atr))

    trend_signal = "BUY" if ma_20 > ma_50 else "SELL" if ma_20 < ma_50 else "HOLD"
    trend_desc = "bullish" if trend_signal == "BUY" else "bearish" if trend_signal == "SELL" else "unclear"

    # MAIN RECOMMENDATION
    st.markdown(f"<h2>Recommendation: 🚀 {trend_signal}</h2>", unsafe_allow_html=True)

    # Percent difference box
    direction = "above" if dist_from_ma > 0 else "below"
    st.markdown(
        f"<div style='background-color:#14233c; padding:10px; border-radius:8px; color:white;'>"
        f"🔺 Price is {abs(dist_from_ma):.2f}% {direction} the 50-day average. "
        f"The short-term average is {'rising' if ma_20 > data['20d'].iloc[-2] else 'falling'}, "
        f"and the long-term average is {'rising' if ma_50 > data['50d'].iloc[-2] else 'falling'}."
        f"</div>",
        unsafe_allow_html=True
    )

    # Moonia Strategy Insight
    st.markdown("### 🧠 Moonia Strategy Insight")
    st.markdown(
        f"""
        <div style='background-color:#0f2f29; padding:15px; border-radius:10px; color:white;'>
        <ul>
        <li>🎯 <b>Buy Target Zone:</b> Around ${price:.2f}</li>
        <li>🛑 <b>Suggested Stop Loss:</b> ${stop_loss}</li>
        <li>📦 <b>Recommended Position Size:</b> {position_size} shares</li>
        <li>💸 <b>Max Risk Amount:</b> ${max_risk}</li>
        <li>📈 <i>Trend is {trend_desc} — suitable for {goal.lower()} and {experience.lower()} investors.</i></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Goal alignment box
    st.markdown(
        f"<div style='background-color:#1d3d1f; padding:10px; border-radius:8px; color:white; margin-top:10px;'>"
        f"✅ <b>Your {goal.lower()} goal aligns with the current {trend_desc} momentum.</b>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Moonia AI's Take
    st.markdown(
        f"""
        <div style='background-color:#2c1a3a; padding:15px; border-radius:10px; color:white; margin-top:16px;'>
        <h4>🤖 Moonia AI’s Take</h4>
        Based on the current {trend_desc} crossover and momentum metrics, this setup shows promise. 
        When price crosses above the 50-day average with upward short-term trend lines and steady volatility (as indicated by ATR), 
        this often signals institutional buying or long setups. 
        Investors targeting growth may find this attractive, but proper risk management — including defined stop-loss levels and position sizing — remains essential. 
        Consider reassessing if short-term momentum weakens significantly in upcoming sessions.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Geek Mode or Simple Mode Breakdown
    with st.expander("📉 Why this makes sense (click to expand)"):
        if insight_mode == "Advanced":
            st.markdown(
                f"""
                <h4>📊 Technical Breakdown</h4>
                • 20-day MA: ${ma_20:.2f}  
                • 50-day MA: ${ma_50:.2f}  
                • ATR (14): ${atr:.2f}  
                • % Distance from 50 MA: {dist_from_ma:.2f}%  
                • Stop-Loss Recommendation: ${stop_loss}  
                • Max Risk Allowed: ${max_risk}  
                • Position Sizing Formula:  
                <code>Shares = Risk ÷ (2 × ATR)</code> → {max_risk} ÷ {2 * atr:.2f} = <b>{position_size} shares</b>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <h4>📌 Interpretation:</h4>
                • Trend Signal: <b>{trend_signal}</b> — based on crossover of short vs. long moving averages  
                • Strategy Fit: Appropriate for <i>{goal.lower()} strategies</i> and <i>{experience.lower()} investors</i>  
                • Volatility-adjusted stop and sizing included for risk control  
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                • 📈 <b>Short-term trend (20-day avg):</b> ${ma_20:.2f}  
                • 🧭 <b>Long-term trend (50-day avg):</b> ${ma_50:.2f}  
                • 🌊 <b>Daily movement (ATR):</b> ${atr:.2f}  
                • 🛑 <b>Suggested safety stop:</b> ≈ ${stop_loss}  
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                ### Here's what it means:
                1. <b>Your current price is {abs(dist_from_ma):.2f}% {direction} the long-term trend.</b>  
                2. The short-term trend is {'above' if ma_20 > ma_50 else 'below'} the long-term trend — that’s a sign of momentum {trend_desc}.  
                3. Based on your risk setting of {risk}%, Moonia suggests you only risk <b>${max_risk}</b> on this trade.  
                4. That means you could trade up to <b>{position_size} shares</b> and protect yourself with a stop-loss at <b>${stop_loss}</b>.  
                💡 Simply put: This setup looks like a good opportunity right now, but you're protected if momentum shifts.
                """,
                unsafe_allow_html=True
            )

    with st.expander("📁 Show Historical Data"):
        st.dataframe(data.tail(60)[["Close", "20d", "50d", "ATR"]])

    st.markdown(
        "<p style='margin-top: 20px; font-size: 0.9em; color: gray;'>"
        "🌕 <i>Disclaimer: Moonia provides educational insights only. No financial advice is given. Invest responsibly.</i>"
        "</p>",
        unsafe_allow_html=True
    )
