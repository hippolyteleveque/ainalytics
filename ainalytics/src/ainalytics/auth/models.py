from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from ainalytics.database import AppTable

if TYPE_CHECKING:
    from ainalytics.charts.models import PersistedChart


class User(AppTable, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: Optional[str] = Field(default=None)

    charts: list["PersistedChart"] = Relationship(back_populates="user")
