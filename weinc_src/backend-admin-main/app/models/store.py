from typing import Union

from pydantic import Field, validator
from enum import Enum

from app.models.product.info import *

from app.models.product.product import DataSimpleProduct
from app.models.common import ListData, date_validator
from app.models.user.member import DataSimpleMember

from app.utils.crypto_utils import AES256
from app.common.consts import AES_KEY, AES_IV


class DataCustomer(BaseModel):
    id: int
    name: Optional[str]
    email: str

    class Config:
        orm_mode = True


class DataRecommanderMember(BaseModel):
    id: int
    name: Optional[str]
    email: str

    class Config:
        orm_mode = True


class AddStore(BaseModel):
    code: str
    member_id: int
    title: str
    type: str
    domain: Optional[str]
    verify_code: Optional[str]
    exclude_menu: Optional[str]
    group: Optional[str]


class DataStore(BaseModel):
    code: str
    member_id: int
    title: str
    type: str
    domain: Optional[str]
    layout: Optional[str]
    status: str
    reg_date: datetime
    mod_date: datetime
    auto_join: Optional[str]
    logo_pc: Optional[str]
    logo_mobile: Optional[str]
    favicon: Optional[str]
    info: Optional[str]
    dupl_store: Optional[str]
    able_target_use: str
    verify_code: Optional[str]
    exclude_menu: Optional[str]
    group: Optional[str]
    prd_pg_opt_use: Optional[str]
    meal_opt_use: Optional[str]
    meal_opt_limit_use: Optional[str]
    meal_opt_limit_time: Optional[str]
    meal_opt_cancel_use: Optional[str]
    keyword: Optional[str]

    member: DataSimpleMember

    class Config:
        orm_mode = True


class ModStore(BaseModel):
    title: Optional[str]
    type: Optional[str]
    domain: Optional[str]
    status: Optional[str]
    layout: Optional[str]
    auto_join: Optional[str]
    logo_pc: Optional[str]
    logo_mobile: Optional[str]
    favicon: Optional[str]
    info: Optional[str]
    dupl_store: Optional[str]
    able_target_use: Optional[str]
    verify_code: Optional[str]
    exclude_menu: Optional[str]
    group: Optional[str]
    prd_pg_opt_use: Optional[str]
    meal_opt_use: Optional[str]
    meal_opt_limit_use: Optional[str]
    meal_opt_limit_time: Optional[str]
    meal_opt_cancel_use: Optional[str]
    keyword: Optional[str]


class ListDataStore(BaseModel):
    total: int = Field(title="Total Count")
    datas: List[DataStore]


class AddMemberStore(BaseModel):
    store_code: str
    customer_id: int
    confirm: str
    recommander_member_id: Optional[int]


class DataMemberStore(BaseModel):
    id: int
    store_code: str
    customer_id: int
    confirm: str
    reg_date: datetime
    mod_date: datetime
    recommander_member_id: Optional[int]
    value: Optional[str]

    customer: DataCustomer
    recommander_member: Optional[DataRecommanderMember]

    class Config:
        orm_mode = True


class ModMemberStore(BaseModel):
    confirm: Optional[str]


class DataStoreTheme(BaseModel):
    id: int
    name: str
    description: str
    store_code: str
    pid: Optional[int]
    layout: Optional[str]
    visible: Optional[str]
    top_visible: str
    use_layout: str
    status: str
    sort: int
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class AddStoreTheme(BaseModel):
    name: str
    description: Optional[str]
    store_code: str
    pid: Optional[int]


class ModStoreTheme(BaseModel):
    name: Optional[str]
    description: Optional[str]
    layout: Optional[str]
    status: Optional[str]
    visible: Optional[str]
    top_visible: Optional[str]
    use_layout: Optional[str]
    sort: Optional[int]


class SubStoreTheme(BaseModel):
    id: int
    name: str
    description: str
    store_code: str
    pid: Optional[int]
    layout: Optional[str]
    status: str
    visible: Optional[str]
    top_visible: str
    use_layout: str
    reg_date: datetime
    mod_date: datetime
    sort: int

    sub: Optional[List['SubStoreTheme']]


class DataStoreProduct(BaseModel):
    id: int
    view_yn: str
    variation: int

    product: Optional[DataSimpleProduct]

    class Config:
        orm_mode = True


class DataSimpleStore(BaseModel):
    code: str
    title: str
    status: str
    logo_pc: Optional[str]
    logo_mobile: Optional[str]
    keyword: Optional[str]

    class Config:
        orm_mode = True


class DataSimpleStoreProd(BaseModel):
    view_yn: str
    product_id: int

    class Config:
        orm_mode = True


class ListCatalogProduct(BaseModel):
    total: int
    datas: List[DataStoreProduct]


class ProductVariation(BaseModel):
    id: int
    variation: int


class LinkProduct(BaseModel):
    products: List[ProductVariation]


class SubStore(BaseModel):
    title: str
    store_code: str


class ListMemberStore(BaseModel):
    total: int
    datas: List[DataMemberStore]


