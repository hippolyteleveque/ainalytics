from fastapi import APIRouter

from ainalytics.auth.service import CurrentUser
from .schemas import ChartDisplay, ChartDisplayId, Message
from .service import run_agent, run_new_agent


router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/", response_model=ChartDisplayId)
@router.post("/new", response_model=ChartDisplayId)
def agent_new(request: Message, current_user: CurrentUser):
    state, data, obj_id = run_new_agent(request.message, user_id=current_user.id)
    return ChartDisplayId(type=state.chart, data=data, query=state.query, id=obj_id)


@router.post("/{id}", response_model=ChartDisplay)
def agent(request: Message, id: int):
    state, data = run_agent(
        request.message,
        id,
    )
    return ChartDisplay(type=state.chart, data=data, query=state.query)
