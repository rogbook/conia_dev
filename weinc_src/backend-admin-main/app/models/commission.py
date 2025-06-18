from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class DataStore(BaseModel):
    code: str
    title: str
    class Config:
        orm_mode = True


class DataMember(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True


class DataProductPhoto(BaseModel):
    uri: Optional[str]

    class Config:
        orm_mode = True


class DataProduct(BaseModel):
    id: str
    code: str
    name: str

    photos: List[DataProductPhoto]
    class Config:
        orm_mode = True


class DataDefaultCommission(BaseModel):
    """
    기본 수수료데이터 모델
    """
    id: int = Field(title="ID")
    default_commission: float = Field(title="기본 수수료")


class DataCommission(BaseModel):
    """
    수수료 데이터 모델
    """
    id: int = Field(title="ID")
    store_code: Optional[str] = Field(title="대상 상점 코드")
    product_id: Optional[int] = Field(title="대상 상품")
    member_id: Optional[int] = Field(title="대상 회원")
    type: str = Field(title="고정(F) / 퍼센트(P)")
    value: Decimal = Field(title="수수료")
    default: str = Field(title="기본 여부")
    mod_date: datetime = Field(title="수정일시")
    target: int = Field(title="수익 대상")
    target_type: Optional[str] = Field(title="대상 타입")
    pg_provider: Optional[str] = Field(title="PG 공급사")
    pg_kind: Optional[str] = Field(title="결제 방법")
    payment: Optional[str] = Field(title="지급방식 (D : 이익차감, S : 분리지급)")

    member: Optional[DataMember]
    member1: Optional[DataMember]
    store: Optional[DataStore]
    product: Optional[DataProduct]

    class Config:
        orm_mode = True


class AddCommission(BaseModel):
    """
    기본 수수료 수정 데이터 모델
    """
    value: Decimal = Field(title="수수료")
    type: str = Field(title="고정(F) / 퍼센트(P)")
    store_code: Optional[str] = Field(title="대상 상점 코드")
    product_id: Optional[int] = Field(title="대상 상품")
    member_id: Optional[int] = Field(title="대상 회원")
    target: int = Field(title="수익 대상")
    target_type: Optional[str] = Field(title="대상 타입")
    kind: Optional[str] = Field(title="prd, ship")
    payment: Optional[str] = Field(title="지급방식 (D : 이익차감, S : 분리지급)")


class ModCommission(BaseModel):
    """
    기본 수수료 수정 데이터 모델
    """
    id: int = Field(title="ID")
    value: Optional[Decimal] = Field(title="수수료")
    type: Optional[str] = Field(title="고정(F) / 퍼센트(P)")
    store_code: Optional[str] = Field(title="대상 상점 코드")
    product_id: Optional[int] = Field(title="대상 상품")
    member_id: Optional[int] = Field(title="대상 회원")


class ModDefaultCommission(BaseModel):
    """
    기본 수수료 수정 데이터 모델
    """
    value: Decimal = Field(title="수수료")
    type: str = Field(title="고정(F) / 퍼센트(P)")

class ListCommission(BaseModel):
    total: int
    datas: List[DataCommission]

