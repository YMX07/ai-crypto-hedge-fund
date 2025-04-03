from src.agents.base_agent import BaseAgent

class BrianArmstrongAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Brian Armstrong")
        self.focus_asset = "BTC"  # Default to BTC as a "blue-chip" crypto

    def generate_signal(self, data, asset="BTC"):
        return super().generate_signal(data, asset=asset)