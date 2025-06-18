from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class SimpleMember(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class SimpleStore(BaseModel):
    code: str
    title: str

    class Config:
        orm_mode = True


class DataProductPhoto(BaseModel):
    id: Optional[int]
    uri: Optional[str]

    class Config:
        orm_mode = True


class SimpleProduct(BaseModel):
    id: int
    code: str
    name: str
    photos: Optional[List[DataProductPhoto]]

    class Config:
        orm_mode = True


class DataProductRequest(BaseModel):
    id: int
    member_id: int
    store_code: str
    title: str
    memo: Optional[str]
    status: str
    reg_date: datetime
    mod_date: datetime
    manager: Optional[int]

    member: SimpleMember
    store: Optional[SimpleStore]
    manager_member: Optional[SimpleMember]

    class Config:
        orm_mode = True


class DetailProductRequest(BaseModel):
    id: int
    member_id: int
    store_code: str
    title: str
    memo: Optional[str]
    status: str
    reg_date: datetime
    mod_date: datetime
    manager: Optional[int]

    member: SimpleMember
    products: List[SimpleProduct]
    store: Optional[SimpleStore]
    manager_member: Optional[SimpleMember]

    class Config:
        orm_mode = True


class AddProductRequest(BaseModel):
    store_code: str
    title: str = Field(title="상품명 외 몇건 형식")
    memo: Optional[str]
    product_ids: List[int]


class ModProductRequest(BaseModel):
    status: Optional[str]


class ListProductRequest(BaseModel):
    total: int
    datas: List[DataProductRequest]
