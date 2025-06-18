from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddCart(BaseModel):
    product_option_id: int
    count: int
    force: Optional[str]


class DataCart(BaseModel):
    id: int
    product_option_id: int
    count: int
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class ModCart(BaseModel):
    count: Optional[int]
    checked: Optional[int]
