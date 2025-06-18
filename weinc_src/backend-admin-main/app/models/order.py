from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List

from app.models.common import ListData


class DataOrderShipping(BaseModel):
    id: int
    provider: Optional[str]
    provider_code: Optional[str]
    number: Optional[str]
    status: str
    cost: int
    shipping_type: str
    pay_type: str
    order_id: str
    member_id: int
    shipping_info_id: int
    number_reg_date: Optional[datetime]
    complete_date: Optional[datetime]

    class Config:
        orm_mode = True


class DataEcoupon(BaseModel):
    provider: Optional[str]
    goods_id: Optional[str]
    tr_id: Optional[str]
    pin_code: Optional[str]
    period_date: Optional[datetime]
    status: Optional[str]
    reg_date: Optional[datetime]
    mod_date: Optional[datetime]
    kind: Optional[str]
    duty_code: Optional[str]
    raw_data: Optional[str]

    class Config:
        orm_mode = True


class DataOrderProduct(BaseModel):
    id: int
    order_id: str
    origin_order_id: Optional[str]
    product_id: int
    product_option_id: int
    ea: int
    amount: Decimal
    status: str
    seller_title: str
    product_name: str
    product_code: str
    product_description: str
    product_thumbnail: str
    origin_price: Decimal
    order_shipping_id: Optional[int]
    member_id: int
    order_date: Optional[datetime]
    pg_date: Optional[datetime]
    pg_kind: Optional[str]
    pg_cancel_disable: Optional[str]
    user_name: Optional[str]
    user_phone: Optional[str]
    user_mobile: Optional[str]
    recipient_name: Optional[str]
    recipient_mobile: Optional[str]
    shipping_msg: Optional[str]
    zipcode: Optional[str]
    address: Optional[str]
    address_detail: Optional[str]
    user_email: Optional[str]
    store_name: Optional[str]
    store_code: Optional[str]
    product_option_name: Optional[str]
    type: Optional[str]
    discount: Optional[Decimal]
    use_end_date: Optional[datetime]
    complete_date: Optional[datetime]
    balance: Optional[int]
    ecoupon: Optional[DataEcoupon]

    order_shipping: Optional[DataOrderShipping]

    class Config:
        orm_mode = True


class ListDataOrderProduct(BaseModel):
    total: int
    datas: List[DataOrderProduct]


class PgInfoSub(BaseModel):
    # id: Optional[int]
    # pg_info_id: Optional[int]
    kind: Optional[str]
    amount: Optional[int]
    # tno: Optional[int]

    class Config:
        orm_mode = True


class PgInfo(BaseModel):
    order_id: str
    provider: str
    kind: str
    tid: str
    app_time: datetime
    deposit_yn: Optional[str]
    deposit_date: Optional[datetime]
    deposit_name: Optional[str]
    bank_account: Optional[str]
    virtual_account: Optional[str]
    virtual_date: Optional[datetime]
    card_app_num: Optional[str]
    card_name: Optional[str]
    card_no: Optional[str]
    card_quota: Optional[str]
    card_partcanc_yn: Optional[str]
    card_bin_type_01: Optional[str]
    card_bin_type_02: Optional[str]
    cash_authno: Optional[str]
    cash_no: Optional[str]
    bankname: Optional[str]
    commid: Optional[str]
    mobile_no: Optional[str]

    pg_info_sub: Optional[List[PgInfoSub]]

    class Config:
        orm_mode = True


class DataPgCancel(BaseModel):
    id: int
    pg_info_order_id: str
    tno: str
    type: str
    reg_date: datetime
    amount: int
    remain: Optional[int]
    part_seq: Optional[str]

    class Config:
        orm_mode = True


class DataOrder(BaseModel):
    id: int
    customer_id: int
    store_code: str
    origin_order_id: Optional[int]
    origin_amount: Optional[Decimal]
    raw_amount: Decimal
    final_amount: Decimal
    tex_free_amount: Optional[Decimal]
    tax_rate: Optional[Decimal]
    discount: Optional[Decimal]
    status: str
    user_name: str
    user_phone: Optional[str]
    user_mobile: str
    user_email: str
    recipient_name: str
    recipient_phone: Optional[str]
    recipient_mobile: str
    shipping_cost: Decimal
    shipping_cost_post: Optional[Decimal]
    shipping_condition: Optional[str]
    shipping_msg: Optional[str]
    zipcode: str
    address: str
    address_detail: str
    coupon_discount: Optional[Decimal]
    step_type: str
    reg_date: datetime
    mod_date: datetime
    client_type: str
    referer: Optional[str]
    referer_url: Optional[str]
    total_ea: int
    total_kind: int
    ipcc_code: Optional[str]
    ip: Optional[str]
    calculate_date: Optional[datetime]
    password: Optional[str]
    cert_id: Optional[int]
    pg_cancel_disable: Optional[str]

    products: List[DataOrderProduct]
    pg_info: Optional[PgInfo]

    class Config:
        orm_mode = True


class ModOrder(BaseModel):
    status: Optional[str]
    deposit_yn: Optional[str]
    deposit_date: Optional[str]
    deposit_name: Optional[str]
    bank_account: Optional[str]
    virtual_account: Optional[str]
    virtual_date: Optional[datetime]
    pg_tid: Optional[str]
    pg_approval_number: Optional[str]
    cash_receipts_no: Optional[str]
    user_name: Optional[str]
    user_phone: Optional[str]
    user_mobile: Optional[str]
    user_email: Optional[str]
    recipient_name: Optional[str]
    recipient_phone: Optional[str]
    recipient_mobile: Optional[str]
    shipping_type: Optional[str]
    shipping_cost: Optional[str]
    shipping_cost_post: Optional[str]
    shipping_condition: Optional[str]
    shipping_msg: Optional[str]
    zipcode: Optional[str]
    address: Optional[str]
    address_detail: Optional[str]
    coupon_discount: Optional[Decimal]
    pg_provider: Optional[str]
    pg_kind: Optional[str]
    total_ea: Optional[str]
    total_kind: Optional[str]
    ipcc_code: Optional[str]
    calculate_date: Optional[datetime]


class ModShipping(BaseModel):
    delivery_code: str
    delivery_provider: str
    delivery_provider_code: str


class DataOrderReParent(BaseModel):
    id: int
    order_id: str
    type: str
    contents: str
    category: Optional[str]
    memo: Optional[str]
    status: str
    reg_date: datetime
    mod_date: Optional[datetime]
    end_date: Optional[datetime]
    refund_amount: Optional[int]
    pay_type: str
    refund_date: Optional[datetime]
    log: str

    class Config:
        orm_mode = True


class DataOrderRe(BaseModel):
    reg_date: Optional[datetime]
    end_date: Optional[datetime]

    parent: DataOrderReParent
    product: DataOrderProduct

    class Config:
        orm_mode = True


class ListDataOrderRe(BaseModel):
    total: int
    datas: List[DataOrderRe]


class CancelPartOrder(BaseModel):
    cancel_amount: Decimal
    order_product_ids: List[str]
    order_shipping_ids: List[str]


class ModRe(BaseModel):
    order_product_ids: List[str]
    status: str


class ModOrderStatus(BaseModel):
    status: str
    order_product_ids: List[str]


class DataMember(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class DataAdminRefund(BaseModel):
    id: int
    order_id: str
    product_name: str
    reg_date: datetime
    store_code: str
    store_name: str
    amount: int
    member_id: int
    customer_id: int

    member: DataMember
    customer: DataMember

    class Config:
        orm_mode = True


class ListAdminRefund(ListData):
    datas: Optional[List[DataAdminRefund]]
