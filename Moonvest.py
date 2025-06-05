import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

st.set_page_config(page_title="Moonvest - Smart Stock Analyzer", layout="wide")
st.title("🌕 Moonvest: Smart Stock Analyzer")

# Description
st.markdown("""
Moonvest is a stock analysis engine delivering simple yet powerful insights.  
🚀 Backed by logic. 📈 Built for clarity. 🌕 Designed to guide your investments to the moon.
""")

st.markdown("---")
st.markdown("### 🌍 Our Mission")
st.markdown("Democratizing financial strategy for every investor — beginner or pro.")

# Sidebar Inputs
st.sidebar.header("Investor Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")
goal = st.sidebar.selectbox("Investment Goal", ["High Growth", "Capital Preservation", "Balanced Strategy"])
risk = st.sidebar.slider("Risk Tolerance (%)", 0, 100, 50)
experience = st.sidebar.selectbox("Investor Experience", ["Beginner", "Intermediate", "Advanced"])
equity = st.sidebar.number_input("Account Equity ($)", min_value=100, value=1000)
insight_mode = st.sidebar.radio("Insight Mode", ["Simple", "Advanced"])

# Button
if st.sidebar.button("🚀 Launch Analysis"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        st.subheader(f"📈 {ticker.upper()} - Performance Chart")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="Close Price"))
        fig.update_layout(template="plotly_dark", hovermode="x unified", height=500)
        st.plotly_chart(fig, use_container_width=True)

        ma_short = hist["Close"].rolling(window=20).mean()
        ma_long = hist["Close"].rolling(window=50).mean()
        atr = hist["High"].subtract(hist["Low"]).rolling(window=14).mean().iloc[-1]
        stop_loss = hist["Close"].iloc[-1] - atr

        if ma_short.iloc[-1] < ma_long.iloc[-1]:
            signal = "🔻 SELL"
            explanation = "The short-term trend has dropped below the long-term trend. Risk is elevated."
        elif ma_short.iloc[-1] > ma_long.iloc[-1]:
            signal = "🚀 BUY"
            explanation = "Momentum is positive — the short-term trend is leading the long-term average."
        else:
            signal = "⏸ HOLD"
            explanation = "No clear signal yet. Price is stabilizing."

        st.markdown(f"### 📌 Recommendation: {signal}")
        st.markdown(explanation)

        if insight_mode == "Advanced":
            st.markdown("#### 🔍 Why This Makes Sense:")
            st.markdown(f"""
- **Short-term (20-day MA):** {ma_short.iloc[-1]:.2f}  
- **Long-term (50-day MA):** {ma_long.iloc[-1]:.2f}  
- **Daily movement (ATR):** {atr:.2f}  
- **Suggested safety stop-loss:** ≈ {stop_loss:.2f}  
""")

        with st.expander("🧾 Show Historical Data"):
            st.dataframe(hist.tail(30))

        # 📤 Export as PDF
        def generate_pdf():
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # Header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "🌕 Moonvest Investor Report")
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 65, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.line(50, height - 70, width - 50, height - 70)

            # Body
            y = height - 100
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"Stock Ticker: {ticker.upper()}")
            y -= 20
            c.drawString(50, y, f"Recommendation: {signal}")
            y -= 20
            c.drawString(50, y, f"Explanation: {explanation}")
            y -= 40

            c.drawString(50, y, "Key Metrics:")
            y -= 20
            c.drawString(70, y, f"20-day MA: {ma_short.iloc[-1]:.2f}")
            y -= 20
            c.drawString(70, y, f"50-day MA: {ma_long.iloc[-1]:.2f}")
            y -= 20
            c.drawString(70, y, f"ATR (14-day): {atr:.2f}")
            y -= 20
            c.drawString(70, y, f"Suggested Stop-Loss: {stop_loss:.2f}")
            y -= 40

            c.drawString(50, y, "Investor Profile:")
            y -= 20
            c.drawString(70, y, f"Goal: {goal}")
            y -= 20
            c.drawString(70, y, f"Risk Tolerance: {risk}%")
            y -= 20
            c.drawString(70, y, f"Experience: {experience}")
            y -= 20
            c.drawString(70, y, f"Equity: ${equity:,.2f}")

            # Footer
            c.setFont("Helvetica-Oblique", 8)
            c.drawString(50, 40, "Empowering smarter investing — www.moonvest.app")
            c.drawString(50, 28, "This report is for informational purposes only and does not constitute financial advice.")
            c.drawRightString(width - 50, 28, "Page 1 of 1")
            c.save()
            buffer.seek(0)
            return buffer

        pdf = generate_pdf()
        st.download_button("📤 Export as PDF", data=pdf, file_name="Moonvest_Report.pdf")

    except Exception as e:
        st.error("⚠️ Error loading stock data. Please verify the ticker and try again.")
