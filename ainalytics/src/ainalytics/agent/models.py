from pydantic import BaseModel


class Chart(BaseModel):
    name: str
    description: str
