from typing import Any

from pydantic import BaseModel


class Message(BaseModel):
    message: str

class ChartDisplay(BaseModel):
    query: str
    type: str
    data: list[Any]
