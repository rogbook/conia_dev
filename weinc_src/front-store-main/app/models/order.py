from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel


class AddOrderSheetProduct(BaseModel):
    product_option_id: int
    count: int


class AddOrderSheet(BaseModel):
    store_code: str
    type: str
    products: Optional[List[AddOrderSheetProduct]]
    carts: Optional[List[int]]


class OrderSheetCoupon(BaseModel):
    sheet_product_id: str
    coupon_id: Optional[int]


class AddOrder(BaseModel):
    id: int
    member_id: int
    store_code: str
    origin_order_id: Optional[int]
    raw_amount: Decimal
    final_amount: Decimal
    tex_free_amount: Decimal
    tax_rate: str
    discount: Decimal
    status: str
    deposit_yn: Optional[str]
    deposit_date: Optional[str]
    deposit_name: Optional[str]
    bank_account: Optional[str]
    virtual_account: Optional[str]
    virtual_date: Optional[datetime]
    pg_tid: Optional[str]
    pg_approval_number: Optional[str]
    cash_receipts_no: Optional[str]
    user_name: str
    user_phone: Optional[str]
    user_mobile: str
    user_email: str
    recipient_name: str
    recipient_phone: Optional[str]
    recipient_mobile: str
    shipping_type: str
    shipping_cost: str
    shipping_cost_post: str
    shipping_condition: str
    shipping_msg: Optional[str]
    zipcode: str
    address: str
    address_detail: str
    coupon_discount: Optional[Decimal]
    pg_provider: str
    pg_kind: str
    pg_tid: str
    step_type: str
    client_type: str
    referer: str
    referer_url: str
    total_ea: int
    total_kind: int
    ipcc_code: Optional[str]
    ip: str
    calculate_date: Optional[datetime]
    password: Optional[str]
    cert_id: Optional[int]


class DataOrder(BaseModel):
    id: int
    member_id: Optional[int]
    store_code: str
    origin_order_id: Optional[int]
    raw_amount: Decimal
    final_amount: Decimal
    tex_free_amount: Decimal
    tax_rate: str
    discount: Decimal
    status: str
    deposit_yn: Optional[str]
    deposit_date: Optional[str]
    deposit_name: Optional[str]
    bank_account: Optional[str]
    virtual_account: Optional[str]
    virtual_date: Optional[datetime]
    pg_tid: str
    pg_approval_number: str
    cash_receipts_no: str
    user_name: str
    user_phone: str
    user_mobile: str
    user_email: str
    recipient_name: str
    recipient_phone: str
    recipient_mobile: str
    shipping_type: str
    shipping_cost: str
    shipping_cost_post: str
    shipping_condition: str
    shipping_msg: str
    zipcode: str
    address: str
    address_detail: str
    coupon_discount: Decimal
    pg_provider: str
    pg_kind: str
    step_type: str
    reg_date: datetime
    mod_date: datetime
    session: str
    client_type: str
    referer: str
    referer_url: str
    total_ea: str
    total_kind: str
    ipcc_code: Optional[str]
    ip: str
    calculate_date: Optional[datetime]
    password: Optional[str]
    cert_id: Optional[int]

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


class ReqOrderRe(BaseModel):
    order_id: str
    order_products: str
    request_type: str
    request_reason: str


class Confirm(BaseModel):
    code: str
