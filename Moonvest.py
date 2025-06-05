import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Moonvest - Smart Stock Analyzer", page_icon="🌕", layout="wide")
st.title("\U0001F315 Moonvest: Smart Stock Analyzer")

# Sidebar Inputs
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Capital Preservation", "Balanced Strategy"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000)
geek_mode = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"], index=0)

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
        short_ma_val = ma_short.iloc[-1]
        long_ma_val = ma_long.iloc[-1]
        atr = (hist["High"] - hist["Low"]).rolling(window=14).mean().iloc[-1]
        stop = round(close_price - 2 * atr, 2)
        percent_below_ma = round(((close_price - long_ma_val) / long_ma_val) * 100, 2)
        position_risk_pct = round(risk / 100, 2)
        max_loss_per_trade = round(equity * position_risk_pct, 2)
        shares = int(max_loss_per_trade / (2 * atr)) if atr > 0 else 0

        short_trend_rising = short_ma_val > ma_short.iloc[-2]
        long_trend_rising = long_ma_val > ma_long.iloc[-2]
        trend = "Bullish" if short_ma_val > long_ma_val else "Bearish" if short_ma_val < long_ma_val else "Neutral"

        # Trend Summary
        st.info(f"🔺 Price is {abs(percent_below_ma)}% {'above' if percent_below_ma > 0 else 'below'} the 50-day average. "
                 f"The short-term average is {'rising' if short_trend_rising else 'falling'}, and the long-term average is {'rising' if long_trend_rising else 'falling'}.")

        signal = "🔻 SELL" if trend == "Bearish" else "🚀 BUY" if trend == "Bullish" else "⏸ HOLD"
        st.markdown(f"### Recommendation: {signal}")

        st.markdown(f"""
        🌐 **Current Trend:** {trend} ✅ The short-term trend is {'above' if trend == 'Bullish' else 'below' if trend == 'Bearish' else 'equal to'} the long-term average — momentum is {'strong' if trend == 'Bullish' else 'weak' if trend == 'Bearish' else 'unclear'}.
        """)

        with st.expander("📊 What this means"):
            if trend == "Bullish":
                st.success("A bullish trend means recent price action is strong. Momentum favors continued growth in the near-term.")
            elif trend == "Bearish":
                st.warning("A bearish trend signals weakening momentum. Be cautious — prices may continue falling or become volatile.")
            else:
                st.info("Momentum is unclear. It may be better to wait for a clearer signal before acting.")

        # Risk-Adjusted Advice Section
        st.markdown("### 🎯 Risk-Adjusted Advice")
        advice = []
        if goal == "High Growth" and trend == "Bullish":
            advice.append("Your high-growth goal aligns with the current bullish momentum.")
        if risk < 30 and atr > 10:
            advice.append("You may want to reduce position size due to high volatility.")
        if experience == "Beginner" and risk < 30:
            advice.append("As a beginner with low risk tolerance, consider starting with ETFs.")
        for tip in advice:
            st.success(f"📉 {tip}")

        with st.expander("📌 Why this makes sense (click to expand)"):
            st.markdown(f"""
- 📉 **Short-term trend (20-day avg):** ${round(short_ma_val, 2)}
- 🌍 **Long-term trend (50-day avg):** ${round(long_ma_val, 2)}
- 🌃 **Daily movement (ATR):** ${round(atr, 2)}
- 🔴 **Suggested safety stop:** ≈ ${stop}
---
### Here's what it means:
1. **Your current price is {abs(percent_below_ma)}% {'below' if percent_below_ma < 0 else 'above'} the long-term trend.**
2. The short-term trend is **{'above' if short_ma_val > long_ma_val else 'below'}** the long-term trend — that's a sign of momentum **{'building' if short_ma_val > long_ma_val else 'slowing down'}**.
3. Based on your risk setting of **{risk}%**, Moonvest suggests you only risk **${max_loss_per_trade}** on this trade.
4. That means you could trade up to **{shares} shares** and protect yourself with a stop-loss at **${stop}** in case things go the other way.
> 💡 Simply put: This setup looks like a good opportunity **right now**, but you're protected if momentum shifts. We give you the math — you stay in control.
            """)

        if geek_mode:
            st.markdown("---")
            st.markdown("### 🧠 Geek Mode – Raw Data")
            st.code(f"""
Price: ${round(close_price, 2)}
20-day MA: {round(short_ma_val, 2)}
50-day MA: {round(long_ma_val, 2)}
ATR (14): {round(atr, 2)}
% Below 50-day MA: {percent_below_ma}%
Suggested Stop: ${stop}
Position Size: {shares} shares @ max ${max_loss_per_trade} risk
            """, language='python')

        with st.expander("🧾 Show Historical Data"):
            st.dataframe(hist_full.tail(30))

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
