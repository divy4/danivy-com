from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import fastapi
import logging
import os
from zoneinfo import ZoneInfo

from typing import List


from .k8s import list_deployments, scale_deployment
from .models import Game
from .runtime_tracker import RuntimeTracker
from .util import get_time, to_human_time

CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "60"))


_logger = logging.getLogger(__name__)
_scheduler = AsyncIOScheduler(timezone=ZoneInfo("UTC"))


_tracker: RuntimeTracker = RuntimeTracker()


async def shutdown_games():
    """Shuts down any games running for a long time."""
    deployments = await list_deployments()
    width = max(len(x.metadata.name) for x in deployments)

    _logger.info("Checking game shutdown times...")
    for deployment in deployments:
        name = deployment.metadata.name
        # Remove deployments that aren't active anymore
        if not deployment.enabled():
            _logger.info(f"{name:<{width}} - inactive")
            _tracker.end(name)
            continue

        # Compute all the times
        start, end = _tracker.get(name)
        current = get_time()
        run = current - start
        left = end - current
        _logger.info(
            f"{name:<{width}} - Running for {to_human_time(run)}, {to_human_time(left)} left"
        )

        # Stop deployment
        if current >= end:
            await scale_deployment(name=name, replicas=0)


@asynccontextmanager
async def lifespan(_: fastapi.FastAPI):
    """Sets up jobs to execute at regular intervals during the lifespan of the app."""
    _scheduler.add_job(shutdown_games, "interval", seconds=CHECK_INTERVAL_SECONDS)
    logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)
    _scheduler.start()
    try:
        yield
    finally:
        _scheduler.shutdown(wait=False)


app = fastapi.FastAPI(lifespan=lifespan)


@app.get("/api/v1/games")
async def list_games() -> List[Game]:
    """List all games."""
    _logger.info("Listing games...")
    games = []
    for d in await list_deployments():
        start, end = None, None
        if d.enabled():
            start, end = _tracker.get(d.metadata.name)
        games.append(Game.from_deployment(d, start, end))
    _logger.info(f"{len(games)} games found.")
    return games


@app.post("/api/v1/games/{name}/start")
async def start_game(name: str) -> None:
    """Start a game server."""
    _logger.info(f"Starting {name}...")
    # Started >> more time, already running >> less time
    if await scale_deployment(name, 1):
        _tracker.start(name)
    else:
        _tracker.extend(name)
