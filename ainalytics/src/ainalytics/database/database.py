from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, create_engine, MetaData

from ainalytics.config import settings
from ainalytics.agent.models import FlowState, FlowStage

from ainalytics.external.database import exec_sql

metadata = MetaData()


class PersistedFlowState(SQLModel, table=True):
    __tablename__ = "flowstates"
    metadata = metadata

    id: Optional[int] = Field(default=None, primary_key=True)
    stage: str
    query: Optional[str]
    chart: Optional[str]

    messages: List["PersistedMessage"] = Relationship(back_populates="flowstate")

    def to_flow_state(self) -> FlowState:
        data = list(exec_sql(self.query)) if self.query else None
        messages = [
            {"role": message.role, "content": message.content}
            for message in self.messages
        ]
        state = FlowState(
            stage=FlowStage(self.stage),
            messages=messages,
            data=data,
            chart=self.chart,
            query=self.query,
        )
        return state

    def update(self, state: FlowState):
        self.chart = state.chart
        self.stage = state.stage.value
        new_messages = state.messages[len(self.messages) :]
        self.messages += [
            PersistedMessage(role=message["role"], content=message["content"])
            for message in new_messages
        ]

    @classmethod
    def from_flow_state(cls, state: FlowState) -> "PersistedFlowState":
        dump = state.model_dump()
        _ = dump.pop("data")
        messages = dump.pop("messages")
        stage = dump.pop("stage").value
        obj = cls(
            **dump,
            stage=stage,
            messages=[
                PersistedMessage(role=message["role"], content=message["content"])
                for message in messages
            ]
        )
        return obj


class PersistedMessage(SQLModel, table=True):
    __tablename__ = "messages"
    metadata = metadata

    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    content: str
    state_id: int = Field(foreign_key="flowstates.id")

    flowstate: PersistedFlowState = Relationship(back_populates="messages")


engine = create_engine(settings.APP_DB_URL)


def create_db_and_tables(engine):
    metadata.create_all(engine)


__all__ = ["PersistedFlowState", "PersistedMessage", "engine"]

if __name__ == "__main__":
    create_db_and_tables(engine)
