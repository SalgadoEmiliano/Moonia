import os
import requests
from dotenv import load_dotenv

# Load .env at the module level
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def explain_signal(ticker: str, signal: str, strategy: str = "Moving Averages & Momentum") -> str:
    """
    Use OpenRouter AI to explain the quant signal in plain English.
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
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",  # GOOD free model for this type of use
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.6
            }
        )
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"⚠️ Error generating explanation: {e}"
