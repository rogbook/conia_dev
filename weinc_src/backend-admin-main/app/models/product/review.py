from datetime import datetime
from decimal import Decimal

from pydantic.utils import GetterDict
from pydantic import BaseModel
from typing import Optional, List, Any


class UserGetter(GetterDict):
    def get(self, key: str, default: Any) -> Any:
        if key == "photos":
            # Use self._obj, which is the orm model to build the list of apps_ids and return that
            photos = super().get(key, default)
            return photos[0]
        return super().get(key, default)


class DataCustomer(BaseModel):
    id: int
    name: Optional[str]

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


class SimplePhoto(BaseModel):
    id: Optional[int]
    uri: Optional[str]

    class Config:
        orm_mode = True


class DataReview(BaseModel):
    id: int
    product_id: str
    title: Optional[str]
    contents: str
    rating: Optional[Decimal]
    status: str
    reg_date: datetime
    mod_date: datetime
    order_info: Optional[str]
    order_product_id: int
    customer_id: int

    customer: Optional[DataCustomer]
    product: Optional[SimpleProduct]
    photos: Optional[List[SimplePhoto]]

    class Config:
        orm_mode = True


class ListDataReview(BaseModel):
    total: int
    datas: List[DataReview]
