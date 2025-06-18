from datetime import datetime, time
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel
from typing import Optional, List

from app.models.common import ListData
from app.models.user.member import DataSimpleMember
from app.models.product.product import DataSimpleProduct
from app.models.store import DataSimpleStore


class DataCustomer(BaseModel):
    id: int
    email: str
    name: Optional[str]

    class Config:
        orm_mode = True


class DataCouponTarget(BaseModel):
    id: Optional[int]
    member_id: Optional[int]
    product_id: Optional[int]

    member: Optional[DataSimpleMember]
    product: Optional[DataSimpleProduct]

    class Config:
        orm_mode = True


class DataCouponPublishTarget(BaseModel):
    id: int
    store_code: str

    store: Optional[DataSimpleStore]

    class Config:
        orm_mode = True


class AddCouponTarget(BaseModel):
    member_id: Optional[int]
    product_id: Optional[int]


class AddCouponGroup(BaseModel):
    name: str
    description: str
    expire_days: Optional[int]
    begin_date: Optional[datetime]
    end_date: Optional[datetime]
    begin_time: Optional[time]
    end_time: Optional[time]
    amount: Optional[Decimal]
    percent: Optional[int]
    store_code: Optional[str]
    brand_id: Optional[int]
    category_id: Optional[int]
    product_id: Optional[int]
    min_price: Optional[int]
    max_price: Optional[int]
    issuer: int
    publish_limit: Optional[int]
    publish_begin_date: Optional[datetime]
    publish_end_date: Optional[datetime]
    target: str
    type: str
    image: Optional[str]
    product_id: Optional[str]

    coupon_target: Optional[List[AddCouponTarget]]


class DataCouponGroup(BaseModel):
    id: int
    name: str
    description: str
    status: str
    reg_date: datetime
    mod_date: datetime
    expire_days: Optional[int]
    begin_date: Optional[datetime]
    end_date: Optional[datetime]
    begin_time: Optional[time]
    end_time: Optional[time]
    amount: Optional[Decimal]
    percent: Optional[int]
    store_code: Optional[str]
    brand_id: Optional[int]
    category_id: Optional[int]
    product_id: Optional[int]
    min_price: Optional[int]
    max_price: Optional[int]
    issuer: int
    auto: Optional[str]
    publish_limit: Optional[int]
    publish_begin_date: Optional[datetime]
    publish_end_date: Optional[datetime]
    target: Optional[str]
    type: Optional[str]
    image: Optional[str]
    product_id: Optional[str]

    publish_cnt: int = 0

    product: Optional[DataSimpleProduct]
    coupon_target: Optional[List[DataCouponTarget]]
    coupon_publish_target: Optional[List[DataCouponPublishTarget]]

    class Config:
        orm_mode = True


class CouponPublishType(str, Enum):
    all = 'all'
    store = 'store'
    customer = 'customer'


class CouponPublish(BaseModel):
    type: CouponPublishType
    store_code: Optional[str]
    customer_ids: Optional[List[int]]


class ListCouponGroup(ListData):
    datas: List[DataCouponGroup]


class DataCoupon(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    reg_date: datetime
    use_date: Optional[datetime]
    begin_date: Optional[datetime]
    end_date: Optional[datetime]
    use_yn: str
    amount: Optional[Decimal]
    percent: Optional[Decimal]
    min_price: Optional[Decimal]
    max_price: Optional[Decimal]
    issuer: int
    coupon_group_id: int
    target: Optional[str]
    type: Optional[str]
    customer_id: int
    product_id: Optional[int]

    customer: DataCustomer

    class Config:
        orm_mode = True


class ListCoupon(ListData):
    datas: List[DataCoupon]
