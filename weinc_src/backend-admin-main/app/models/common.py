from enum import Enum
from datetime import datetime, time

from pydantic import BaseModel
from typing import Optional, Any, List, Union


class Success(BaseModel):
    msg: str = "success"


class SuccessCount(Success):
    count: int = 0


class SuccessFail(Success):
    success_count: int = 0
    fail_list: List[List[str]] = []


class CreatedID(BaseModel):
    id: int


class CreatedURI(BaseModel):
    uri: str


class Exist(BaseModel):
    exist: bool


class EnumSearchType(str, Enum):
    all = 'all'
    top = 'top'


class DataLog(BaseModel):
    action: str
    msg: str
    writer: str
    reg_date: datetime

    class Config:
        orm_mode = True


class ListLog(BaseModel):
    total: int
    datas: List[DataLog]


class LogMemberDataIn(BaseModel):
    member_id: int
    action: str
    msg: str
    writer: str


class LogCustomerDataIn(BaseModel):
    customer_id: int
    action: str
    msg: str
    writer: str


class LogStoreDataIn(BaseModel):
    store_code: str
    action: str
    msg: str
    writer: str


class LogProductDataIn(BaseModel):
    product_id: int
    action: str
    msg: str
    writer: str


class LogOrderDataIn(BaseModel):
    order_id: Any
    action: str
    msg: str
    writer: str


class LogCommissionDataIn(BaseModel):
    member_id: int
    action: str
    msg: str
    writer: str


class ListData(BaseModel):
    total: int


def date_validator(date):
    if not isinstance(date, (datetime, time)) and date != "_null_":
        raise ValueError("invalid datetime format")
    return date
