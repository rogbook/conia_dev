from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict
import re


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


class MemberToken(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    store_code: Optional[List[str]]

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str
    store_code: str


class AppleLogin(BaseModel):
    id_token: str
    state: str


class TargetCheck(BaseModel):
    token_version_id: str
    id: str


class PasswordReset(BaseModel):
    password: str
    token: str


class PasswordChange(BaseModel):
    password: str
    new_password: str
    store_code: str


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