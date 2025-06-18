from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict
import re


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


class MemberToken(BaseModel):
    id: int
    name: str
    email: Optional[str]
    company_id: Optional[int]
    partner: Optional[str]
    status: str
    member_class: Optional[List[str]]
    scopes: Dict[str, List[str]] = {}
    organization: Dict[str, List[str]] = {}
    admin: Optional[str]
    store_code: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class SnsLogin(BaseModel):
    type: str
    token: str


class PasswordChange(BaseModel):
    password: str
    new_password: str


class FindId(BaseModel):
    token_version_id: str = Field(title="본인인증 데이터 (token_version_id)")


class ChangePassword(BaseModel):
    token_version_id: str = Field(title="본인인증 데이터 (token_version_id)")
    email_id: str = Field(title="이메일 아이디")
    new_password: str = Field(title="새로운 패스워드")


class CertSmsReq(BaseModel):
    mobile: str

    @validator("mobile")
    def mobile_check(cls, v):
        regex = r"^(01[0-9])\-?([1-9]{3,4})\-?([1-9]{4,4})$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class CertSmsVerify(BaseModel):
    mobile: str
    code: str = Field(min_length=6, max_length=6)

    @validator("mobile")
    def mobile_check(cls, v):
        regex = r"^(01[0-9])\-?([1-9]{3,4})\-?([1-9]{4,4})$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class CertNiceIdReq(BaseModel):
    return_url: str = Field(title="결과를 받을 URL")


class CertNiceId(BaseModel):
    token_version_id: str = Field(title="본인인증 데이터 (token_version_id)")
    enc_data: str = Field(title="본인인증 데이터 (enc_data)")
    integrity_value: str = Field(title="본인인증 데이터 (integrity_value)")


class CertNiceIdResult(BaseModel):
    name: str = Field(title="이름")
    mobile: str = Field(title="휴대 전화번호")
    birth: str = Field(title="생년월일")
    gender: str = Field(title="성별")


class Menu(BaseModel):
    name: str = Field(title="이름")
    depth: int = Field(title="Depth")
    menu_id: Optional[int] = Field(title="상위 메뉴")

    class Config:
        orm_mode = True


class MenuList(BaseModel):
    depth1: Optional[List[Menu]] = Field(title="대메뉴")
    depth2: Optional[List[Menu]] = Field(title="중메뉴")
    depth3: Optional[List[Menu]] = Field(title="소메뉴")

