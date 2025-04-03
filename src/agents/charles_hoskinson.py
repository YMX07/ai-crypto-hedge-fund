from agents.base_agent import BaseAgent

class CharlesHoskinsonAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Charles Hoskinson")
        self.focus_asset = "ADA"  # Default to Cardano (ADA)

    def generate_signal(self, data, asset="ADA"):
        return super().generate_signal(data, asset=asset)