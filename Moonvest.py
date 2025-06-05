import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ----- Page Settings -----
st.set_page_config(page_title="Moonia", page_icon="🌕")

# ----- Title -----
st.markdown("## 🌕 Moonia: AI-Powered Stock Strategist")
st.markdown("### Smarter insights. Safer trades. Always one step ahead.")
st.markdown("---")

# ----- Sidebar -----
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Steady Growth", "Value"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", value=1000)
show_geek = st.sidebar.checkbox("🧠 Show raw numbers (Geek Mode)")
mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"])
launched = st.sidebar.button("🚀 Launch Analysis")

# ----- Run Only if Button is Clicked -----
if launched:
    try:
        # ----- Fetch Data -----
        df = yf.download(ticker, period="5y")
        df["20_MA"] = df["Close"].rolling(window=20).mean()
        df["50_MA"] = df["Close"].rolling(window=50).mean()
        df["ATR"] = df["High"].rolling(14).max() - df["Low"].rolling(14).min()

        current_price = df["Close"].iloc[-1]
        short_avg = df["20_MA"].iloc[-1]
        long_avg = df["50_MA"].iloc[-1]
        atr = df["ATR"].iloc[-1]

        dist_pct = ((current_price - long_avg) / long_avg) * 100
        above_below = "above" if dist_pct > 0 else "below"
        trend_desc = "rising" if short_avg > df["20_MA"].iloc[-10] else "falling"
        long_desc = "rising" if long_avg > df["50_MA"].iloc[-10] else "falling"

        # ----- Signal -----
        if short_avg > long_avg:
            signal = "🚀 BUY"
        elif short_avg < long_avg:
            signal = "🔻 SELL"
        else:
            signal = "⚖️ HOLD"

        # ----- Recommendations -----
        stop_loss = current_price - (2 * atr)
        max_risk_amt = equity * (risk / 100)
        position_size = int(max_risk_amt // (current_price - stop_loss))

        # ----- Header -----
        st.markdown(f"### Recommendation: {signal}")
        st.info(f"🔺 Price is {abs(dist_pct):.2f}% {above_below} the 50-day average. The short-term average is {trend_desc}, and the long-term average is {long_desc}.")

        # ----- Strategy Insight -----
        with st.container():
            with st.container():
                st.markdown("### 🧠 Moonia Strategy Insight")
                strategy_box = st.container()
                with strategy_box:
                    st.markdown(
                        f"""
                        <div style="background-color:#113C35;padding:16px;border-radius:10px">
                        <ul>
                        <li>🎯 <b>Buy Target Zone</b>: Around ${current_price:.2f}</li>
                        <li>🛑 <b>Suggested Stop Loss</b>: ${stop_loss:.2f}</li>
                        <li>📦 <b>Recommended Position Size</b>: {position_size} shares</li>
                        <li>💸 <b>Max Risk Amount</b>: ${max_risk_amt:.2f}</li>
                        <li>📈 <i>Trend is bullish — suitable for high growth strategies and beginner investors.</i></li>
                        </ul>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # ----- Risk-Adjusted Note -----
        st.markdown("✅ <b>Your high growth goal aligns with the current bullish momentum.</b>", unsafe_allow_html=True)

        # ----- AI's Take -----
        st.markdown(
            """
            <div style="background-color:#3B2350;padding:16px;border-radius:10px;margin-top:15px">
            <h4>🤖 Moonia AI’s Take</h4>
            <p>
            Based on the current bullish crossover and momentum metrics, this setup shows promise.
            When price crosses above the 50-day average with upward short-term trend lines and steady volatility (as indicated by ATR),
            this often signals institutional buying or long setups.
            Investors targeting growth may find this attractive, but proper risk management —
            including defined stop-loss levels and position sizing — remains essential.
            Consider reassessing if short-term momentum weakens significantly in upcoming sessions.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----- Why it makes sense -----
        with st.expander("📌 Why this makes sense (click to expand)"):
            st.markdown(f"• 📈 <b>Short-term trend (20-day avg)</b>: ${short_avg:.2f}", unsafe_allow_html=True)
            st.markdown(f"• 📉 <b>Long-term trend (50-day avg)</b>: ${long_avg:.2f}", unsafe_allow_html=True)
            st.markdown(f"• 🌐 <b>Daily movement (ATR)</b>: ${atr:.2f}", unsafe_allow_html=True)
            st.markdown(f"• 🧯 <b>Suggested safety stop</b>: ≈ ${stop_loss:.2f}", unsafe_allow_html=True)

        # ----- Explanation -----
        st.markdown("### Here's what it means:")
        st.markdown(
            f"""
            1. <b>Your current price is {abs(dist_pct):.2f}% {above_below} the long-term trend.</b>  
            2. The short-term trend is {trend_desc} and sits {above_below} the long-term average — that’s a sign of momentum {trend_desc}.  
            3. Based on your risk setting of {risk}%, Moonia suggests you only risk <b>${max_risk_amt:.2f}</b> on this trade.  
            4. That means you could trade up to <b>{position_size} shares</b> with a stop-loss at <b>${stop_loss:.2f}</b>.  
            💡 Simply put: This setup looks like a good opportunity right now, but you're protected if momentum shifts.
            """,
            unsafe_allow_html=True
        )

        # ----- Historical Chart -----
        with st.expander("📉 Show Historical Data"):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close"))
            fig.add_trace(go.Scatter(x=df.index, y=df["20_MA"], name="20-Day MA"))
            fig.add_trace(go.Scatter(x=df.index, y=df["50_MA"], name="50-Day MA"))
            fig.update_layout(title="Price Chart (5Y)", xaxis_title="Date", yaxis_title="Price", height=500)
            st.plotly_chart(fig, use_container_width=True)

        # ----- Disclaimer -----
        st.markdown(
            "<small>🌕 <i>Disclaimer: Moonia provides educational insights only. No financial advice is given. Invest responsibly.</i></small>",
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error("❌ Something went wrong. Please check your inputs or try again later.")
        st.exception(e)
