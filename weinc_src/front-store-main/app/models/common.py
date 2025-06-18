from enum import Enum
from typing import Union, Any

from pydantic import BaseModel


class Success(BaseModel):
    msg: str = "success"


class CreatedID(BaseModel):
    id: Union[int, str]


class CreatedURI(BaseModel):
    uri: str


class Exist(BaseModel):
    exist: bool


class EnumSearchType(str, Enum):
    all = 'all'
    top = 'top'


class LogMemberDataIn(BaseModel):
    member_id: int
    action: str
    msg: str
    writer: str


class LogOrderDataIn(BaseModel):
    order_id: Any
    action: str
    msg: str
    writer: str
