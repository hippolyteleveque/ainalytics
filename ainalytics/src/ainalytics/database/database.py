from sqlmodel import SQLModel, create_engine, MetaData

from ainalytics.config import settings


metadata = MetaData()


class AppTable(SQLModel, table=False):
    metadata = metadata


engine = create_engine(settings.APP_DB_URL)





__all__ = ["AppTable", "engine"]
