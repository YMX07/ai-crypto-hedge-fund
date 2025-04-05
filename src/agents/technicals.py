from agents.base_agent import BaseAgent
from tools.llm_interface import call_llm
from pydantic import BaseModel

class TradingSignal(BaseModel):
    action: str
    confidence: float
    reasoning: str

class TechnicalsAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Technicals")

    def generate_signal(self, state):
        """
        Generates a technical trading signal based on RSI and market data.
        Args:
            state (dict): The state containing data, tickers, and signals.
        Returns:
            dict: Updated state with the generated signal.
        """
        data = state["data"]
        tickers = data["tickers"]
        price_data = data.get("price_data", {})
        signals = data.get("analyst_signals", {})
        model_name = state["metadata"].get("model_name", "gemini-2.0-flash")
        model_provider = state["metadata"].get("model_provider", "Gemini")

        signals_generated = False
        for ticker in tickers:
            if ticker not in price_data or price_data[ticker].empty:
                continue

            df = price_data[ticker]
            if "close" not in df.columns:
                continue

            # Calculate RSI
            delta = df["close"].pct_change()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1] if not rs.isna().all() else 50  # Default to 50 if NaN

            # Prepare data summary for LLM
            data_summary = f"Asset: {ticker}\nLatest Close: {df['close'].iloc[-1]}\nRSI (14-day): {rsi:.2f}"
            full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning in JSON format:\n{{\"action\": \"buy/sell/hold\", \"confidence\": 0-1, \"reasoning\": \"your reasoning\"}}"

            # Call LLM
            response = call_llm(full_prompt, model_name, model_provider, TradingSignal, agent_name=self.name)
            try:
                signal = response if isinstance(response, dict) else response.dict()
                signals.setdefault("Technicals", {})[ticker] = signal
                signals_generated = True
            except Exception:
                signals.setdefault("Technicals", {})[ticker] = {
                    "action": "hold",
                    "confidence": 0.5,
                    "reasoning": "Error processing technical signal"
                }
                signals_generated = True

        if not signals_generated:
            pass  # Silently skip if no signals are generated

        data["analyst_signals"] = signals
        return state