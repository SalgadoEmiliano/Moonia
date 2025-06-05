import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Moonvest - Smart Stock Analyzer", layout="wide")
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

# Launch Analysis
if st.sidebar.button("🚀 Launch Analysis"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        hist_full = stock.history(period="5y")

        st.subheader(f"📈 {ticker.upper()} - 5 Year Performance")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_full.index, y=hist_full["Close"], mode="lines", name="Close Price"))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # Calculate Indicators
        close = hist["Close"].iloc[-1]
        ma_short = hist["Close"].rolling(window=20).mean()
        ma_long = hist["Close"].rolling(window=50).mean()
        ma_short_val = ma_short.iloc[-1]
        ma_long_val = ma_long.iloc[-1]
        atr = (hist["High"] - hist["Low"]).rolling(window=14).mean().iloc[-1]
        stop_loss = round(close - 2 * atr, 2)
        percent_diff = round(((close - ma_long_val) / ma_long_val) * 100, 2)
        max_risk = round(equity * (risk / 100), 2)
        shares = int(max_risk / (2 * atr)) if atr > 0 else 0

        # Determine Trend
        if ma_short_val > ma_long_val:
            trend = "bullish"
            signal = "🚀 BUY"
            trend_text = "Trend is bullish — suitable for high growth strategies and beginner investors."
            trend_color = "🟢"
        elif ma_short_val < ma_long_val:
            trend = "bearish"
            signal = "🔻 SELL"
            trend_text = "Trend is bearish — caution advised based on recent signals."
            trend_color = "🔴"
        else:
            trend = "neutral"
            signal = "⏸ HOLD"
            trend_text = "No clear trend detected — consider waiting for a stronger signal."
            trend_color = "🟡"

        # Summary Box
        st.markdown(
            f"<div style='background-color:#1c2c44; padding:10px; border-radius:8px; color:white;'>"
            f"{'🟢' if percent_diff >= 0 else '🔺'} Price is {abs(percent_diff)}% "
            f"{'above' if percent_diff >= 0 else 'below'} the 50-day average. "
            f"The short-term average is {'rising' if ma_short.iloc[-1] > ma_short.iloc[-2] else 'falling'}, "
            f"and the long-term average is {'rising' if ma_long.iloc[-1] > ma_long.iloc[-2] else 'falling'}."
            f"</div>", unsafe_allow_html=True
        )

        st.markdown(f"### Recommendation: {signal}")

        # Strategy Insight Box
        st.markdown(f"""
        <div style='background-color:#1c3d2e; padding:20px; border-radius:10px; margin-bottom:15px'>
        <h3 style='color:white'>🧠 Moonvest Strategy Insight</h3>
        <ul style='color:white; font-size:16px'>
        <li>🎯 <strong>Buy Target Zone:</strong> Around ${round(close, 2)}</li>
        <li>🛑 <strong>Suggested Stop Loss:</strong> ${stop_loss}</li>
        <li>📦 <strong>Recommended Position Size:</strong> {shares} shares</li>
        <li>💸 <strong>Max Risk Amount:</strong> ${max_risk}</li>
        <li>📈 <em>{trend_text}</em></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        # Personal Advice Box
        st.markdown(
            f"<div style='background-color:#264d2c; padding:12px; border-radius:10px; "
            f"margin-bottom:16px; color:white;'>✅ Your <strong>{goal.lower()}</strong> goal aligns with the current "
            f"<strong>{trend} momentum</strong>.</div>", unsafe_allow_html=True
        )

        # Why This Makes Sense
        with st.expander("📌 Why this makes sense (click to expand)"):
            if insight_mode == "Simple":
                st.markdown(f"""
- 📉 **Short-term trend (20-day avg):** ${round(ma_short_val, 2)}
- 🌍 **Long-term trend (50-day avg):** ${round(ma_long_val, 2)}
- 📊 **Daily movement (ATR):** ${round(atr, 2)}
- 🛑 **Suggested safety stop:** ≈ ${stop_loss}

---

### Here's what it means:

1. **Your current price is {abs(percent_diff)}% {'below' if percent_diff < 0 else 'above'} the long-term trend.**
2. The short-term trend is **{'above' if ma_short_val > ma_long_val else 'below'}** the long-term trend — that's a sign of momentum **{'building' if ma_short_val > ma_long_val else 'slowing down'}**.
3. Based on your risk setting of **{risk}%**, Moonvest suggests you only risk **${max_risk}** on this trade.
4. That means you could trade up to **{shares} shares** and protect yourself with a stop-loss at **${stop_loss}** in case things go the other way.

💡 *This setup looks like a good opportunity right now, but you're protected if momentum shifts.*
                """)
            else:
                st.markdown(f"""
### 📊 Technical Breakdown

- **20-day MA:** ${round(ma_short_val, 2)}
- **50-day MA:** ${round(ma_long_val, 2)}
- **ATR (14):** ${round(atr, 2)}
- **% Distance from 50 MA:** {percent_diff}%
- **Stop-Loss Recommendation:** ${stop_loss}
- **Max Risk Allowed:** ${max_risk}
- **Position Sizing Formula:**  
  Shares = Risk ÷ (2 × ATR) = {max_risk} ÷ {round(2 * atr, 2)} = {shares} shares

---

### 📌 Interpretation:

- Trend Signal: **{trend.upper()}** — based on crossover of short vs. long moving averages
- Strategy Fit: Appropriate for **{goal.lower()}** strategies and **{experience.lower()}** investors
- Volatility-adjusted stop and sizing included for risk control
                """)

        # Geek Mode Raw Output
        if geek_mode:
            st.markdown("### 🧠 Geek Mode – Raw Data")
            st.code(f"""
Price: ${round(close, 2)}
20-day MA: {round(ma_short_val, 2)}
50-day MA: {round(ma_long_val, 2)}
ATR (14): {round(atr, 2)}
% Below 50-day MA: {percent_diff}%
Suggested Stop: ${stop_loss}
Position Size: {shares} shares @ max ${max_risk} risk
            """, language='python')

        with st.expander("🧾 Show Historical Data"):
            st.dataframe(hist_full.tail(30))

        # Disclaimer
        st.markdown(
            "<p style='font-size:14px; color:gray; margin-top:32px'>"
            "🧠 <em>Disclaimer: Moonvest provides educational insights only. No financial advice is given. Invest responsibly.</em>"
            "</p>", unsafe_allow_html=True
        )

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
