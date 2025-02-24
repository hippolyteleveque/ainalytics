from ainalytics.database import engine
from sqlmodel import Session, select

from .models import PersistedChart


def get_charts():
    with Session(engine) as session:
        statement = select(PersistedChart)
        objs = session.exec(statement).all()
    return list(objs)

def create_chart(query: str, chart_type: str):
    obj = PersistedChart(type=chart_type, query=query)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj
