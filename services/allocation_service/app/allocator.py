import math
from services.shared.models import Unit


EVENT_TO_UNIT = {
    "fire": "fire_truck",
    "medical": "ambulance",
    "crime": "police",
    "flood": "fire_truck",
    "earthquake": "ambulance",
}


def required_unit_type(event_type: str) -> str | None:
    return EVENT_TO_UNIT.get(event_type)


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def choose_best_unit(units: list[Unit], event_x: float, event_y: float):
    if not units:
        return None

    best_unit = None
    best_distance = float("inf")

    for unit in units:
        d = distance(unit.location_x, unit.location_y, event_x, event_y)
        if d < best_distance:
            best_distance = d
            best_unit = unit

    return best_unit