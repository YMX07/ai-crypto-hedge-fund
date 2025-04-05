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

        for ticker in tickers:
            if ticker not in price_data or price_data[ticker].empty:
                continue

            df = price_data[ticker]
            if "close" not in df.columns:
                continue

            # Générer le signal en utilisant la méthode de BaseAgent
            # La 50-day SMA est déjà calculée dans BaseAgent et incluse dans le prompt
            signal = super().generate_signal(df, asset=ticker, model_name=model_name, model_provider=model_provider)
            signals.setdefault("Technicals", {})[ticker] = signal

        data["analyst_signals"] = signals
        return state