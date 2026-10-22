import os

from .util import get_time

from typing import Dict, Tuple

# 4 hours
START_RUNTIME_SECONDS = int(os.getenv("START_RUNTIME_SECONDS", "14400"))
# 2 hours
EXTEND_RUNTIME_SECONDS = int(os.getenv("EXTEND_RUNTIME_SECONDS", "7200"))


class RuntimeTracker:
    """An in-memory database."""

    def __init__(self):
        self.__times: Dict[str, Tuple[int, int]] = {}

    def __contains__(self, name: str) -> bool:
        """Checks if a service is in the tracker."""
        return name in self.__times

    def __getitem__(self, name: str) -> Tuple[int, int]:
        """Gets the start time and end time of a service."""
        return self.__times[name]

    def get(self, name: str) -> Tuple[int, int]:
        """Same as [], but ensures the service exists."""
        if name not in self.__times:
            time = get_time()
            self.__times[name] = (time, time + START_RUNTIME_SECONDS)
        return self.__times[name]

    def start(self, name: str) -> None:
        """Start a service."""
        self.__extend(name, START_RUNTIME_SECONDS)

    def extend(self, name: str) -> None:
        """Extend a service's runtime."""
        self.__extend(name, EXTEND_RUNTIME_SECONDS)

    def end(self, name: str) -> None:
        """End a service."""
        if name in self.__times:
            del self.__times[name]

    def __extend(self, name: str, seconds: int) -> None:
        """Extends a service's runtime, if now + seconds is greater than
        the current end time."""
        start, end = self.get(name)
        self.__times[name] = (start, max(end, get_time() + seconds))
