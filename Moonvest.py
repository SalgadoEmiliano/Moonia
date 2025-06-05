import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Moonvest - Smart Stock Analyzer", layout="wide")
st.title("🌕 Moonvest: Smart Stock Analyzer")

# Sidebar
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Capital Preservation", "Balanced Strategy"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000)
geek_mode = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"], index=0)

# Launch button
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

        # Indicators
        close = hist["Close"].iloc[-1]
        ma20 = hist["Close"].rolling(window=20).mean().iloc[-1]
        ma50 = hist["Close"].rolling(window=50).mean().iloc[-1]
        atr = (hist["High"] - hist["Low"]).rolling(window=14).mean().iloc[-1]
        stop_loss = round(close - 2 * atr, 2)
        percent_diff = round(((close - ma50) / ma50) * 100, 2)
        trend_slope = ma20 - ma50
        max_risk = round(equity * (risk / 100), 2)
        shares = int(max_risk / (2 * atr)) if atr > 0 else 0

        # Trend direction
        if ma20 > ma50:
            signal = "🚀 BUY"
            trend = "Bullish"
            trend_text = "📈 Trend is bullish — suitable for high growth strategies and beginner investors."
            emoji = "🟢"
        elif ma20 < ma50:
            signal = "🔻 SELL"
            trend = "Bearish"
            trend_text = "📉 Trend is bearish — consider reducing position or waiting for confirmation."
            emoji = "🔴"
        else:
            signal = "⏸ HOLD"
            trend = "Neutral"
            trend_text = "⏸ Trend is neutral — market is uncertain."

        # Summary Alert
        st.info(f"{emoji} Price is {abs(percent_diff)}% {'above' if percent_diff > 0 else 'below'} the 50-day average. "
                f"The short-term average is {'rising' if ma20 > hist['Close'].rolling(20).mean().iloc[-2] else 'falling'}, "
                f"and the long-term average is {'rising' if ma50 > hist['Close'].rolling(50).mean().iloc[-2] else 'falling'}.")

        # Recommendation
        st.markdown(f"### Recommendation: {signal}")

        # Moonvest Strategy Insight Box
        with st.container():
            st.markdown("""
<div style='background-color:#1c3d2e; padding:20px; border-radius:10px'>
<h3 style='color:white'>🧠 Moonvest Strategy Insight</h3>
<ul style='color:white'>
<li>🎯 <strong>Buy Target Zone:</strong> Around ${:.2f}</li>
<li>🛑 <strong>Suggested Stop Loss:</strong> ${}</li>
<li>📦 <strong>Recommended Position Size:</strong> {} shares</li>
<li>💸 <strong>Max Risk Amount:</strong> ${}</li>
<li>📈 <em>{}</em></li>
</ul>
</div>
""".format(close, stop_loss, shares, max_risk, trend_text), unsafe_allow_html=True)

        # Alignment Notice Box
        st.markdown(f"<div style='background-color:#23492c; padding:12px; border-radius:8px; color:white'>"
                    f"✅ <strong>Your {goal.lower()} goal aligns with the current {trend.lower()} momentum.</strong></div>",
                    unsafe_allow_html=True)

        # Insights Section
        with st.expander("📌 Why this makes sense (click to expand)"):
            if insight_mode == "Simple":
                st.markdown(f"""
- 📉 **Short-term trend (20-day avg):** ${round(ma20, 2)}
- 🌐 **Long-term trend (50-day avg):** ${round(ma50, 2)}
- 📊 **Daily movement (ATR):** ${round(atr, 2)}
- 🛑 **Suggested safety stop:** ≈ ${stop_loss}

---

### Here's what it means:

1. **Your current price is {abs(percent_diff)}% {'above' if percent_diff > 0 else 'below'} the long-term trend.**
2. The short-term trend is **{'above' if trend == 'Bullish' else 'below'}** the long-term trend — that's a sign of momentum **{'building' if trend == 'Bullish' else 'slowing'}**.
3. Based on your risk setting of **{risk}%**, Moonvest suggests you only risk **${max_risk}** on this trade.
4. That means you could trade up to **{shares} shares** and protect yourself with a stop-loss at **${stop_loss}**.

💡 *This setup looks like a good opportunity right now, but you're protected if momentum shifts.*
                """)
            else:
                st.markdown(f"""
### 🔍 Technical Breakdown

- **20-day MA:** ${round(ma20, 2)}
- **50-day MA:** ${round(ma50, 2)}
- **ATR (14):** ${round(atr, 2)}
- **% Distance from 50 MA:** {percent_diff}%
- **Stop-Loss Recommendation:** ${stop_loss}
- **Max Risk Allowed:** ${max_risk}
- **Position Sizing Formula:**  
  `Shares = Risk ÷ (2 × ATR)` = {max_risk} ÷ {round(2 * atr, 2)} = **{shares} shares**

---

### 📌 Interpretation

- **Trend Signal:** {trend.upper()} — based on crossover of short vs. long moving averages  
- **Strategy Fit:** Suitable for {goal.lower()} investors with {experience.lower()} experience  
- **Risk Control:** Volatility-adjusted stop and sizing is factored in
                """)

        # Geek Mode
        if geek_mode:
            st.markdown("---")
            st.markdown("### 🧠 Geek Mode – Raw Data")
            st.code(f"""
Price: ${round(close, 2)}
20-day MA: {round(ma20, 2)}
50-day MA: {round(ma50, 2)}
ATR (14): {round(atr, 2)}
% from 50-day MA: {percent_diff}%
Stop Loss: ${stop_loss}
Max Risk: ${max_risk}
Position Size: {shares} shares
            """, language='python')

        with st.expander("📄 Show Historical Data"):
            st.dataframe(hist_full.tail(30))

        # Disclaimer
        st.markdown("<br><div style='font-size: 0.9em; color: grey;'>"
                    "🧠 <em>Disclaimer: Moonvest provides educational insights only. No financial advice is given. Invest responsibly.</em></div>",
                    unsafe_allow_html=True)

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
