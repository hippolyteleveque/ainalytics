from enum import Enum
from typing import Optional, Any, List

from pydantic import BaseModel
from sqlmodel import Field, Relationship

from ainalytics.database import AppTable
from ainalytics.external.database import exec_sql


class Chart(BaseModel):
    name: str
    description: str


class FlowStage(Enum):
    GET_DATA = "get"
    TRANSFORM_DATA = "transform"
    DISPLAY_DATA = "display"
    DONE = "done"


class FlowState(BaseModel):
    stage: FlowStage = FlowStage.GET_DATA
    messages: list[dict] = []
    data: Optional[Any] = None
    query: Optional[str] = None
    chart: Optional[str] = None


class PersistedFlowState(AppTable, table=True):
    __tablename__ = "flowstates"

    id: Optional[int] = Field(default=None, primary_key=True)
    stage: str
    query: Optional[str]
    chart: Optional[str]
    user_id: int = Field(foreign_key="users.id")

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
    def from_flow_state(cls, state: FlowState, user_id: int) -> "PersistedFlowState":
        dump = state.model_dump()
        _ = dump.pop("data")
        messages = dump.pop("messages")
        stage = dump.pop("stage").value
        obj = cls(
            **dump,
            user_id=user_id,
            stage=stage,
            messages=[
                PersistedMessage(role=message["role"], content=message["content"])
                for message in messages
            ]
        )
        return obj


class PersistedMessage(AppTable, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    content: str
    state_id: int = Field(foreign_key="flowstates.id")

    flowstate: PersistedFlowState = Relationship(back_populates="messages")
