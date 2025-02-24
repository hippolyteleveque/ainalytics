from fastapi import APIRouter

from .service import get_charts, create_chart, chart_delete
from .schemas import Charts, ChartIn, Chart

router = APIRouter(prefix="/charts", tags=["charts"])


@router.get("/", response_model=Charts)
def charts():
    objs = get_charts()
    return Charts(charts=objs)


@router.post("/")
def post_chart(request: ChartIn):
    obj = create_chart(request.query, request.type)
    return Chart(**obj.model_dump())


@router.delete("/{id}")
def delete_chart(id: int):
    obj = chart_delete(id)
    return obj
