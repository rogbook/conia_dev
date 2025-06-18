from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List


class DataPhoto(BaseModel):
    id: int
    uri: str

    class Config:
        orm_mode = True


class DataMember(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DataCustomer(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DataStore(BaseModel):
    code: str
    title: str

    class Config:
        orm_mode = True


class DataFaqCate(BaseModel):
    id: int
    category: str
    sort: int

    class Config:
        orm_mode = True


class AddFaq(BaseModel):
    title: str
    contents: str
    category: Optional[str]
    status: Optional[str]
    target: str
    store_code: Optional[str]
    file: Optional[str]


class DataFaq(BaseModel):
    id: int
    title: str
    contents: str
    category: str
    status: str
    target: str
    file: Optional[str]
    store_code: Optional[str]
    reg_date: datetime
    mod_date: datetime

    store: Optional[DataStore]

    class Config:
        orm_mode = True


class ModFaq(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    category: Optional[str]
    status: Optional[str]
    target: Optional[str]
    store_code: Optional[str]
    file: Optional[str]


class AddNotice(BaseModel):
    title: str
    contents: str
    pin: Optional[str]
    sort: Optional[int]
    status: Optional[str]
    member_id: int
    target: str
    store_code: Optional[str]
    file: Optional[str]


class ModeNotice(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    pin: Optional[str]
    sort: Optional[int]
    status: Optional[str]
    target: Optional[str]
    store_code: Optional[str]
    file: Optional[str]


class DataNotice(BaseModel):
    id: int
    title: str
    contents: str
    pin: str
    sort: int
    status: str
    target: str
    file: Optional[str]
    store_code: Optional[str]
    reg_date: datetime
    mod_date: datetime
    member_id: int

    member: Optional[DataMember]
    store: Optional[DataStore]

    class Config:
        orm_mode = True


class AddQna(BaseModel):
    title: str
    contents: str
    q_member_id: int
    a_member_id: Optional[int]
    qna_id: Optional[int]
    admin_id: Optional[int]
    status: Optional[str]
    store_code: Optional[str]
    secret: Optional[str]


class ModQna(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    a_member_id: Optional[int]
    admin_id: Optional[int]
    status: Optional[str]
    store_code: Optional[str]
    secret: Optional[str]


class DataQna(BaseModel):
    id: int
    title: str
    contents: str
    q_member_id: int
    status: str
    reg_date: datetime
    mod_date: datetime
    qna_id: Optional[int]
    admin_id: Optional[int]
    a_member_id: Optional[int]
    store_code: Optional[str]
    secret: str

    q_member: Optional[DataMember]
    a_member: Optional[DataMember]

    store: Optional[DataStore]

    class Config:
        orm_mode = True


class AddQnaStore(BaseModel):
    title: str
    contents: str
    a_member_id: int
    qna_id: int
    admin_id: Optional[int]
    status: Optional[str]
    store_code: Optional[str]
    secret: Optional[str]


class DataQnaStore(BaseModel):
    id: int
    type: Optional[str]
    title: str
    contents: str
    customer_id: int
    status: Optional[str]
    reg_date: datetime
    mod_date: datetime
    qna_id: Optional[int]
    admin_id: Optional[int]
    a_member_id: Optional[int]
    store_code: Optional[str]
    secret: str

    customer: Optional[DataCustomer]
    a_member: Optional[DataMember]

    store: Optional[DataStore]
    answer: Optional["DataQnaStore"]

    class Config:
        orm_mode = True


class ListNotice(BaseModel):
    total: int
    datas: List[DataNotice]


class ListQna(BaseModel):
    total: int
    datas: List[DataQna]


class ListQnaStore(BaseModel):
    total: int
    datas: List[DataQnaStore]
