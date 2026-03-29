from enum import Enum


class EventType(str, Enum):
    FIRE = "fire"
    MEDICAL = "medical"
    CRIME = "crime"
    FLOOD = "flood"
    EARTHQUAKE = "earthquake"


class EventStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    RESOLVED = "resolved"
    FAILED = "failed"


class UnitType(str, Enum):
    AMBULANCE = "ambulance"
    FIRE_TRUCK = "fire_truck"
    POLICE = "police"


class UnitStatus(str, Enum):
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"


class DispatchStatus(str, Enum):
    REQUESTED = "requested"
    ACKNOWLEDGED = "acknowledged"
    TIMED_OUT = "timed_out"
    REASSIGNED = "reassigned"
    COMPLETED = "completed"
