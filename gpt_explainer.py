import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env at the module level
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def explain_signal(ticker: str, signal: str, strategy: str = "Moving Averages & Momentum") -> str:
    """
    Use GPT to explain the quant signal in plain English.

    :param ticker: Stock ticker (e.g., AAPL)
    :param signal: 'BUY', 'SELL', 'HOLD'
    :param strategy: Strategy name
    :return: Natural language explanation
    """
    prompt = f"""
You are the AI engine behind Moonia — an advanced stock strategist app.

Your job is to explain this stock signal clearly to a retail investor. Be professional but friendly. Do NOT give financial advice or guarantee outcomes. Focus on the signal, reasoning, and what a user may wish to think about. Write about 3-5 sentences.

Stock: {ticker}
Strategy: {strategy}
Signal: {signal}

Explain what this signal likely means based on the strategy and why it was triggered.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating explanation: {e}"
