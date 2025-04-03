from dataclasses import dataclass
from typing import Dict, List, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    data: Dict
    metadata: Dict