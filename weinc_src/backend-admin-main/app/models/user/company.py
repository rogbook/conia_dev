from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional, List

from app.models.user.member import DataMember


class CorpType(str, Enum):
    """
    사업자 종류 (개인(P),법인(B),개인사업자(PB),개인사업자간이과세(PBS))
    """
    P = "P"
    B = "B"
    PB = "PB"
    PBS = "PBS"


class DataCompany(BaseModel):
    """
    회사 정보 데이터 모델
    """
    id: int = Field(title="ID")
    member_id: int = Field(title="회원 ID")
    name: Optional[str] = Field(title="회사명")
    ceo: Optional[str] = Field(title="대표자명")
    reg_no: Optional[str] = Field(title="사업자등록번호")
    biz_type: Optional[str] = Field(title="업태")
    biz_item: Optional[str] = Field(title="업종")
    zipcode: Optional[str] = Field(title="우편번호")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="주소상세")
    phone: Optional[str] = Field(title="대표자 전화번호")
    mobile: Optional[str] = Field(title="대표자 휴대전화")
    corp_type: str = Field(title="사업자 종류 (개인(P),법인(B),개인사업자(PB),개인사업자간이과세(PBS))")
    corp_number: Optional[str] = Field(title="법인번호/주민번호")
    tax_email: Optional[str] = Field(title="계산서 이메일")
    bank: Optional[str] = Field(title="은행")
    account: Optional[str] = Field(title="계좌번호")
    bank_user: Optional[str] = Field(title="예금주")
    photo_reg: Optional[str] = Field(title="사업자등록증 사진")
    photo_bank: Optional[str] = Field(title="통장 사본 사진")
    status: str = Field(title="상태")
    reg_date: datetime = Field(title="등록일시")
    mod_date: datetime = Field(title="수정일시")
    manager_name: Optional[str] = Field(title="사업자등록증 사진")
    manager_phone: Optional[str] = Field(title="통장 사본 사진")
    manager_mobile: Optional[str] = Field(title="담당자명")
    manager_email: Optional[str] = Field(title="담당자 전화번호")
    settlement_name: Optional[str] = Field(title="담당자 휴대전화")
    settlement_phone: Optional[str] = Field(title="담당자 이메일")
    settlement_mobile: Optional[str] = Field(title="정산 담당자명")
    settlement_email: Optional[str] = Field(title="정산 담당자 전화번호")
    cs_name: Optional[str] = Field(title="정산 담당자 휴대전화")
    cs_phone: Optional[str] = Field(title="정산 담당자 이메일")
    cs_mobile: Optional[str] = Field(title="CS 담당자명")
    cs_email: Optional[str] = Field(title="CS 담당자 전화번호")
    network_reg_no: Optional[str] = Field(title="통신판매업 신고번호")

    member: DataMember

    class Config:
        orm_mode = True


class ModCompany(BaseModel):
    """
    회사 정보 수정 데이터 모델
    """
    name: Optional[str] = Field(title="회사명")
    ceo: Optional[str] = Field(title="대표자명")
    reg_no: Optional[str] = Field(title="사업자등록번호")
    biz_type: Optional[str] = Field(title="업태")
    biz_item: Optional[str] = Field(title="업종")
    zipcode: Optional[str] = Field(title="우편번호")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="주소상세")
    phone: Optional[str] = Field(title="대표자 전화번호")
    mobile: Optional[str] = Field(title="대표자 휴대전화")
    corp_type: Optional[CorpType] = Field(title="사업자 종류 (개인(P),법인(B),개인사업자(PB),개인사업자간이과세(PBS))")
    corp_number: Optional[str] = Field(title="법인번호/주민번호")
    tax_email: Optional[str] = Field(title="계산서 이메일")
    bank: Optional[str] = Field(title="은행")
    account: Optional[str] = Field(title="계좌번호")
    bank_user: Optional[str] = Field(title="예금주")
    status: Optional[str] = Field(title="상태")
    manager_name: Optional[str] = Field(title="사업자등록증 사진")
    manager_phone: Optional[str] = Field(title="통장 사본 사진")
    manager_mobile: Optional[str] = Field(title="담당자명")
    manager_email: Optional[str] = Field(title="담당자 전화번호")
    settlement_name: Optional[str] = Field(title="담당자 휴대전화")
    settlement_phone: Optional[str] = Field(title="담당자 이메일")
    settlement_mobile: Optional[str] = Field(title="정산 담당자명")
    settlement_email: Optional[str] = Field(title="정산 담당자 전화번호")
    cs_name: Optional[str] = Field(title="정산 담당자 휴대전화")
    cs_phone: Optional[str] = Field(title="정산 담당자 이메일")
    cs_mobile: Optional[str] = Field(title="CS 담당자명")
    cs_email: Optional[str] = Field(title="CS 담당자 전화번호")
    network_reg_no: Optional[str] = Field(title="통신판매업 신고번호")


class DataDept(BaseModel):
    id: int
    name: str
    description: str
    status: str
    reg_date: datetime
    mod_date: datetime
    member_company_id: int
    pid: int

    member_company: DataCompany
    parent: 'DataDept' = None

    class Config:
        orm_mode = True


class AddDept(BaseModel):
    name: str
    description: Optional[str]
    pid: Optional[int]


class UpdateDept(BaseModel):
    name: str
    description: str
    status: str


class ListCompany(BaseModel):
    total: int
    datas: List[DataCompany]
