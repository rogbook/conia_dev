from datetime import datetime, time
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union
from app.models.product.info import DataCommonInfo
from app.models.product.shipping import DataShippingInfo
from app.models.common import date_validator


class DataMemberCompany(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True


class DataMember(BaseModel):
    email: str
    name: str
    company: Optional[DataMemberCompany]

    class Config:
        orm_mode = True


class DataSimpleCategory(BaseModel):
    id: int
    name: str
    depth: Optional[int]
    depth1_name: Optional[str]
    depth2_name: Optional[str]
    depth3_name: Optional[str]
    depth4_name: Optional[str]
    depth1_id: Optional[int]
    depth2_id: Optional[int]
    depth3_id: Optional[int]
    depth4_id: Optional[int]

    class Config:
        orm_mode = True


class DataSimpleBrand(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DataProductOption(BaseModel):
    code: Optional[str]
    supply_price: Optional[int]
    origin_price: Optional[int]
    selling_price: Optional[int]
    view_yn: Optional[str]
    default_yn: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True


class DataProductPhoto(BaseModel):
    id: Optional[int]
    uri: Optional[str]

    class Config:
        orm_mode = True


class DataSimpleBadge(BaseModel):
    id: int
    name: str
    color: str
    shape: str
    imt: Optional[str]

    class Config:
        orm_mode = True


class AddProduct(BaseModel):
    member_id: int = Field(title="PA id (정산 대상자)")
    name: str = Field(title="상품명")
    type: Optional[str] = Field(title="")
    view_yn: Optional[str] = Field(title="노출 여부")
    code: Optional[str] = Field(title="상품코드")
    summary: Optional[str] = Field(title="요약 설명")
    keyword: Optional[str] = Field(title="검색 키워드")
    contents: Optional[str] = Field(title="내용")
    tax: Optional[str] = Field(title="과세여부")
    min_purchase_limit: Optional[str] = Field(title="최소 구매 수량")
    max_purchase_limit: Optional[str] = Field(title="최대 구매 수량")
    adult: Optional[str] = Field(title="성인인증 필요")
    hscode: Optional[str] = Field(title="")
    ipcc_yn: Optional[str] = Field(title="개인통관번호 여부")
    cancel_yn: Optional[str] = Field(title="취소 가능 여부")
    video: Optional[str] = Field(title="동영상 링크")
    memo: Optional[str] = Field(title="메모")
    common_info_id: Optional[int] = Field(title="공통정보 id")
    shipping_info_id: Optional[int] = Field(title="배송그룹 id")
    inven_use: Optional[str] = Field(title="간편 재고 사용 여부")
    coupon_yn: Optional[str] = Field(title="쿠폰 사용 여부")
    option_use: Optional[str] = Field(title="옵션 사용 여부")
    subtitle: Optional[str] = Field(title="부제목")
    view_inventory: Optional[str] = Field(title="재고 노출 여부")
    api_provider: Optional[str] = Field(title="외부업체 연동 구분")
    api_goods_id: Optional[str] = Field(title="외부업체 상품 ID")
    resale: Optional[str] = Field(title="사입 여부")


class DataProduct(BaseModel):
    id: int
    member_id: int = Field(title="PA id (정산 대상자)")
    name: str = Field(title="상품명")
    type: Optional[str] = Field(title="")
    status: str
    view_yn: Optional[str] = Field(title="노출 여부")
    code: Optional[str] = Field(title="상품코드")
    summary: Optional[str] = Field(title="요약 설명")
    keyword: Optional[str] = Field(title="검색 키워드")
    contents: Optional[str] = Field(title="내용")
    tax: Optional[str] = Field(title="과세여부")
    min_purchase_limit: Optional[str] = Field(title="최소 구매 수량")
    max_purchase_limit: Optional[str] = Field(title="최대 구매 수량")
    adult: Optional[str] = Field(title="성인인증 필요")
    hscode: Optional[str] = Field(title="")
    reg_date: datetime
    mod_date: datetime
    ipcc_yn: Optional[str] = Field(title="개인통관번호 여부")
    cancel_yn: Optional[str] = Field(title="취소 가능 여부")
    confirm: Optional[str] = Field(title="관리자 승인 여부")
    video: Optional[str] = Field(title="동영상 링크")
    memo: Optional[str] = Field(title="메모")
    common_info_id: Optional[int] = Field(title="공통정보 id")
    shipping_info_id: Optional[int] = Field(title="배송그룹 id")
    inven_use: str = Field(title="간편 재고 사용 여부")
    coupon_yn: str = Field(title="쿠폰 사용 여부")
    option_use: str = Field(title="옵션 사용 여부")
    barcode: Optional[str] = Field(title="배송그룹 id")
    user_limit: Optional[int] = Field(title="1인당 구매횟수 제한")
    use_end_period: Optional[int] = Field(title="비실물 상품 사용 기한 (일)")
    use_end_date: Optional[datetime] = Field(title="비실물 상품 사용 기한 (지정 일시)")
    sale_start_date: Optional[datetime] = Field(title="판매 가능 시간 시작")
    sale_end_date: Optional[datetime] = Field(title="판매 가능 시간 종료")
    sale_start_time: Optional[time] = Field(title='판매 가능 일(시각) 시작')
    sale_end_time: Optional[time] = Field(title='판매 가능 일(시각) 종료')
    tel: Optional[str] = Field(title="")
    address: Optional[str] = Field(title="")
    address_detail: Optional[str] = Field(title="주소 상세")
    lat: Optional[str] = Field(title="")
    lng: Optional[str] = Field(title="")
    subtitle: Optional[str] = Field(title="부제목")
    view_inventory: Optional[str] = Field(title="재고 노출여부")
    view_end_time: Optional[str] = Field(title="판매 종료시간 노출여부")
    reject: Optional[str] = Field(title="반려 사유")
    pg_provider: Optional[str] = Field(title="PG사 선택, 구분자 |, 없으면 전체")
    api_provider: Optional[str] = Field(title="외부업체 연동 구분")
    api_goods_id: Optional[str] = Field(title="외부업체 상품 ID")
    use_place: Optional[str] = Field(title="E쿠폰 사용처")
    user_limit_reset: Optional[str] = Field(title="1인당 구매횟수 제한 초기화 방법")
    resale: Optional[str] = Field(title="사입 여부")

    member: Optional[DataMember]
    categories: Optional[List[DataSimpleCategory]]
    brands: Optional[List[DataSimpleBrand]]
    common_info: Optional[DataCommonInfo]
    shipping_info: Optional[DataShippingInfo]
    options: Optional[List[DataProductOption]]
    photos: Optional[List[DataProductPhoto]]
    badges: Optional[List[DataSimpleBadge]]

    class Config:
        orm_mode = True


class DataProductList(BaseModel):
    id: int
    member_id: int = Field(title="PA id (정산 대상자)")
    name: str = Field(title="상품명")
    type: Optional[str] = Field(title="")
    status: str
    view_yn: Optional[str] = Field(title="노출 여부")
    code: Optional[str] = Field(title="상품코드")
    summary: Optional[str] = Field(title="요약 설명")
    keyword: Optional[str] = Field(title="검색 키워드")
    contents: Optional[str] = Field(title="내용")
    tax: Optional[str] = Field(title="과세여부")
    min_purchase_limit: Optional[str] = Field(title="최소 구매 수량")
    max_purchase_limit: Optional[str] = Field(title="최대 구매 수량")
    adult: Optional[str] = Field(title="성인인증 필요")
    hscode: Optional[str] = Field(title="")
    reg_date: datetime
    mod_date: datetime
    ipcc_yn: Optional[str] = Field(title="개인통관번호 여부")
    cancel_yn: Optional[str] = Field(title="취소 가능 여부")
    confirm: Optional[str] = Field(title="관리자 승인 여부")
    video: Optional[str] = Field(title="동영상 링크")
    memo: Optional[str] = Field(title="메모")
    common_info_id: Optional[int] = Field(title="공통정보 id")
    shipping_info_id: Optional[int] = Field(title="배송그룹 id")
    inven_use: str = Field(title="간편 재고 사용 여부")
    coupon_yn: str = Field(title="쿠폰 사용 여부")
    option_use: str = Field(title="옵션 사용 여부")
    barcode: Optional[str] = Field(title="배송그룹 id")
    user_limit: Optional[int] = Field(title="1인당 구매횟수 제한")
    use_end_period: Optional[int] = Field(title="비실물 상품 사용 기한 (일)")
    use_end_date: Optional[datetime] = Field(title="비실물 상품 사용 기한 (지정 일시)")
    sale_start_date: Optional[datetime] = Field(title="판매 가능 시간 시작")
    sale_end_date: Optional[datetime] = Field(title="판매 가능 시간 종료")
    sale_start_time: Optional[time] = Field(title='판매 가능 일(시각) 시작')
    sale_end_time: Optional[time] = Field(title='판매 가능 일(시각) 종료')
    subtitle: Optional[str] = Field(title="부제목")
    view_inventory: Optional[str] = Field(title="재고 노출여부")
    view_end_time: Optional[str] = Field(title="판매 종료시간 노출여부")
    api_provider: Optional[str] = Field(title="외부업체 연동 구분")
    api_goods_id: Optional[str] = Field(title="외부업체 상품 ID")
    use_place: Optional[str] = Field(title="E쿠폰 사용처")
    resale: Optional[str] = Field(title="사입 여부")
    pg_provider: Optional[str] = Field(title="PG사 선택, 구분자 |, 없으면 전체")

    member: Optional[DataMember]
    options: Optional[List[DataProductOption]]
    photos: Optional[List[DataProductPhoto]]

    class Config:
        orm_mode = True


class ModProductStatus(BaseModel):
    status: str
    product_ids: List[str]


class ModProduct(BaseModel):
    name: Optional[str] = Field(title="PA id (정산 대상자)")
    type: Optional[str] = Field(title="상품명")
    status: Optional[str] = Field(title="")
    view_yn: Optional[str] = Field(title="노출 여부")
    summary: Optional[str] = Field(title="요약 설명")
    keyword: Optional[str] = Field(title="검색 키워드")
    contents: Optional[str] = Field(title="내용")
    tax: Optional[str] = Field(title="과세여부")
    min_purchase_limit: Optional[str] = Field(title="최소 구매 수량")
    max_purchase_limit: Optional[str] = Field(title="최대 구매 수량")
    adult: Optional[str] = Field(title="성인인증 필요")
    hscode: Optional[str] = Field(title="")
    ipcc_yn: Optional[str] = Field(title="개인통관번호 여부")
    cancel_yn: Optional[str] = Field(title="취소 가능 여부")
    confirm: Optional[str] = Field(title="관리자 승인 여부")
    video: Optional[str] = Field(title="동영상 링크")
    memo: Optional[str] = Field(title="메모")
    common_info_id: Optional[int] = Field(title="공통정보 id")
    shipping_info_id: Optional[int] = Field(title="배송그룹 id")
    inven_use: Optional[str] = Field(title="간편 재고 사용 여부")
    coupon_yn: Optional[str] = Field(title="쿠폰 사용 여부")
    option_use: Optional[str] = Field(title="옵션 사용 여부")
    barcode: Optional[str] = Field(title="배송그룹 id")
    user_limit: Optional[int] = Field(title="1인당 구매횟수 제한")
    use_end_period: Optional[int] = Field(title="비실물 상품 사용 기한 (일)")
    use_end_date: Optional[Union[datetime, str]] = Field(title="비실물 상품 사용 기한 (지정 일시)")
    sale_start_date: Optional[Union[datetime, str]] = Field(title="판매 가능 시간 시작")
    sale_end_date: Optional[Union[datetime, str]] = Field(title="판매 가능 시간 종료")
    sale_start_time: Optional[Union[time, str]] = Field(title='판매 가능 일(시각) 시작')
    sale_end_time: Optional[Union[time, str]] = Field(title='판매 가능 일(시각) 종료')
    tel: Optional[str] = Field(title="")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="주소 상세")
    lat: Optional[str] = Field(title="")
    lng: Optional[str] = Field(title="")
    subtitle: Optional[str] = Field(title="부제목")
    view_inventory: Optional[str] = Field(title="재고 노출여부")
    view_end_time: Optional[str] = Field(title="판매 종료시간 노출여부")
    reject: Optional[str] = Field(title="반려 사유")
    pg_provider: Optional[str] = Field(title="PG사 선택, 구분자 |, 없으면 전체")
    api_provider: Optional[str] = Field(title="외부업체 연동 구분")
    api_goods_id: Optional[str] = Field(title="외부업체 상품 ID")
    use_place: Optional[str] = Field(title="E쿠폰 사용처")
    user_limit_reset: Optional[str] = Field(title="1인당 구매횟수 제한 초기화 방법")
    resale: Optional[str] = Field(title="사입 여부")


    _date_validator = validator('use_end_date', 'sale_start_date', 'sale_end_date', 'sale_start_time', 'sale_end_time', allow_reuse=True)(date_validator)


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
    product_id: int
    member_id: int
    title: str
    contents: str
    rating: Optional[float]
    order_info: Optional[str]


class ModProductReview(BaseModel):
    title: str
    contents: str
    rating: Optional[float]


class AddProductStoreMemo(BaseModel):
    memo: str
    product_id: int
    store_code: str


class DataProductStoreMemo(BaseModel):
    id: int
    memo: str
    product_id: int
    store_code: str
    member_id: int
    reg_date: datetime
    mod_date: datetime


class ModProductStoreMemo(BaseModel):
    memo: str


class DataSimpleProduct(BaseModel):
    id: Optional[int]
    name: Optional[str]
    code: Optional[str]
    type: Optional[str]
    status: Optional[str]
    view_yn: Optional[str]

    options: Optional[List[DataProductOption]]
    photos: Optional[List[DataProductPhoto]]

    class Config:
        orm_mode = True


class ListDataProduct(BaseModel):
    total: int
    datas: List[DataProductList]


class ListDataSimpleProduct(BaseModel):
    total: int
    datas: List[DataSimpleProduct]
