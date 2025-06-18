from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AddStore(BaseModel):
    code: str
    member_id: int
    title: str
    type: str
    domain: Optional[str]


class DataStore(BaseModel):
    code: str
    member_id: int
    title: str
    type: str
    domain: Optional[str]
    status: str
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class ModStore(BaseModel):
    title: Optional[str]
    type: Optional[str]
    domain: Optional[str]
    status: Optional[str]


class AddMemberStore(BaseModel):
    email: str
    password: str
    value: Optional[str]


class DataMemberStore(BaseModel):
    id: int
    store_code: str
    member_id: int
    confirm: str
    reg_date: datetime
    mod_date: datetime
    recommander_member_id: int

    class Config:
        orm_mode = True


class ModMemberStore(BaseModel):
    confirm: Optional[str]


class DataStoreTheme(BaseModel):
    id: int
    name: str
    description: str
    store_code: str
    pid: Optional[int]
    status: str
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class AddStoreTheme(BaseModel):
    name: str
    description: Optional[str]
    store_code: str
    pid: Optional[int]


class ModStoreTheme(BaseModel):
    name: Optional[str]
    description: Optional[str]


class SubStoreTheme(BaseModel):
    id: int
    name: str
    description: str
    store_code: str
    pid: Optional[int]
    status: str
    reg_date: datetime
    mod_date: datetime

    sub: Optional[List['SubStoreTheme']]


class DataStoreProduct(BaseModel):
    id: int
    view_yn: str

    class Config:
        orm_mode = True


class DataSimpleStore(BaseModel):
    code: str
    title: str

    class Config:
        orm_mode = True
