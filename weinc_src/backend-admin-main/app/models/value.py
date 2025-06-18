from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Optional, List


class AddOptionValue(BaseModel):
    type: str = Field(title="타입")
    name: str = Field(title="이름")
    value: str = Field(title="값")
    sort: Optional[int] = Field(title="순서")


class DataOptionValue(BaseModel):
    id: int = Field(title="아이디")
    type: str = Field(title="타입")
    name: str = Field(title="이름")
    value: str = Field(title="값")
    sort: int = Field(title="순서")

    class Config:
        orm_mode = True


class ModOptionValue(BaseModel):
    type: Optional[str] = Field(title="타입")
    name: Optional[str] = Field(title="이름")
    value: Optional[str] = Field(title="값")
    sort: Optional[int] = Field(title="순서")


class AddSettingValue(BaseModel):
    type: str = Field(title="타입")
    name: str = Field(title="이름")
    value: str = Field(title="값")
    description: Optional[str] = Field(title="설명")


class DataSettingValue(BaseModel):
    id: int = Field(title="아이디")
    type: str = Field(title="타입")
    name: str = Field(title="이름")
    value: str = Field(title="값")
    description: Optional[str] = Field(title="설명")

    class Config:
        orm_mode = True


class ModSettingValue(BaseModel):
    type: Optional[str] = Field(title="타입")
    name: Optional[str] = Field(title="이름")
    value: Optional[str] = Field(title="값")
    description: Optional[str] = Field(title="설명")


class DataNoticeInfoTemplateCategory(BaseModel):
    category: str

    class Config:
        orm_mode = True


class DataNoticeInfoTemplate(BaseModel):
    category: str
    item: str

    class Config:
        orm_mode = True


class DataFavoriteOptionProperty(BaseModel):
    value: str = Field(title="값")
    price: Decimal = Field(title="가격")
    code: str = Field(title="가격")

    class Config:
        orm_mode = True


class DataFavoriteOption(BaseModel):
    id: int = Field(title="아이디")
    name: str = Field(title="이름")
    type: Optional[str] = Field(title="타입")
    propertys: List[DataFavoriteOptionProperty]

    class Config:
        orm_mode = True


class AddFavoriteOption(BaseModel):
    name: str = Field(title="이름")
    type: Optional[str] = Field(title="타입")
    propertys: List[DataFavoriteOptionProperty]

