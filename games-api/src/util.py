import time


def get_time() -> int:
    """Returns the epoch time."""
    return int(time.time())


def to_human_time(total_seconds: int) -> str:
    """Converts integer time to human-readable time."""
    if total_seconds <= 0:
        return "0s"

    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    hours = total_minutes // 60

    ret = ""
    if hours > 0:
        ret += f"{hours}h"
    if minutes > 0:
        ret += f"{minutes}m"
    if seconds > 0:
        ret += f"{seconds}s"
    return ret
