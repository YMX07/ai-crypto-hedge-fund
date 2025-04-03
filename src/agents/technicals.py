from src.agents.base_agent import BaseAgent
from src.tools.llm_interface import call_llm
import json

class TechnicalsAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Technicals Agent")

    def generate_signal(self, data, asset="BTC"):
        # Add technical indicators to data summary
        rsi = data["close"].pct_change().rolling(14).apply(lambda x: 100 - 100 / (
            1 + x[x > 0].mean() / abs(x[x < 0].mean()) if x[x < 0].mean() != 0 else float('inf')), raw=False).iloc[-1]
        macd = data["close"].ewm(span=12).mean().iloc[-1] - data["close"].ewm(span=26).mean().iloc[-1]
        data_summary = f"Asset: {asset}\nLatest Close: {data['close'].iloc[-1]}\nRSI: {rsi}\nMACD: {macd}"

        full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning."
        response = call_llm(full_prompt)

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