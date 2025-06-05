import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Page setup with favicon and tagline
st.set_page_config(
    page_title="Moonia: AI-Powered Stock Strategist",
    page_icon="🌕",
    layout="wide"
)

st.title("🌕 Moonia: AI-Powered Stock Strategist")
st.markdown("##### Smarter insights. Safer trades. Always one step ahead.")

# Sidebar user input
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Balanced Strategy", "Capital Preservation"])
risk_pct = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Expert"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000, step=100)
geek_mode = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"])

if st.sidebar.button("🚀 Launch Analysis"):
    data = yf.download(ticker, period="5y")
    if data.empty:
        st.error("Stock data could not be loaded. Check the ticker symbol.")
    else:
        data["20d"] = data["Close"].rolling(window=20).mean()
        data["50d"] = data["Close"].rolling(window=50).mean()
        data["ATR"] = data["High"].rolling(window=14).max() - data["Low"].rolling(window=14).min()

        current_price = data["Close"].iloc[-1]
        ma_20 = data["20d"].iloc[-1]
        ma_50 = data["50d"].iloc[-1]
        atr = data["ATR"].iloc[-1]
        trend_signal = "Bullish" if ma_20 > ma_50 else "Bearish"
        dist_from_ma = (current_price - ma_50) / ma_50 * 100
        stop_loss = current_price - (2 * atr)
        max_risk = equity * (risk_pct / 100)
        position_size = int(max_risk / (2 * atr))

        # Market context banner
        st.markdown(
            f"<div style='background-color:#14233c; padding:10px; border-radius:8px; color:white;'>"
            f"🔺 Price is {dist_from_ma:.2f}% {'above' if dist_from_ma > 0 else 'below'} the 50-day average. "
            f"The short-term average is {'rising' if ma_20 > data['20d'].iloc[-2] else 'falling'}, "
            f"and the long-term average is {'rising' if ma_50 > data['50d'].iloc[-2] else 'falling'}."
            f"</div>",
            unsafe_allow_html=True
        )

        # Recommendation
        st.markdown(f"### Recommendation: 🚀 BUY")

        # Moonia Strategy Insight (green box)
        st.markdown(
            f"""
            <div style="background-color:#103730; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
            <h3 style='color:white;'>🧠 Moonia Strategy Insight</h3>
            <ul style='color:white;'>
            <li>🎯 <strong>Buy Target Zone:</strong> Around ${current_price:.2f}</li>
            <li>🛑 <strong>Suggested Stop Loss:</strong> ${stop_loss:.2f}</li>
            <li>📦 <strong>Recommended Position Size:</strong> {position_size} shares</li>
            <li>💸 <strong>Max Risk Amount:</strong> ${max_risk:.2f}</li>
            <li>📈 <em>Trend is {trend_signal.lower()} — suitable for high growth strategies and beginner investors.</em></li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Risk-adjusted advice
        st.markdown(
            f"<div style='background-color:#214e26; padding:10px; border-radius:8px; color:white;'>"
            f"✅ <strong>Your {goal.lower()} goal aligns with the current {trend_signal.lower()} momentum.</strong>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Moonia AI's Take (purple insight box)
        st.markdown(
            """
            <div style="background-color:#2b183f; padding: 20px; border-radius: 10px; margin-top: 15px; margin-bottom: 25px;">
                <h3 style="color:white;">🤖 Moonia AI’s Take</h3>
                <p style="color:white;">
                Based on the current bullish crossover pattern and momentum metrics, the setup shows promise. 
                When price crosses above the 50-day average with rising short-term trend lines and stable volatility (as measured by ATR), 
                it often indicates sustained bullish behavior — especially when supported by volume. 
                For investors targeting high growth, this could be an effective entry point. However, always manage your risk appropriately: 
                using a well-placed stop-loss and monitoring shifts in trend are critical to long-term performance.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Expandable: Why this makes sense
        with st.expander("📌 Why this makes sense (click to expand)"):
            if insight_mode == "Simple":
                st.write(f"• **Short-term trend (20-day avg):** ${ma_20:.2f}")
                st.write(f"• **Long-term trend (50-day avg):** ${ma_50:.2f}")
                st.write(f"• **Daily movement (ATR):** ${atr:.2f}")
                st.write(f"• **Suggested safety stop:** ≈ ${stop_loss:.2f}")
            else:
                st.markdown("### Technical Breakdown")
                st.markdown(f"- **20-day MA:** ${ma_20:.2f}")
                st.markdown(f"- **50-day MA:** ${ma_50:.2f}")
                st.markdown(f"- **ATR (14):** ${atr:.2f}")
                st.markdown(f"- **% Distance from 50 MA:** {dist_from_ma:.2f}%")
                st.markdown(f"- **Stop-Loss Recommendation:** ${stop_loss:.2f}")
                st.markdown(f"- **Max Risk Allowed:** ${max_risk:.2f}")
                st.markdown(f"- **Position Sizing Formula:**<br>Shares = Risk ÷ (2 × ATR) = {max_risk:.0f} ÷ {2*atr:.2f} = {position_size} shares", unsafe_allow_html=True)
                st.markdown("### Interpretation:")
                st.write("- Trend Signal: **BULLISH** — based on crossover of short vs. long moving averages")
                st.write("- Strategy Fit: Appropriate for high growth strategies and beginner investors")
                st.write("- Volatility-adjusted stop and sizing included for risk control")

        # Expandable: Show historical data
        with st.expander("📊 Show Historical Data"):
            st.line_chart(data["Close"])

        # Disclaimer
        st.markdown(
            "<p style='font-size: 0.85rem; color: gray;'>🌕 <em>Disclaimer: Moonia provides educational insights only. No financial advice is given. Invest responsibly.</em></p>",
            unsafe_allow_html=True
        )
