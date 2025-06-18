from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.product.product import DataSimpleProduct
from app.models.store import DataSimpleStore


class DataSimpleMember(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class AddCatalog(BaseModel):
    name: str
    description: str
    member_id: int


class DataCatalog(BaseModel):
    id: int
    name: str
    description: str
    member_id: int
    open: str
    status: str
    reg_date: datetime
    mod_date: datetime

    member: DataSimpleMember

    class Config:
        orm_mode = True


class ModCatalog(BaseModel):
    name: Optional[str]
    description: Optional[str]
    open: Optional[str]
    status: Optional[str]


class DataCatalogStore(BaseModel):
    id: int

    store: Optional[DataSimpleStore]

    class Config:
        orm_mode = True
        

class DataCatalogProduct(BaseModel):
    id: int
    variation: int

    product: Optional[DataSimpleProduct]

    class Config:
        orm_mode = True


class ListCatalog(BaseModel):
    total: int
    datas: List[DataCatalog]


class ListCatalogStore(BaseModel):
    total: int
    datas: List[DataCatalogStore]


class ListCatalogProduct(BaseModel):
    total: int
    datas: List[DataCatalogProduct]