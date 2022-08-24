from typing import Any
from pydantic import BaseModel


class KeyValueIn(BaseModel):
    key: str
    value: Any


class KeyValueOut(KeyValueIn):
    status: str = "ok"
