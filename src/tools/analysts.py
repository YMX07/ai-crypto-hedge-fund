ANALYST_ORDER = [
    ("Michael Saylor", "michael_saylor"),
    ("Vitalik Buterin", "vitalik_buterin"),
    ("Technicals Agent", "technicals"),
    ("Changpeng Zhao", "cz_binance"),
    ("Elon Musk", "elon_musk"),
    ("Brian Armstrong", "brian_armstrong"),
    ("Charles Hoskinson", "charles_hoskinson")
]

def get_analyst_nodes():
    """
    Returns a dictionary mapping analyst keys to their node names and functions.
    """
    from agents.michael_saylor import MichaelSaylorAgent
    from agents.vitalik_buterin import VitalikButerinAgent
    from agents.technicals import TechnicalsAgent
    from agents.cz_binance import CZBinanceAgent
    from agents.elon_musk import ElonMuskAgent
    from agents.brian_armstrong import BrianArmstrongAgent
    from agents.charles_hoskinson import CharlesHoskinsonAgent

    return {
        "michael_saylor": ("michael_saylor_agent", MichaelSaylorAgent().generate_signal),
        "vitalik_buterin": ("vitalik_buterin_agent", VitalikButerinAgent().generate_signal),
        "technicals": ("technicals_agent", TechnicalsAgent().generate_signal),
        "cz_binance": ("cz_binance_agent", CZBinanceAgent().generate_signal),
        "elon_musk": ("elon_musk_agent", ElonMuskAgent().generate_signal),
        "brian_armstrong": ("brian_armstrong_agent", BrianArmstrongAgent().generate_signal),
        "charles_hoskinson": ("charles_hoskinson_agent", CharlesHoskinsonAgent().generate_signal)
    }