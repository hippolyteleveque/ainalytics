from typing import List, Any
from pydantic import BaseModel


class Chart(BaseModel):
    id: int
    query: str
    type: str


class ChartData(BaseModel):
    id: int
    type: str
    data: List[Any]


class Charts(BaseModel):
    charts: list[ChartData]


class ChartIn(BaseModel):
    query: str
    type: str
