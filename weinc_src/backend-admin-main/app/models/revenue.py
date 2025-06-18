from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Optional, List

from app.models.common import ListData


class DataOfflineRevenue(BaseModel):
    id: int = Field(title="아이디")
    code: str = Field(title="타입")
    amount: Decimal = Field(title="금액")
    sales_date: datetime = Field(title="매출일")
    status: str = Field(title="상태")
    reg_date: datetime = Field(title="등록일")
    mod_date: datetime = Field(title="수정일")
    member_id: Optional[int] = Field(title="등록자 IDX")

    class Config:
        orm_mode = True


class DataRevenue(BaseModel):
    date: date
    total_sales: int

    class Config:
        orm_mode = True


class DataMonth(BaseModel):
    online: Optional[List[DataRevenue]]
    offline: Optional[List[DataRevenue]]

    class Config:
        orm_mode = True


class ListOfflineRevenue(ListData):
    total_sum: Optional[int]
    data: List[DataOfflineRevenue]
