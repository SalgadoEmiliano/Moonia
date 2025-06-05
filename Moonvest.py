import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Moonvest - Smart Stock Analyzer", page_icon="🌕", layout="wide")
st.title("🌕 Moonvest: Smart Stock Analyzer")

# Sidebar Inputs
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Capital Preservation", "Balanced Strategy"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000)
geek_mode = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"], index=0)

# Launch
if st.sidebar.button("🚀 Launch Analysis"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        hist_full = stock.history(period="5y")

        st.subheader(f"📈 {ticker.upper()} - 5 Year Performance")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_full.index, y=hist_full["Close"], mode="lines", name="Close Price"))
        fig.update_layout(xaxis_title="Date", yaxis_title="Price ($)", template="plotly_dark", hovermode="x unified", height=500)
        st.plotly_chart(fig, use_container_width=True)

        close_price = hist["Close"].iloc[-1]
        ma_short = hist["Close"].rolling(window=20).mean()
        ma_long = hist["Close"].rolling(window=50).mean()
        short_ma_val = round(ma_short.iloc[-1], 2)
        long_ma_val = round(ma_long.iloc[-1], 2)
        atr = round((hist["High"] - hist["Low"]).rolling(window=14).mean().iloc[-1], 2)
        stop = round(close_price - 2 * atr, 2)
        percent_below_ma = round(((close_price - long_ma_val) / long_ma_val) * 100, 2)
        max_loss = round(equity * (risk / 100), 2)
        shares = int(max_loss / (2 * atr)) if atr > 0 else 0

        # Signal
        if short_ma_val > long_ma_val:
            signal = "🚀 BUY"
            trend = "Bullish"
            trend_expl = "The short-term trend is rising above the long-term average — momentum is strong."
        elif short_ma_val < long_ma_val:
            signal = "🔻 SELL"
            trend = "Bearish"
            trend_expl = "The short-term trend is below the long-term average — momentum may be weakening."
        else:
            signal = "⏸ HOLD"
            trend = "Neutral"
            trend_expl = "Short- and long-term trends are aligned — direction unclear."

        st.markdown(f"### Recommendation: {signal}")
        st.markdown(f"📊 **Current Trend**: {trend} — ✅ {trend_expl}")

        # Confidence Score
        ma_diff = abs(short_ma_val - long_ma_val)
        trend_slope = ma_short.iloc[-1] - ma_short.iloc[-5]
        volatility_factor = max(0, 1 - atr / close_price)
        consistency = hist["Close"].rolling(window=10).mean().std()
        signal_strength = int(min(100, (ma_diff * 3 + trend_slope * 100 + volatility_factor * 50 - consistency * 2)))
        signal_strength = max(0, min(signal_strength, 100))

        # Confidence Meter Display
        confidence_bar = "🔴🟠🟡🟢"
        color = "🟢" if signal_strength >= 75 else "🟡" if signal_strength >= 50 else "🟠" if signal_strength >= 25 else "🔴"
        st.markdown(f"📈 **Signal Confidence**: {signal_strength}% {color}")

        # Moonvest AI Advice Box
        st.markdown("### 🧠 Moonvest Strategy Insight")
        st.success(f"""
- 🎯 **Buy Target Zone**: Around ${round(close_price, 2)}  
- 🛑 **Suggested Stop Loss**: ${stop}  
- 📦 **Recommended Position Size**: {shares} shares  
- 🧮 **Max Risk Amount**: ${max_loss}  
- ⏳ *Trend is {trend.lower()} — suitable for {goal.lower()} strategies and {experience.lower()} investors.*
""")

        # Risk-adjusted advice
        if goal == "High Growth":
            st.success("📈 Your high-growth goal aligns with the current bullish momentum.")
        elif experience == "Beginner" and risk < 30:
            st.warning("🧠 As a beginner with low risk tolerance, consider ETFs or dollar-cost averaging.")
        elif atr > close_price * 0.1:
            st.warning("⚠️ You may want to reduce position size due to high volatility.")

        # Why this makes sense (Simple / Advanced)
        with st.expander("📌 Why this makes sense (click to expand)"):
            if insight_mode == "Simple":
                st.markdown(f"""
- 📈 **Short-term trend (20-day avg):** ${short_ma_val}  
- 🧭 **Long-term trend (50-day avg):** ${long_ma_val}  
- 📊 **Daily movement (ATR):** ${atr}  
- 🛑 **Suggested safety stop:** ≈ ${stop}

---

### Here's what it means:
1. **Your current price is {abs(percent_below_ma)}% {'below' if percent_below_ma < 0 else 'above'} the long-term trend.**  
2. The short-term trend is **{'above' if short_ma_val > long_ma_val else 'below'}** the long-term trend — that's a sign of momentum **{'building' if short_ma_val > long_ma_val else 'slowing down'}**.  
3. Based on your risk setting of **{risk}%**, Moonvest suggests you only risk **${max_loss}** on this trade.  
4. That means you could trade up to **{shares} shares** and protect yourself with a stop-loss at **${stop}**.

💡 *This setup looks like a good opportunity right now, but you're protected if momentum shifts.*
                """)
            else:
                st.markdown(f"""
### 📊 Technical Breakdown
- 20-day MA: ${short_ma_val}  
- 50-day MA: ${long_ma_val}  
- ATR (14): ${atr}  
- % Distance from 50 MA: {percent_below_ma}%  
- Stop-Loss Recommendation: ${stop}  
- Max Risk Allowed: ${max_loss}  
- Position Sizing Formula:  
  Shares = Risk ÷ (2 × ATR) = {max_loss} ÷ {round(2 * atr, 2)} = {shares} shares

---

### 🧠 Interpretation:
- Trend Signal: **{trend.upper()}** — based on crossover of short vs. long moving averages  
- Strategy Fit: Appropriate for **{goal.lower()}** strategies and **{experience.lower()}** investors  
- Risk Tools: Volatility-adjusted stop and sizing included
                """)

        if geek_mode:
            st.markdown("---")
            st.markdown("### 🧠 Geek Mode – Raw Data")
            st.code(f"""
Price: ${round(close_price, 2)}
20-day MA: {short_ma_val}
50-day MA: {long_ma_val}
ATR (14): {atr}
% Distance from 50 MA: {percent_below_ma}%
Suggested Stop: ${stop}
Position Size: {shares} shares @ max ${max_loss} risk
            """, language='python')

        with st.expander("🧾 Show Historical Data"):
            st.dataframe(hist_full.tail(30))

        st.caption("📘 Disclaimer: Moonvest provides educational insights only. No financial advice is given. Invest responsibly.")
    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
