from ainalytics.agent.models import *  # noqa: F403
from ainalytics.charts.models import *  # noqa: F403

from .database import metadata, engine


def init_db():
    metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
