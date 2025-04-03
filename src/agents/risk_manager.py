from agents.base_agent import BaseAgent
from tools.utils import calculate_volatility

class RiskManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Risk Manager")

    def generate_signal(self, state):
        """
        Generates a risk-adjusted signal based on market data and volatility.
        Args:
            state (AgentState): The current state with market data
        Returns:
            AgentState: Updated state with risk-adjusted signals
        """
        data = state["data"]
        tickers = data["tickers"]
        price_data = data.get("price_data", {})
        signals = data.get("analyst_signals", {})

        for ticker in tickers:
            if ticker not in price_data:
                continue

            df = price_data[ticker]
            volatility = calculate_volatility(df).iloc[-1] if not df.empty else 0

            data_summary = f"Asset: {ticker}\nLatest Close: {df['close'].iloc[-1]}\n30-day Volatility: {volatility:.2f}%"
            full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning."

            response = call_llm(full_prompt)
            try:
                signal = json.loads(response)
                for analyst, analyst_signals in signals.items():
                    if ticker in analyst_signals:
                        # Adjust confidence based on volatility (simplified)
                        if volatility > 50:  # High volatility threshold
                            signal["confidence"] *= 0.8  # Reduce confidence in high volatility
                        signals[analyst][ticker] = signal
            except Exception:
                continue

        data["analyst_signals"] = signals
        return state
