from typing import Optional

from sqlmodel import Field

from ainalytics.database import AppTable


class PersistedChart(AppTable, table=True):
    __tablename__ = "charts"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    query: str
