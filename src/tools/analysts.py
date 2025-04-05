ANALYST_ORDER = [
    ("Michael Saylor", "michael_saylor"),
    ("Vitalik Buterin", "vitalik_buterin"),
    ("Technicals Agent", "technicals"),
    ("Changpeng Zhao", "cz_binance"),
    ("Elon Musk", "elon_musk"),
    ("Brian Armstrong", "brian_armstrong"),
    ("Charles Hoskinson", "charles_hoskinson")
]

def get_analyst_nodes(selected_analysts=None):
    """
    Returns a dictionary mapping analyst keys to their node names and functions.
    Only initializes the selected analysts to avoid loading unused agents.
    Args:
        selected_analysts (list): List of analyst keys to initialize
    Returns:
        dict: Mapping of analyst keys to (node_name, node_function)
    """
    from agents.michael_saylor import MichaelSaylorAgent
    from agents.vitalik_buterin import VitalikButerinAgent
    from agents.technicals import TechnicalsAgent
    from agents.cz_binance import CZBinanceAgent
    from agents.elon_musk import ElonMuskAgent
    from agents.brian_armstrong import BrianArmstrongAgent
    from agents.charles_hoskinson import CharlesHoskinsonAgent

    all_analysts = {
        "michael_saylor": (MichaelSaylorAgent, "michael_saylor_agent"),
        "vitalik_buterin": (VitalikButerinAgent, "vitalik_buterin_agent"),
        "technicals": (TechnicalsAgent, "technicals_agent"),
        "cz_binance": (CZBinanceAgent, "cz_binance_agent"),
        "elon_musk": (ElonMuskAgent, "elon_musk_agent"),
        "brian_armstrong": (BrianArmstrongAgent, "brian_armstrong_agent"),
        "charles_hoskinson": (CharlesHoskinsonAgent, "charles_hoskinson_agent")
    }

    # Only initialize selected analysts
    if selected_analysts is None:
        selected_analysts = list(all_analysts.keys())

    analyst_nodes = {}
    for key in selected_analysts:
        if key in all_analysts:
            agent_class, node_name = all_analysts[key]
            agent_instance = agent_class()
            analyst_nodes[key] = (node_name, agent_instance.generate_signal)

    return analyst_nodes