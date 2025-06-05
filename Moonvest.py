import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# App config
st.set_page_config(page_title="Moonia", page_icon="🌕", layout="wide")

# Header
st.markdown("<h1 style='font-size: 2.5em;'>🌕 Moonia: AI-Powered Stock Strategist</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #bbb;'>Smarter insights. Safer trades. Always one step ahead.</h4>", unsafe_allow_html=True)
st.markdown("---")

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

        trend_label = "Bullish" if short_ma_val > long_ma_val else "Bearish"
        short_slope = ma_short.iloc[-1] - ma_short.iloc[-2]
        long_slope = ma_long.iloc[-1] - ma_long.iloc[-2]

        signal = "🚀 BUY" if short_ma_val > long_ma_val else "🔻 SELL"
        st.markdown(f"### Recommendation: {signal}")

        st.info(f"{'🟢' if percent_below_ma > 0 else '🔺'} Price is {abs(percent_below_ma)}% "
                f"{'above' if percent_below_ma > 0 else 'below'} the 50-day average. "
                f"The short-term average is {'rising' if short_slope > 0 else 'falling'}, and the "
                f"long-term average is {'rising' if long_slope > 0 else 'falling'}.")


                f"""
            <div style="background-color:#14352C;padding:16px;border-radius:10px;">
            <ul>
            with st.container():
    st.markdown("### 🧠 Moonia Strategy Insight")
    # rest of the green box goes here
            <li>🎯 <strong>Buy Target Zone:</strong> Around ${round(close_price, 2)}</li>
            <li>🛑 <strong>Suggested Stop Loss:</strong> ${stop}</li>
            <li>📦 <strong>Recommended Position Size:</strong> {shares} shares</li>
            <li>💸 <strong>Max Risk Amount:</strong> ${max_loss_per_trade}</li>
            <li>📈 <em>Trend is {trend_label.lower()} — suitable for high growth strategies and {experience.lower()} investors.</em></li>
            </ul>
            </div>
            """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"<div style='background-color:#1B4721;padding:12px 16px;border-radius:8px;margin-top:12px;'>"
            f"✅ <strong>Your {goal.lower()} goal aligns with the current {trend_label.lower()} momentum.</strong>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div style='background-color:#2a1938;padding:16px;border-radius:10px;margin-top:16px;'>"
            f"<h4 style='color:#f5f5f5;'>🤖 Moonia AI’s Take</h4>"
            f"<p style='color:#e0dcee;'>"
            f"Based on the current {trend_label.lower()} crossover pattern and momentum metrics, the setup shows promise. "
            f"When price crosses above the 50-day average with rising short-term trend lines and stable volatility (as measured by ATR), "
            f"it often indicates sustained bullish behavior — especially when supported by volume. If you're targeting high growth, "
            f"this could be an effective entry point. But don't ignore risk: a stop-loss and ongoing monitoring are essential to stay protected."
            f"</p></div>",
            unsafe_allow_html=True
        )

        with st.expander("📌 Why this makes sense (click to expand)"):
            if insight_mode == "Simple":
                st.markdown(f"""
- 📉 **Short-term trend (20-day avg):** ${round(short_ma_val, 2)}
- 📏 **Long-term trend (50-day avg):** ${round(long_ma_val, 2)}
- 📊 **Daily movement (ATR):** ${round(atr, 2)}
- 🛑 **Suggested safety stop:** ≈ ${stop}

---

### Here's what it means:

1. **Your current price is {abs(percent_below_ma)}% {'below' if percent_below_ma < 0 else 'above'} the long-term trend.**
2. The short-term trend is **{'above' if short_ma_val > long_ma_val else 'below'}** the long-term trend — that's a sign of momentum **{'building' if short_ma_val > long_ma_val else 'slowing down'}**.
3. Based on your risk setting of **{risk}%**, Moonia suggests you only risk **${max_loss_per_trade}** on this trade.
4. That means you could trade up to **{shares} shares** and protect yourself with a stop-loss at **${stop}** in case things go the other way.

> 💡 Simply put: This setup looks like a good opportunity **right now**, but you're protected if momentum shifts.
                """)
            else:
                st.markdown(f"""
### 📊 Technical Breakdown

- **20-day MA:** ${round(short_ma_val, 2)}
- **50-day MA:** ${round(long_ma_val, 2)}
- **ATR (14):** ${round(atr, 2)}
- **% Distance from 50 MA:** {percent_below_ma}%
- **Stop-Loss Recommendation:** ${stop}
- **Max Risk Allowed:** ${max_loss_per_trade}
- **Position Sizing Formula:**  
  \> `Shares = Risk ÷ (2 × ATR)`  
  \> `= {max_loss_per_trade} ÷ {round(2 * atr, 2)} = {shares} shares`

---

### 📌 Interpretation:

- Momentum is currently **{trend_label.upper()}**.
- Risk is managed with a **${stop}** stop-loss based on recent volatility.
- Ideal for **{goal.lower()}** strategies with a **{experience.lower()}** investor profile.
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

        with st.expander("🗂 Show Historical Data"):
            st.dataframe(hist_full.tail(30))

        st.markdown(
            "<div style='margin-top:40px;color:#888;font-size:13px;'>🤖 <em>Disclaimer: Moonia provides educational insights only. No financial advice is given. Invest responsibly.</em></div>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
