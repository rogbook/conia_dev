from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DataCategoryBrand(BaseModel):
    """
    카테고리, 브랜드 데이터 모델
    """
    id: int
    name: str
    status: str
    description: Optional[str]
    reg_date: datetime
    mod_date: datetime
    photo: Optional[str]
    pid: Optional[int]
    depth: Optional[int]
    depth1_name: Optional[str]
    depth2_name: Optional[str]
    depth3_name: Optional[str]
    depth4_name: Optional[str]

    class Config:
        orm_mode = True


class AddCategoryBrand(BaseModel):
    """
    카테고리, 브랜드 등록 모델
    """
    name: str
    description: Optional[str]
    photo: Optional[str]
    pid: Optional[int]


class ModCategoryBrand(BaseModel):
    """
    카테고리, 브랜드 수정 모델
    """
    name: Optional[str]
    status: Optional[str]
    description: Optional[str]
    photo: Optional[str]
