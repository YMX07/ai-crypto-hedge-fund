from agents.base_agent import BaseAgent
from tools.utils import calculate_volatility
from tools.llm_interface import call_llm
from pydantic import BaseModel

class TradingSignal(BaseModel):
    action: str
    confidence: float
    reasoning: str

class RiskManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Risk Manager")

    def generate_signal(self, state):
        data = state["data"]
        tickers = data["tickers"]
        price_data = data.get("price_data", {})
        signals = data.get("analyst_signals", {})
        model_name = state["metadata"].get("model_name", "gemini-2.0-flash")
        model_provider = state["metadata"].get("model_provider", "Gemini")

        for ticker in tickers:
            if ticker not in price_data:
                continue

            df = price_data[ticker]
            volatility = calculate_volatility(df).iloc[-1] if not df.empty else 0

            data_summary = f"Asset: {ticker}\nLatest Close: {df['close'].iloc[-1]}\n30-day Volatility: {volatility:.2f}%"
            full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning."

            response = call_llm(full_prompt, model_name, model_provider, TradingSignal)
            try:
                signal = response if isinstance(response, dict) else response.dict()
                # Store the signal under "Risk Manager" without overwriting other analysts' signals
                signals.setdefault("Risk Manager", {})[ticker] = signal

                # Adjust confidence of other analysts' signals based on volatility
                for analyst, analyst_signals in signals.items():
                    if analyst == "Risk Manager":  # Skip Risk Manager itself
                        continue
                    if ticker in analyst_signals:
                        if volatility > 50:  # High volatility threshold
                            analyst_signals[ticker]["confidence"] *= 0.8  # Reduce confidence in high volatility
            except Exception:
                continue

        data["analyst_signals"] = signals
        return state