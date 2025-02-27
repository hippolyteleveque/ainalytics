from fastapi import APIRouter

from ainalytics.auth.service import CurrentUser
from .service import get_charts, create_chart, delete_chart_user
from .schemas import Charts, ChartIn, Chart

router = APIRouter(prefix="/charts", tags=["charts"])


@router.get("/", response_model=Charts)
def charts(current_user: CurrentUser):
    objs = get_charts(current_user.id)
    return Charts(charts=objs)


@router.post("/", response_model=Chart)
def post_chart(request: ChartIn, current_user: CurrentUser):
    obj = create_chart(request.query, request.type, current_user.id)
    return Chart(**obj.model_dump())


@router.delete("/{id}")
def delete_chart(id: int, current_user: CurrentUser):
    obj = delete_chart_user(id, current_user.id)
    return obj
