import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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

# Launch
if st.sidebar.button("🚀 Launch Analysis"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        hist_full = stock.history(period="5y")

        st.subheader(f"📈 {ticker.upper()} - 5 Year Performance")

        # Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_full.index,
            y=hist_full["Close"],
            mode="lines",
            name="Close Price"
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # Indicators
        close_price = hist["Close"].iloc[-1]
        ma_short = hist["Close"].rolling(window=20).mean()
        ma_long = hist["Close"].rolling(window=50).mean()
        short_ma_val = ma_short.iloc[-1]
        long_ma_val = ma_long.iloc[-1]
        atr = (hist["High"] - hist["Low"]).rolling(window=14).mean().iloc[-1]
        stop = round(close_price - 2 * atr, 2)
        percent_below_ma = round(((close_price - ma_long.iloc[-1]) / ma_long.iloc[-1]) * 100, 2)
        position_risk_pct = round(risk / 100, 2)
        max_loss_per_trade = round(equity * position_risk_pct, 2)
        shares = int(max_loss_per_trade / (2 * atr)) if atr > 0 else 0

        # Summary Banner
        st.info(f"📉 Price is {percent_below_ma}% {'below' if percent_below_ma < 0 else 'above'} the 50-day average. "
                f"The short-term average is {'rising' if short_ma_val > ma_short.iloc[-2] else 'falling'}, "
                f"and the long-term average is {'rising' if long_ma_val > ma_long.iloc[-2] else 'falling'}.")

        # Signal
        if short_ma_val < long_ma_val:
            signal = "🔻 SELL"
            explanation = "Short-term momentum has dropped below the long-term trend. Risk is elevated."
        elif short_ma_val > long_ma_val:
            signal = "🚀 BUY"
            explanation = "Short-term trend is strong. Market momentum supports upside potential."
        else:
            signal = "⏸ HOLD"
            explanation = "No clear trend direction. Hold for now."

        st.markdown(f"### Recommendation: {signal}")

        # Insight Box
        with st.expander("📌 Why this makes sense (click to expand)"):
            st.markdown(f"""
**Short-term average:** {round(short_ma_val, 2)}  
**Long-term average:** {round(long_ma_val, 2)}  
**ATR (14):** {round(atr, 2)}  
**Suggested stop:** ≈ ${stop}

1. Your current price is **{percent_below_ma}% {('below' if percent_below_ma < 0 else 'above')}** the long-term trend.
2. This setup suggests that recent momentum is **{'weakening' if short_ma_val < long_ma_val else 'improving'}**.
3. Based on your risk tolerance of **{risk}%**, your suggested loss cap is **${max_loss_per_trade}**.
4. You could buy/sell approximately **{shares} shares** with a stop-loss at **${stop}** to match your risk.

{f"5. As a {experience.lower()}, consider managing your position cautiously. Diversify and rebalance gradually." if experience == 'Beginner' else ""}
            """)

        # Raw Geek Mode
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
