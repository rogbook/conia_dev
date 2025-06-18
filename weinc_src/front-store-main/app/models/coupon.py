from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List


class DataCouponTarget(BaseModel):
    member_id: Optional[str]
    product_id: Optional[str]

    class Config:
        orm_mode = True


class DataCouponGroup(BaseModel):
    image: Optional[str]
    coupon_target: Optional[List[DataCouponTarget]]

    class Config:
        orm_mode = True


class DataCoupon(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    reg_date: Optional[datetime]
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
    status: Optional[str]
    coupon_group: Optional[DataCouponGroup]

    target_pa_str: Optional[str]
    target_prd_str: Optional[str]
    able_prd_list: Optional[List[str]] = []
    able_prd_str: Optional[List[str]]

    class Config:
        orm_mode = True
