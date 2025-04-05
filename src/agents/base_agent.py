import json
from tools.llm_interface import call_llm
from pydantic import BaseModel

class TradingSignal(BaseModel):
    action: str
    confidence: float
    reasoning: str

class BaseAgent:
    def __init__(self, name, prompt_file="config/prompts.json"):
        self.name = name
        with open(prompt_file, 'r') as f:
            self.prompt = json.load(f).get(name, "")

    def generate_signal(self, data, asset="BTC", model_name="gemini-2.0-flash", model_provider="Gemini"):
        """
        Generates a trading signal using LLM based on market data.
        Args:
            data (pd.DataFrame): OHLCV data
            asset (str): Crypto asset ticker
            model_name (str): Name of the LLM model
            model_provider (str): Provider of the LLM model
        Returns:
            dict: Signal with action, asset, confidence, and reasoning
        """
        if "close" not in data:
            return {"action": "hold", "asset": asset, "confidence": 0.0, "reasoning": "Missing 'close' column in data"}

        # Prepare data summary for LLM
        latest_close = data["close"].iloc[-1]
        volume = data["volume"].iloc[-1]
        sma_50 = data["close"].rolling(window=50).mean().iloc[-1]
        data_summary = f"Asset: {asset}\nLatest Close: {latest_close}\nVolume: {volume}\n50-day SMA: {sma_50}"

        # Construct prompt with data
        full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning."

        # Call LLM with the required arguments
        response = call_llm(full_prompt, model_name, model_provider, TradingSignal, agent_name=self.name)

        # Convert response to dict
        try:
            signal = response if isinstance(response, dict) else response.dict()
            return {
                "action": signal.get("action", "hold"),
                "asset": asset,
                "confidence": float(signal.get("confidence", 0.5)),
                "reasoning": signal.get("reasoning", "No reasoning provided")
            }
        except Exception as e:
            return {"action": "hold", "asset": asset, "confidence": 0.5, "reasoning": f"Error parsing LLM response: {e}"}