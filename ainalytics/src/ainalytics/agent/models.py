from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel


class Chart(BaseModel):
    name: str
    description: str


class FlowStage(Enum):
    GET_DATA = "get"
    TRANSFORM_DATA = "transform"
    DISPLAY_DATA = "display"
    DONE = "done"


class FlowState(BaseModel):
    stage: FlowStage = FlowStage.GET_DATA
    messages: list[dict] = []
    data: Optional[Any] = None
    query: Optional[str] = None
    chart: Optional[str] = None