class EnumLogoType(str, Enum):
    logo_p = 'logo-p'
    logo_m = 'logo-m'
    favicon = 'favicon'


class DataAbleTarget(BaseModel):
    id: int
    store_code: str
    unique_value: str
    name: str
    mobile: str
    used: str

    class Config:
        orm_mode = True

    @validator('mobile')
    def decrypt(cls, v):
        if len(v) > 24:  # ListDataMember 로 들어 가면 두번 호출 되어 복호화된 데이터를 또 다시 복호화 시도 에러 발생
            v = AES256(AES_KEY, AES_IV).decrypt(v)
        return v


class ListAbleTarget(ListData):
    datas: List[DataAbleTarget]


class DataStorePopup(BaseModel):
    id: int
    store_code: str
    title: str
    contents: Optional[str]
    img: Optional[str]
    link: Optional[str]
    type: Optional[str]
    status: str
    view_start_date: Optional[datetime]
    view_end_date: Optional[datetime]
    duplicate: Optional[str]
    sort: int
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class AddStorePopup(BaseModel):
    store_code: str
    title: str
    contents: Optional[str]
    img: Optional[str]
    link: Optional[str]
    type: Optional[str]
    view_start_date: Optional[Union[datetime, str]]
    view_end_date: Optional[Union[datetime, str]]
    duplicate: Optional[str]
    sort: Optional[int]

    _date_validator = validator('view_start_date', 'view_end_date', allow_reuse=True)(date_validator)


class ModStorePopup(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    img: Optional[str]
    link: Optional[str]
    type: Optional[str]
    status: Optional[str]
    view_start_date: Optional[Union[datetime, str]]
    view_end_date: Optional[Union[datetime, str]]
    duplicate: Optional[str]
    sort: Optional[int]

    _date_validator = validator('view_start_date', 'view_end_date', allow_reuse=True)(date_validator)


class ListStorePopup(BaseModel):
    total: int
    datas: List[DataStorePopup]


class ModAbleTarget(BaseModel):
    unique_value: Optional[str]
    name: Optional[str]
    mobile: Optional[str]
    used: Optional[str]

    @validator('mobile')
    def encrypt(cls, v):
        v = AES256(AES_KEY, AES_IV).encrypt(v)
        return v


class AddAbleTarget(BaseModel):
    name: str
    unique_value: str
    mobile: str

    @validator('mobile')
    def encrypt(cls, v):
        v = AES256(AES_KEY, AES_IV).encrypt(v)
        return v


class AddBoardGroup(BaseModel):
    name: str
    menu_visible: str
    view_type: str
    view_end_content: Optional[str]
    sort: Optional[int]


class DataBoardGroup(BaseModel):
    id: int
    name: str
    menu_visible: str
    view_type: str
    view_end_content: Optional[str]
    sort: Optional[int]
    status: str
    store_code: str

    class Config:
        orm_mode = True


class ModBoardGroup(BaseModel):
    name: Optional[str]
    menu_visible: Optional[str]
    view_type: Optional[str]
    view_end_content: Optional[str]
    sort: Optional[int]
    status: Optional[str]


class ListBoardGroup(ListData):
    datas: List[DataBoardGroup]


class AddBoard(BaseModel):
    title: str
    contents: str
    pin: Optional[str]
    sort: Optional[int]
    image: Optional[str]
    view_start_date: Optional[datetime]
    view_end_date: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    store_board_group_id: int
    member_id: Optional[int]
    customer_id: Optional[int]


class DataBoard(BaseModel):
    id: int
    title: str
    contents: str
    pin: str
    sort: int
    status: str
    reg_date: datetime
    mod_date: datetime
    image: Optional[str]
    view_start_date: Optional[datetime]
    view_end_date: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    store_board_group_id: int
    member_id: Optional[int]
    customer_id: Optional[int]

    class Config:
        orm_mode = True


class ModBoard(BaseModel):
    title: Optional[str]
    contents: Optional[str]
    pin: Optional[str]
    sort: Optional[int]
    status: Optional[str]
    image: Optional[str]
    view_start_date: Optional[datetime]
    view_end_date: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    store_board_group_id: int


class ListBoard(ListData):
    datas: List[DataBoard]


class DataSimpleMember(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class AddBoardComment(BaseModel):
    comment: str
    store_board_id: int
    member_id: Optional[int]
    customer_id: Optional[int]
    p_id: Optional[int]


class DataBoardComment(BaseModel):
    id: int
    comment: str
    status: str
    reg_date: datetime
    mod_date: datetime
    store_board_id: int
    member_id: Optional[int]
    customer_id: Optional[int]
    p_id: Optional[int]

    customer: Optional[DataSimpleMember]
    member: Optional[DataSimpleMember]

    class Config:
        orm_mode = True


class ModBoardComment(BaseModel):
    comment: Optional[str]
    status: Optional[str]


class ListBoardComment(ListData):
    datas: List[DataBoardComment]


class MemoProduct(BaseModel):
    memo: str
    products: List[int]

class MemoOnlyProduct(BaseModel):
    memo: str

class TargetStore(BaseModel):
    target_store_code: str