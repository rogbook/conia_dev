from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


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


class AddCommonInfo(BaseModel):
    name: str
    contents: str
    member_id: Optional[int]


class DataCommonInfo(BaseModel):
    id: int
    name: str
    contents: str
    status: str
    reg_date: Optional[datetime]
    mod_date: Optional[datetime]
    member_id: Optional[int]

    member: Optional[DataSimpleMember]

    class Config:
        orm_mode = True


class ModCommonInfo(BaseModel):
    name: Optional[str]
    contents: Optional[str]
    status: Optional[str]
    member_id: Optional[int]


class AddNoticeInfo(BaseModel):
    product_id: int
    item: str
    category: str
    contents: str
    sort: int


class DataNoticeInfo(BaseModel):
    id: int
    product_id: int
    item: str
    category: str
    contents: str
    sort: int

    class Config:
        orm_mode = True


class ModNoticeInfo(BaseModel):
    notice_id: int
    product_id: int
    item: Optional[str]
    category: Optional[str]
    contents: Optional[str]
    sort: Optional[int]


class AddExtraInfo(BaseModel):
    product_id: int
    category: str
    contents: str


class DataExtraInfo(BaseModel):
    id: int
    product_id: int
    category: str
    contents: str

    class Config:
        orm_mode = True


class ModExtraInfo(BaseModel):
    id: int
    category: Optional[str]
    contents: Optional[str]


class DataOption(BaseModel):
    id: int
    code: Optional[str]
    option_title: Optional[str]
    option_1: Optional[str]
    option_2: Optional[str]
    option_3: Optional[str]
    option_4: Optional[str]
    option_5: Optional[str]
    option_code_1: Optional[str]
    option_code_2: Optional[str]
    option_code_3: Optional[str]
    option_code_4: Optional[str]
    option_code_5: Optional[str]

    class Config:
        orm_mode = True


class DataProductPhoto(BaseModel):
    id: int
    product_id: int
    uri: str
    reg_dt: datetime
    mod_dt: datetime
    product_option: Optional[DataOption]

    class Config:
        orm_mode = True
