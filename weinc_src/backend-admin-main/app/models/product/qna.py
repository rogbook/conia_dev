from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List


class DataMember(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DataCustomer(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True


class DataStore(BaseModel):
    code: str
    title: str

    class Config:
        orm_mode = True


class DataProductPhoto(BaseModel):
    id: Optional[int]
    uri: Optional[str]

    class Config:
        orm_mode = True


class DataProduct(BaseModel):
    id: int
    code: str
    name: str
    photos: Optional[List[DataProductPhoto]]

    class Config:
        orm_mode = True


class AddProductQna(BaseModel):
    title: str
    contents: str
    customer_id: int
    a_member_id: Optional[int]
    product_qna_id: Optional[int]
    admin_id: Optional[int]
    status: Optional[str]
    store_code: Optional[str]
    secret: Optional[str]


class AddProductQnaAnswer(BaseModel):
    title: str
    contents: str
    a_member_id: int


class DataProductQna(BaseModel):
    id: int
    title: str
    contents: str
    product_id: Optional[int]
    status: str
    reg_date: datetime
    mod_date: datetime
    product_qna_id: Optional[int]
    admin_id: Optional[int]
    a_member_id: Optional[int]
    store_code: Optional[str]
    secret: str
    customer_id: Optional[int]

    customer: Optional[DataCustomer]
    a_member: Optional[DataMember]

    store: Optional[DataStore]
    product: Optional[DataProduct]
    answer: Optional["DataProductQna"]

    class Config:
        orm_mode = True


class ModQna(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    a_member_id: Optional[int]
    admin_id: Optional[int]
    status: Optional[str]
    store_code: Optional[str]
    secret: Optional[str]


class ListProductQna(BaseModel):
    total: int
    datas: List[DataProductQna]
