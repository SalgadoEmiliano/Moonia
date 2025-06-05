import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Moonia – AI-Powered Stock Strategist", layout="wide")

# Title + Tagline
st.markdown("<h1 style='font-size: 2.4em;'>🌕 Moonia: AI-Powered Stock Strategist</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:gray;margin-top:-15px;'>Smarter insights. Safer trades. Always one step ahead.</h4>", unsafe_allow_html=True)

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
        percent_below_ma = round(((close_price - long_ma_val) / long_ma_val) * 100, 2)
        position_risk_pct = round(risk / 100, 2)
        max_loss_per_trade = round(equity * position_risk_pct, 2)
        shares = int(max_loss_per_trade / (2 * atr)) if atr > 0 else 0

        # Market condition banner
        icon = "🟢" if percent_below_ma >= 0 else "🔺"
        st.markdown(
            f"<div style='background-color:#1f355a;padding:10px;border-radius:5px;color:white'>"
            f"{icon} Price is {abs(percent_below_ma)}% {'above' if percent_below_ma >= 0 else 'below'} the 50-day average. "
            f"The short-term average is {'rising' if short_ma_val > ma_short.iloc[-2] else 'falling'}, and the long-term average is "
            f"{'rising' if long_ma_val > ma_long.iloc[-2] else 'falling'}.</div>", unsafe_allow_html=True)

        # Recommendation
        if short_ma_val > long_ma_val:
            signal = "🚀 BUY"
            trend_outlook = "bullish"
        elif short_ma_val < long_ma_val:
            signal = "🔻 SELL"
            trend_outlook = "bearish"
        else:
            signal = "⏸ HOLD"
            trend_outlook = "neutral"

        st.markdown(f"### Recommendation: {signal}")

        # Strategy Insight Panel
        with st.container():
            st.markdown("""
                <div style='background-color:#1c3d2e;padding:15px;border-radius:8px;color:white'>
                <h4>🧠 Moonia Strategy Insight</h4>
                <ul>
                <li>🎯 <strong>Buy Target Zone:</strong> Around ${:.2f}</li>
                <li>🛑 <strong>Suggested Stop Loss:</strong> ${}</li>
                <li>📦 <strong>Recommended Position Size:</strong> {} shares</li>
                <li>💸 <strong>Max Risk Amount:</strong> ${}</li>
                <li>📈 <em>Trend is {}</em> — suitable for {} strategies and {} investors.</li>
                </ul>
                </div>
            """.format(
                close_price, stop, shares, max_loss_per_trade,
                trend_outlook,
                goal.lower(),
                experience.lower()
            ), unsafe_allow_html=True)

        # Moonia AI's Take
        ai_take = {
            "bullish": "Momentum is strong. This could be a good entry point, but always use a stop-loss.",
            "bearish": "Momentum is fading. Consider waiting for a reversal or using tighter stops.",
            "neutral": "The market is indecisive. Look for confirmation before entering a position."
        }

        st.markdown(
            f"<div style='background-color:#264d1f;padding:10px;border-radius:5px;color:white;margin-top:8px;'>"
            f"✅ <strong>Your {goal.lower()} goal aligns with the current {trend_outlook} momentum.</strong>"
            f"</div>", unsafe_allow_html=True)

        st.markdown(
            f"<div style='background-color:#1c1c1c;padding:14px;border-radius:8px;margin-top:12px;'>"
            f"<h4 style='color:white;'>🤖 Moonia AI’s Take</h4>"
            f"<p style='color:#d3d3d3;'>{ai_take[trend_outlook]}</p>"
            f"</div>", unsafe_allow_html=True)

        # Insights Section
        with st.expander("📌 Why this makes sense (click to expand)"):
            if insight_mode == "Simple":
                st.markdown(f"""
- 📈 **Short-term trend (20-day avg):** ${round(short_ma_val, 2)}
- 🌍 **Long-term trend (50-day avg):** ${round(long_ma_val, 2)}
- 📊 **Daily movement (ATR):** ${round(atr, 2)}
- 🛑 **Suggested safety stop:** ≈ ${stop}

---

### Here's what it means:

1. **Your current price is {abs(percent_below_ma)}% {'below' if percent_below_ma < 0 else 'above'} the long-term trend.**
2. The short-term trend is **{'above' if short_ma_val > long_ma_val else 'below'}** the long-term trend — that's a sign of momentum **{'building' if short_ma_val > long_ma_val else 'slowing down'}**.
3. Based on your risk setting of **{risk}%**, Moonia suggests you only risk **${max_loss_per_trade}** on this trade.
4. That means you could trade up to **{shares} shares** and protect yourself with a stop-loss at **${stop}** in case things go the other way.

💡 *This setup looks like a good opportunity right now, but you're protected if momentum shifts.*
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

- Trend Signal: **{trend_outlook.upper()}** — based on moving average crossovers.
- Strategy Fit: **Good for {goal.lower()} goals with {experience.lower()} investors.**
- Volatility-adjusted sizing and stop-loss included.
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

        with st.expander("📜 Show Historical Data"):
            st.dataframe(hist_full.tail(30))

        st.markdown(
            "<p style='color:#888;margin-top:30px;'>🤖 <em>Disclaimer: Moonia provides educational insights only. No financial advice is given. Invest responsibly.</em></p>",
            unsafe_allow_html=True)

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
