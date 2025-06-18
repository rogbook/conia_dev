from pydantic import BaseModel, Field
from typing import Optional, List

from app.models.common import ListData
from app.models.user.member import DataSimpleMember


class DataBadge(BaseModel):
    id: int
    name: str = Field(title="뱃지 이름")
    color: Optional[str] = Field(title="색상 16진수")
    img: Optional[str] = Field(title="이미지 URL")
    shape: Optional[str] = Field(title="형태")

    class Config:
        orm_mode = True


class DataShop(BaseModel):
    """
    매장 정보 데이터 모델
    """
    id: int = Field(title="ID")
    name: str = Field(title="매장명")
    description: str = Field(title="매장 설명")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="상세 주소")
    work_time: Optional[str] = Field(title="운영 시간")
    holiday: Optional[str] = Field(title="휴무일")
    image: Optional[str] = Field(title="이미지")
    lat: Optional[str] = Field(title="위도")
    lng: Optional[str] = Field(title="경도")
    tel: Optional[str] = Field(title="전화번호")
    subtitle: Optional[str] = Field(title="부제목")

    member: DataSimpleMember
    badges: Optional[List[DataBadge]]

    class Config:
        orm_mode = True


class AddShop(BaseModel):
    name: str = Field(title="매장명")
    description: str = Field(title="매장 설명")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="주소 상세")
    work_time: Optional[str] = Field(title="운영 시간")
    holiday: Optional[str] = Field(title="휴무일")
    image: Optional[str] = Field(title="이미지")
    lat: Optional[str] = Field(title="위도")
    lng: Optional[str] = Field(title="경도")
    tel: Optional[str] = Field(title="전화번호")
    subtitle: Optional[str] = Field(title="부제목")


class ModShop(BaseModel):
    name: Optional[str] = Field(title="매장명")
    description: Optional[str] = Field(title="매장 설명")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="주소 상세")
    work_time: Optional[str] = Field(title="운영 시간")
    holiday: Optional[str] = Field(title="휴무일")
    image: Optional[str] = Field(title="이미지")
    lat: Optional[str] = Field(title="위도")
    lng: Optional[str] = Field(title="경도")
    tel: Optional[str] = Field(title="전화번호")
    subtitle: Optional[str] = Field(title="부제목")


class ListShop(ListData):
    datas: List[DataShop]
