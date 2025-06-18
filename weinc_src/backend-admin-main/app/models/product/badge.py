from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DataBadge(BaseModel):
    id: int
    name: str = Field(title="뱃지 이름")
    color: Optional[str] = Field(title="색상 16진수")
    img: Optional[str] = Field(title="이미지 URL")
    shape: Optional[str] = Field(title="형태")
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class AddBadge(BaseModel):
    name: str = Field(title="뱃지 이름")
    color: Optional[str] = Field(title="색상 16진수")
    img: Optional[str] = Field(title="이미지 URL")
    shape: Optional[str] = Field(title="형태")


class ModBadge(BaseModel):
    name: Optional[str] = Field(title="뱃지 이름")
    color: Optional[str] = Field(title="색상 16진수")
    img: Optional[str] = Field(title="이미지 URL")
    shape: Optional[str] = Field(title="형태")
