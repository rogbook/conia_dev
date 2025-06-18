from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal


class AddShippingAreaDetail(BaseModel):
    category_text: str
    zipcode: str
    address_house: str
    address_street: str
    shipping_area_id: int


class DataShippingAreaDetail(BaseModel):
    id: int
    category_text: str
    zipcode: str
    address_house: str
    address_street: str
    shipping_area_id: int

    class Config:
        orm_mode = True


class ModShippingAreaDetail(BaseModel):
    category_text: Optional[str]
    zipcode: Optional[str]
    address_house: Optional[str]
    address_street: Optional[str]


class AddShippingArea(BaseModel):
    name: str
    cost: int
    shipping_cost_id: int


class DataShippingArea(BaseModel):
    id: int
    name: str
    cost: int
    shipping_cost_id: int

    shipping_area_details: Optional[List[DataShippingAreaDetail]]

    class Config:
        orm_mode = True


class ModShippingArea(BaseModel):
    name: Optional[str]
    cost: Optional[int]


class AddShippingCost(BaseModel):
    type: str
    category: str
    cost: int
    section_start: Optional[int]
    section_end: Optional[int]
    section_repeat: Optional[int]


class DataShippingCost(BaseModel):
    id: int
    type: str
    category: str
    cost: int
    section_start: Optional[int]
    section_end: Optional[int]
    section_repeat: Optional[int]
    shipping_info_id: int

    shipping_areas: Optional[List[DataShippingArea]]

    class Config:
        orm_mode = True


class ModShippingCost(BaseModel):
    type: Optional[str]
    category: Optional[str]
    cost: Optional[int]
    section_start: Optional[int]
    section_end: Optional[int]
    section_repeat: Optional[int]


class AddShippingInfo(BaseModel):
    name: str
    type: str
    pay_type: str
    calc_type: str
    return_cost: Decimal
    change_cost: Decimal
    member_id: Optional[int] = Field(title="PA Id")


class DataSimpleCompany(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DataSimpleMember(BaseModel):
    id: int
    name: str
    email: str

    company: Optional[DataSimpleCompany]

    class Config:
        orm_mode = True


class DataShippingInfo(BaseModel):
    id: int
    name: str
    type: str
    pay_type: str
    calc_type: str
    return_cost: Decimal
    change_cost: Decimal
    status: str
    reg_date: datetime
    mod_date: datetime

    member: DataSimpleMember
    shipping_costs: Optional[List[DataShippingCost]]

    class Config:
        orm_mode = True


class ModShippingInfo(BaseModel):
    name: Optional[str]
    type: Optional[str]
    pay_type: Optional[str]
    calc_type: Optional[str]
    return_cost: Optional[Decimal]
    change_cost: Optional[Decimal]
    status: Optional[str]
