from typing import Any, Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str

class NewUser(User):
    password: str

class UserInDB(User):
    hashed_password: str
    disabled: Optional[bool] = False

class KeyValueIn(BaseModel):
    key: str
    value: Any


class KeyValueOut(KeyValueIn):
    status: str = "ok"
