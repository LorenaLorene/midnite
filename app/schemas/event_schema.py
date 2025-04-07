from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    withdraw = "withdraw"
    deposit = "deposit"


class EventCode(int, Enum):
    WITHDRAW_OVER_100 = 1100
    CONSECUTIVE_3_WITHDRAWS = 30
    CONSECUTIVE_3_INCREASING_DEPOSITS = 300
    ACCUMULATIVE_DEPOSITS_200_IN_30_SECONDS = 123


class Event(BaseModel):
    type: EventType
    amount: str
    user_id: int
    t: int


class EventResponse(BaseModel):
    alert: bool
    alert_codes: list[EventCode]
    user_id: int
