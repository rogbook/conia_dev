from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class DataInventory(BaseModel):
    id: int
    count: Optional[int]
    safe_count: Optional[int]
    day_able_count: Optional[int]
    use_acc_qty: Optional[str]

    class Config:
        orm_mode = True


class AddProductOption(BaseModel):
    code: Optional[str]
    supply_price: Optional[int]
    origin_price: Optional[int]
    selling_price: int
    view_yn: str
    default_yn: str
    count: int = 0
    safe_count: int = 0
    day_able_count: Optional[int]
    use_acc_qty: Optional[str]
    weight: Decimal = 0
    option_title: Optional[str]
    option_1: Optional[str]
    option_2: Optional[str]
    option_3: Optional[str]
    option_4: Optional[str]
    option_5: Optional[str]
    option_code_1: Optional[str]
    option_code_2: Optional[str]
    option_code_3: Optional[str]
    option_code_4: Optional[str]
    option_code_5: Optional[str]
    option_tmp_price: Optional[str]


class DataProductOption(BaseModel):
    id: int
    code: Optional[str]
    supply_price: Optional[int]
    origin_price: Optional[int]
    selling_price: int
    view_yn: str
    default_yn: str
    product_id: int
    weight: Decimal
    status: str
    option_title: Optional[str]
    option_1: Optional[str]
    option_2: Optional[str]
    option_3: Optional[str]
    option_4: Optional[str]
    option_5: Optional[str]
    option_code_1: Optional[str]
    option_code_2: Optional[str]
    option_code_3: Optional[str]
    option_code_4: Optional[str]
    option_code_5: Optional[str]
    option_tmp_price: Optional[str]

    inventory: DataInventory

    class Config:
        orm_mode = True


class ModProductOption(BaseModel):
    opt_id: int
    code: Optional[str]
    supply_price: Optional[str]
    origin_price: Optional[str]
    selling_price: Optional[str]
    view_yn: Optional[str]
    default_yn: Optional[str]
    weight: Optional[str]
    status: Optional[str]
    option_title: Optional[str]
    option_1: Optional[str]
    option_2: Optional[str]
    option_3: Optional[str]
    option_4: Optional[str]
    option_5: Optional[str]
    option_code_1: Optional[str]
    option_code_2: Optional[str]
    option_code_3: Optional[str]
    option_code_4: Optional[str]
    option_code_5: Optional[str]
    option_tmp_price: Optional[str]
    count: Optional[int]
    safe_count: Optional[int]
    day_able_count: Optional[int]
    use_acc_qty: Optional[str]


class ModProductInventory(BaseModel):
    count: Optional[int]
    safe_count: Optional[int]
    day_able_count: Optional[int]
    use_acc_qty: Optional[str]
