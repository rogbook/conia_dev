from decimal import Decimal
from datetime import datetime, time
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class DataUser(BaseModel):
    name: str

    class Config:
        orm_mode = True


class DataPhoto(BaseModel):
    id: int
    product_id: int
    uri: str
    reg_dt: datetime
    mod_dt: datetime

    class Config:
        orm_mode = True


class DataReviewPhoto(BaseModel):
    id: int
    product_review_id: int
    uri: str
    reg_dt: datetime
    mod_dt: datetime

    class Config:
        orm_mode = True


class DataReview(BaseModel):
    id: int
    contents: str
    status: str
    mod_date: datetime
    customer: DataUser
    photos: Optional[List[DataReviewPhoto]]

    class Config:
        orm_mode = True


class DataBadge(BaseModel):
    name: str
    color: str

    class Config:
        orm_mode = True


class DataBrand(BaseModel):
    name: str

    class Config:
        orm_mode = True


class DataCommonInfo(BaseModel):
    id: int
    name: str
    contents: str
    status: str
    reg_date: datetime
    mod_date: datetime

    class Config:
        orm_mode = True


class DataInventory(BaseModel):
    count: int
    safe_count: int

    class Config:
        orm_mode = True


class DataOptions(BaseModel):
    id: int
    code: Optional[str]
    origin_price: Decimal
    selling_price: Decimal
    view_yn: str
    default_yn: str
    product_id: int
    weight: Decimal
    status: Optional[str]
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
    option_tmp_price: Optional[str]
    is_sold_out: Optional[bool]

    inventory: Optional[DataInventory]

    class Config:
        orm_mode = True


class DataProduct(BaseModel):
    id: int
    member_id: int
    name: str
    type: Optional[str]
    status: str
    view_yn: Optional[str]
    code: Optional[str]
    summary: Optional[str]
    keyword: Optional[str]
    contents: Optional[str]
    tax: Optional[str]
    min_purchase_limit: Optional[int]
    max_purchase_limit: Optional[int]
    adult: Optional[str]
    hscode: Optional[str]
    reg_date: datetime
    mod_date: datetime
    ipcc_yn: Optional[str]
    cancel_yn: Optional[str]
    confirm: Optional[str]
    video: Optional[str]
    memo: Optional[str]
    common_info_id: Optional[int]
    shipping_info_id: Optional[int]
    inven_use: str
    coupon_yn: Optional[str] = Field(title="쿠폰 사용 여부")
    option_use: Optional[str] = Field(title="옵션 사용 여부")
    barcode: Optional[str] = Field(title="배송그룹 id")
    user_limit: Optional[int] = Field(title="1인당 구매횟수 제한")
    use_end_period: Optional[int] = Field(title="비실물 상품 사용 기한 (일)")
    use_end_date: Optional[Union[datetime, str]] = Field(title="비실물 상품 사용 기한 (지정 일시)")
    sale_start_date: Optional[Union[datetime, str]] = Field(title="판매 가능 시간 시작")
    sale_end_date: Optional[Union[datetime, str]] = Field(title="판매 가능 시간 종료")
    sale_start_time: Optional[Union[time, str]] = Field(title="판매 가능 일(시각) 시작")
    sale_end_time: Optional[Union[time, str]] = Field(title="판매 가능 일(시각) 종료")
    tel: Optional[str] = Field(title="")
    address: Optional[str] = Field(title="")
    lat: Optional[str] = Field(title="")
    lng: Optional[str] = Field(title="")
    subtitle: Optional[str] = Field(title="부제목")
    view_inventory: Optional[str] = Field(title="재고 노출여부")
    view_end_time: Optional[str] = Field(title="판매 종료시간 노출여부")
    api_provider: Optional[str] = Field(title="외부업체 연동 구분")
    api_goods_id: Optional[str] = Field(title="외부업체 상품 ID")
    use_place: Optional[str] = Field(title="E쿠폰 사용처")
    user_limit_reset: Optional[str] = Field(title="1인당 구매횟수 제한 초기화 방법")
    inven_cnt: Optional[int] = 0
    is_sold_out: Optional[bool]
    product_default: Optional[DataOptions]

    common_info: Optional[DataCommonInfo]
    options: Optional[List[DataOptions]]
    photos: List[DataPhoto]
    reviews: Optional[List[DataReview]]
    badges: Optional[List[DataBadge]]
    brands: Optional[List[DataBrand]]

    class Config:
        orm_mode = True


class ListProduct(BaseModel):
    datas: Optional[List[DataProduct]]

    class Config:
        orm_mode = True


class DataProductReview(BaseModel):
    id: int
    product_id: int
    member_id: int
    title: str
    contents: str
    rating: Optional[float]
    status: str
    reg_date: datetime
    mod_date: datetime
    order_info: str

    class Config:
        orm_mode = True


class AddProductReview(BaseModel):
    order_product_id: int
    contents: str
    order_info: Optional[str]


class ModProductReview(BaseModel):
    title: Optional[str]
    contents: str
    rating: Optional[float]


class AddProductQna(BaseModel):
    title: str
    contents: str
    store_code: str
