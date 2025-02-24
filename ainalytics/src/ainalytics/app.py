from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .schemas import ChartDisplay, ChartDisplayId, Message
from .service import run_new_agent, run_agent

app = FastAPI()


def configure_cors():
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


configure_cors()


@app.post("/agent", response_model=ChartDisplayId)
@app.post("/agent/new", response_model=ChartDisplayId)
def agent_new(request: Message):
    state, data, obj_id = run_new_agent(request.message)
    return ChartDisplayId(type=state.chart, data=data, query=state.query, id=obj_id)


@app.post("/agent/{id}", response_model=ChartDisplay)
def agent(request: Message, id: int):
    state, data = run_agent(request.message, id)
    return ChartDisplay(type=state.chart, data=data, query=state.query)
