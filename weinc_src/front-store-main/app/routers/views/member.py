import json
from typing import List
from pydantic import parse_obj_as

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, DeliveryAddress, Customer, WishProduct, Coupon
from app.models.auth import MemberToken
from app.models.customer import DataCustomer, DataDeliveryAddress
from app.models.coupon import DataCoupon
from app.utils.common_utils import check_store, make_view_context_data, get_base_url
from app.utils.jwt import token_user
from app.utils.templates import templates
from app.utils.date_utils import D
from app.common.consts import AES_IV, AES_KEY
from app.utils.crypto_utils import AES256

router = APIRouter(prefix="/member")


@router.get("/signup")
def signup(req: Request, store_code: str,
           data: str = Query(default=None),
           session: Session = Depends(db.session),
           store: Store = Depends(check_store)):
    context_data = make_view_context_data(session, req, store)
    context_data.update(base_url=get_base_url(req))

    if data:
        dec_data = AES256(AES_KEY, AES_IV).decrypt(data)
        context_data.update(legacy_user_data=json.loads(dec_data))

    return templates.TemplateResponse("account-signup.html", context=context_data)


@router.get("/signout")
def signout(req: Request, store_code: str,
            session: Session = Depends(db.session),
            store: Store = Depends(check_store),
            user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    return templates.TemplateResponse("account-signout.html", context=context_data)


@router.get("/profile")
def profile(req: Request, store_code: str,
            store: Store = Depends(check_store),
            session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    member = Customer.get(session, id=user.id)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(member=DataCustomer.from_orm(member))
    context_data.update(base_url=get_base_url(req))

    return templates.TemplateResponse("account-profile.html", context=context_data)


@router.get("/password")
def profile(req: Request, store_code: str,
            store: Store = Depends(check_store),
            session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    return templates.TemplateResponse("account-password-change.html", context=context_data)


@router.get("/address")
def my_address(req: Request, store_code: str,
               store: Store = Depends(check_store),
               session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    address: List[DeliveryAddress] = DeliveryAddress.filter(session=session, customer_id=user.id).order_by("-default_yn").all()

    address_obj = parse_obj_as(List[DataDeliveryAddress], address)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(address=address_obj)

    return templates.TemplateResponse("account-address.html", context=context_data)


@router.get("/address/edit")
def my_address(req: Request, store_code: str,
               address_id: int = Query(default=None),
               store: Store = Depends(check_store),
               session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    if address_id:
        address = DeliveryAddress.get(session=session, customer_id=user.id, id=address_id)
        address = DataDeliveryAddress.from_orm(address)
    else:
        address = None

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(address=address)

    return templates.TemplateResponse("account-address-edit.html", context=context_data)


@router.get("/coupon")
def coupon(req: Request, store_code: str,
           store: Store = Depends(check_store),
           session: Session = Depends(db.session),
           user: MemberToken = Depends(token_user)):
    coupons: List[Coupon] = session.query(Coupon).filter(Coupon.customer_id == user.id).order_by(Coupon.reg_date.desc()).all()

    coupon_able = []
    coupon_disable = []

    now = D().now
    for row in coupons:
        data = DataCoupon.from_orm(row)
        if data.coupon_group.coupon_target:
            pa_list = []
            prd_list = []

            for row in data.coupon_group.coupon_target:
                if row.member_id:
                    pa_list.append(row.member_id)
                elif row.product_id:
                    prd_list.append(row.product_id)
            if pa_list:
                data.target_pa_str = ','.join(pa_list)
            if prd_list:
                data.target_prd_str = ','.join(prd_list)

        if data.use_yn == 'Y':
            data.status = 'USE'
            coupon_disable.append(data)
            continue

        if data.end_date and data.end_date < now:
            data.status = 'DE'
            coupon_disable.append(data)
            continue

        if data.begin_date and data.begin_date > now:
            data.status = 'DS'
            coupon_disable.append(data)
            continue

        coupon_able.append(data)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(coupon_able=coupon_able)
    context_data.update(coupon_disable=coupon_disable)

    return templates.TemplateResponse("account-coupons.html", context=context_data)
