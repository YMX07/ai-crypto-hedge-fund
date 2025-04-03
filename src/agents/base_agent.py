import json
from tools.llm_interface import call_llm


class BaseAgent:
    def __init__(self, name, prompt_file="config/prompts.json"):
        self.name = name
        with open(prompt_file, 'r') as f:
            self.prompt = json.load(f).get(name, "")

    def generate_signal(self, data, asset="BTC"):
        """
        Generates a trading signal using LLM based on market data.
        Args:
            data (pd.DataFrame): OHLCV data
            asset (str): Crypto asset ticker
        Returns:
            dict: Signal with action, asset, confidence
        """
        if "close" not in data:
            return {"action": "hold", "asset": asset, "confidence": 0.0}

        # Prepare data summary for LLM
        latest_close = data["close"].iloc[-1]
        volume = data["volume"].iloc[-1]
        sma_50 = data["close"].rolling(window=50).mean().iloc[-1]
        data_summary = f"Asset: {asset}\nLatest Close: {latest_close}\nVolume: {volume}\n50-day SMA: {sma_50}"

        # Construct prompt with data
        full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning."

        # Call LLM
        response = call_llm(full_prompt)

        # Parse response (assuming LLM returns JSON-like string)
        try:
            signal = json.loads(response)
            return {
                "action": signal.get("action", "hold"),
                "asset": asset,
                "confidence": float(signal.get("confidence", 0.5)),
                "reasoning": signal.get("reasoning", "")
            }
        except Exception:
            return {"action": "hold", "asset": asset, "confidence": 0.5, "reasoning": "Error parsing LLM response"}