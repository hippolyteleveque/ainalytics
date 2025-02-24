from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from ainalytics.agent.router import router as agent_router
from ainalytics.charts.router import router as charts_router

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


app.include_router(agent_router)
app.include_router(charts_router)
