from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel
from openai import OpenAI

from ainalytics.config import settings
from ainalytics.agent.prompts import GET_DATA_PROMPT, GET_DISPLAY_PROMPT, GET_DISPLAY_USR_PROMPT
from ainalytics.agent.helpers import extract_raw_code
from ainalytics.agent.database import exec_sql
from ainalytics.agent.models import Chart


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


class Flow:

    def __init__(
        self,
        database_desc: str,
        chart_desc: list[Chart],
        state: FlowState | None = None,
    ):
        self.database_desc = database_desc
        self.chart_desc = chart_desc
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        if state is None:
            self.state = FlowState()
        else:
            self.state = state

    def _get_prompt(self) -> str:
        if self.state.stage == FlowStage.GET_DATA:
            return GET_DATA_PROMPT.render(database=self.database_desc)
        elif self.state.stage == FlowStage.DISPLAY_DATA:
            return GET_DISPLAY_PROMPT.render(database=self.database_desc)

    def _get_sql_query(
        self,
    ) -> str:  # we could have a special type that validate query there
        system = self._get_prompt()
        response = self.client.chat.completions.create(
            model=settings.MODEL_ID,
            messages=[{"role": "system", "content": system}] + self.state.messages,
            temperature=0,
        )
        res = response.choices[0].message.content
        res = extract_raw_code(res)
        return res

    def _exec_sql(self, statement: str) -> list[Any]:
        iterator = exec_sql(statement)
        return list(iterator)

    def _get_chart(self) -> str:
        data_sample = self.state.data[0]
        system = GET_DISPLAY_PROMPT
        usr = GET_DISPLAY_USR_PROMPT.render(
            data_sample=data_sample, charts=self.chart_desc
        )
        response = self.client.chat.completions.create(
            model=settings.MODEL_ID,
            messages=[{"role": "system", "content": system}]
            + self.state.messages
            + [{"role": "user", "content": usr}],
            temperature=0,
        )
        res = response.choices[0].message.content
        return res

    def step(self):
        if self.state.stage == FlowStage.GET_DATA:
            query = self._get_sql_query()
            self.state.query = query
            self.state.messages.append({"role": "assistant", "content": query})
            rows = self._exec_sql(query)
            self.state.data = rows
            self.state.stage = FlowStage.DISPLAY_DATA
        elif self.state.stage == FlowStage.DISPLAY_DATA:
            chart = self._get_chart()
            # TODO validate chart
            self.state.chart = chart
            self.state.stage = FlowStage.DONE

    def run(self, prompt: str) -> FlowState:
        self.state.messages.append({"role": "user", "content": prompt})
        while self.state.stage != FlowStage.DONE:
            self.step()
        return self.state
