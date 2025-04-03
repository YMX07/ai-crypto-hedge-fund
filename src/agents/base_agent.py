import json
from tools.llm_interface import call_llm

class BaseAgent:
    def __init__(self, name, prompt_file="config/prompts.json"):
        self.name = name
        with open(prompt_file, 'r') as f:
            self.prompt = json.load(f).get(name, "")

    def generate_signal(self, state, asset=None):
        """
        Generates a trading signal using LLM based on market data.
        Args:
            state (AgentState): The current state with market data
            asset (str): Crypto asset ticker (optional, defaults to agent's focus)
        Returns:
            AgentState: Updated state with the agent's signal
        """
        data = state["data"]
        price_data = data.get("price_data", {})
        tickers = data["tickers"] if asset is None else [asset]
        signals = data.get("analyst_signals", {})
        show_reasoning = state["metadata"].get("show_reasoning", False)
        model_name = state["metadata"].get("model_name", "gemini-1.5-flash")
        model_provider = state["metadata"].get("model_provider")
        pyd = state["metadata"].get("pydantic_model")

        if self.name not in signals:
            signals[self.name] = {}

        for ticker in tickers:
            if ticker not in price_data:
                continue

            df = price_data[ticker]
            if df.empty:
                continue

            latest_close = df["close"].iloc[-1]
            volume = df["volume"].iloc[-1]
            sma_50 = df["close"].rolling(window=50).mean().iloc[-1]
            data_summary = f"Asset: {ticker}\nLatest Close: {latest_close}\nVolume: {volume}\n50-day SMA: {sma_50}"


            full_prompt = f"{self.prompt}\n\nCurrent Market Data:\n{data_summary}\n\nProvide a trading signal (buy, sell, hold) with confidence (0-1) and brief reasoning."
            response = call_llm(full_prompt,model_name,model_provider,pyd)  # Pass the model argument

            try:
                signal = json.loads(response)
                signals[self.name][ticker] = signal
                if show_reasoning:
                    print(f"{self.name} Signal for {ticker}: {signal}")
            except Exception:
                signals[self.name][ticker] = {"action": "hold", "confidence": 0.5, "reasoning": "Error parsing LLM response"}

        data["analyst_signals"] = signals
        return state