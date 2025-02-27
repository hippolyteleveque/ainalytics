from ainalytics.database import engine
from sqlmodel import Session, select


from .models import PersistedChart
from ainalytics.external.database import exec_sql


def _get_format_data(query: str) -> dict:
    data = exec_sql(query)
    data = [{"name": pt[0], "value": pt[1]} for pt in data]
    return data


def get_charts(user_id: int) -> list[dict]:
    with Session(engine) as session:
        statement = select(PersistedChart).where(PersistedChart.user_id == user_id)
        objs = session.exec(statement).all()
    # TODO correct this, awful
    res = [
        {"id": obj.id, "type": obj.type, "data": _get_format_data(obj.query)}
        for obj in objs
    ]

    return res


def create_chart(query: str, chart_type: str, user_id: int) -> PersistedChart:
    obj = PersistedChart(type=chart_type, query=query, user_id=user_id)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        session.refresh(obj)
    return obj


def chart_delete(id: int):
    with Session(engine) as session:
        statement = select(PersistedChart).where(PersistedChart.id == id)
        obj = session.exec(statement).one_or_none()
        if obj:
            session.delete(obj)
            session.commit()
    return obj


def delete_chart_user(id: int, user_id: int):
    with Session(engine) as session:
        statement = (
            select(PersistedChart)
            .where(PersistedChart.id == id)
            .where(PersistedChart.user_id == user_id)
        )
        obj = session.exec(statement).one_or_none()
        if obj:
            session.delete(obj)
            session.commit()
    return obj
