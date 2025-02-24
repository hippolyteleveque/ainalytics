from pydantic import BaseModel

class Chart(BaseModel):
    id: int
    query: str
    type: str

class Charts(BaseModel):
    charts: list[Chart]

class ChartIn(BaseModel):
    query: str
    type: str
