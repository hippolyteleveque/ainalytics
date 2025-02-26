from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from ainalytics.database import AppTable

if TYPE_CHECKING:
    from ainalytics.auth.models import User


class PersistedChart(AppTable, table=True):
    __tablename__ = "charts"

    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    query: str
    user_id: int = Field(foreign_key="users.id")

    user: "User" = Relationship(back_populates="charts")
