from fastapi import APIRouter

from .service import get_charts, create_chart
from .schemas import Charts, ChartIn, Chart

router = APIRouter(prefix="/charts", tags=["charts"])


@router.get("/", response_model=Charts)
def charts():
    objs = get_charts()
    return Charts(charts=objs)


@router.post("/")
def post_chart(request: ChartIn) -> Chart:
    obj = create_chart(request.query, request.type)
    return Chart(**obj.model_dump())
