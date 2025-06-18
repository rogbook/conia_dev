from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field
from typing import Optional, List


class DataMember(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class DataOption(BaseModel):
    supply_price: Decimal
    origin_price: Decimal
    selling_price: Decimal
    option_title: Optional[str]
    option_1: Optional[str]
    option_2: Optional[str]
    option_3: Optional[str]
    option_4: Optional[str]
    option_5: Optional[str]

    class Config:
        orm_mode = True


class DataEcoupon(BaseModel):
    pin_code: str

    class Config:
        orm_mode = True


class DataOrderProduct(BaseModel):
    id: int
    ea: int
    complete_date: Optional[datetime]

    product_option: DataOption
    ecoupon: Optional[DataEcoupon]

    class Config:
        orm_mode = True


class DataProduct(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DataStore(BaseModel):
    code: Optional[str]
    title: Optional[str]

    class Config:
        orm_mode = True


class DataCompany(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True


class DataSettlementRaw(BaseModel):
    id: int = Field(title="ID")
    target_date: date = Field(title="정산일")
    order_id: str = Field(title="주문번호")
    order_product_id: int = Field(title="주문상품")
    product_id: int = Field(title="상품 ID")
    store_code: str = Field(title="상점 코드")
    amount: Decimal = Field(title="정산 대상금")
    pg_type: str = Field(title="결제 방법")
    supply_price: Decimal = Field(title="공급가")
    margin_price: Decimal = Field(title="마진가")
    processed: datetime = Field(title="데이터 처리일")
    reg_date: datetime = Field(title="등록일")

    order_product: DataOrderProduct
    product: DataProduct
    store: DataStore

    class Config:
        orm_mode = True


class DataSettlementData(BaseModel):
    id: int = Field(title="ID")
    target_date: date = Field(title="정산일")
    account_raw_id: str = Field(title="정산 Raw 번호")
    member_id: int = Field(title="수익 대상자")
    type: str = Field(title="타입")
    sequence: int = Field(title="정산 순번")
    target_amount: Decimal = Field(title="정산 대상금")
    amount: Decimal = Field(title="정산금")
    commission_type: Optional[str] = Field(title="수수료 타입")
    commission_value: Optional[Decimal] = Field(title="수수료 값")
    payment_date: Optional[datetime] = Field(title="지급일")
    reg_date: datetime = Field(title="등록일")
    mod_date: Optional[datetime] = Field(title="수정일")
    pg_provider: Optional[str] = Field(title="PG 공급사")
    pg_kind: Optional[str] = Field(title="결제 방법")
    status: Optional[str] = Field(title="상태")
    reject: Optional[str] = Field(title="반려 사유")
    tax: Optional[str] = Field(title="과세여부")
    payment: Optional[str] = Field(title="지급방식")

    account_raw: DataSettlementRaw
    member: DataMember

    class Config:
        orm_mode = True


class DataSettlementShip(BaseModel):
    id: int = Field(title="ID")
    target_date: date = Field(title="정산일")
    order_id: str = Field(title="주문 번호")
    order_shipping_id: int = Field(title="주문 배송 ID")
    store_code: str = Field(title="상점 코드")
    type: str = Field(title="정산 타입")
    sequence: Decimal = Field(title="정산 순번")
    target_amount: Decimal = Field(title="정산 대상금")
    amount: Decimal = Field(title="정산금")
    member_id: Optional[Decimal] = Field(title="수익 대상자")
    payment_date: Optional[datetime] = Field(title="지급일")
    reg_date: datetime = Field(title="등록일")
    commission_type: Optional[str] = Field(title="수수료 타입")
    commission_value: Optional[Decimal] = Field(title="수수료 값")
    pg_provider: Optional[str] = Field(title="PG 공급사")
    pg_kind: Optional[str] = Field(title="결제 방법")
    status: Optional[str] = Field(title="상태")
    reject: Optional[str] = Field(title="반려 사유")
    mod_date: Optional[datetime] = Field(title="수정일")

    account_raw: Optional[DataSettlementRaw]
    member: DataMember
    store: DataStore

    class Config:
        orm_mode = True


class ListData(BaseModel):
    total: int
    total_sum: Optional[int]
    datas: List[DataSettlementData]


class ListShipData(BaseModel):
    total: int
    total_sum: Optional[int]
    datas: List[DataSettlementShip]


class ModSettlementData(BaseModel):
    ids: List[int]
    status: Optional[str]
    reject: Optional[str]
    date_range: Optional[str]


class SettlementHistoryData(BaseModel):
    id: int
    target_date: date
    member: DataMember
    type: str
    sequence: int
    target_amount: Decimal
    amount: Decimal
    commission_type: Optional[str]
    commission_value: Optional[Decimal]
    reg_date: Optional[datetime]
    payment: Optional[str]

    class Config:
        orm_mode = True


class ListSettlementHistoryData(BaseModel):
    datas: List[SettlementHistoryData]


class DataMemberSC(BaseModel):
    id: int
    name: str
    email: str

    store: Optional[DataStore]
    company: DataCompany

    class Config:
        orm_mode = True


class SettlementExcelReq(BaseModel):
    id: int
    member_id: int
    member_type: str
    request_member: int
    reg_date: Optional[datetime]
    mod_date: Optional[datetime]
    s_reg_date: Optional[date]
    e_reg_date: Optional[date]
    status: str
    file: Optional[str]

    member: DataMemberSC
    member1: DataMember

    class Config:
        orm_mode = True
