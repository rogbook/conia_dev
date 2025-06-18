from typing import List
import json
import bcrypt
from fastapi import APIRouter, Depends, Request, Query, Response
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.common.consts import AES_KEY, AES_IV
from app.database.conn import db
from app.database.schema import Customer, DeliveryAddress, MemberStore, EmailHistory, Store, CouponGroup, Coupon
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, CreatedID, Exist
from app.models.customer import DataCustomer, AddCustomer, ModCustomer, AddDeliveryAddress, DataDeliveryAddress, ModDeliveryAddress, SingOut
from app.utils.common_utils import get_ip
from app.utils.crypto_utils import AES256
from app.utils.jwt import token_user
from app.utils.aws import SES
from app.utils.date_utils import D
from app.common.config import conf

router = APIRouter(prefix='/customer')


@router.post("", response_model=CreatedID, name="회원 등록")
def add_member(indata: AddCustomer, req: Request,
               store_code: str = Query(None, description=""),
               session: Session = Depends(db.session)):
    is_exist = is_email_exist(indata.email)
    if is_exist:
        raise exc.AlreadyUserEx
    ip = get_ip(req)

    hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
    if indata.mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
        indata.mobile = enc_mobile
    indata.password = hash_pw
    indata.status = "E"

    indata_dict = indata.dict()
    if indata.legacy:
        dec_str = AES256(AES_KEY, AES_IV).decrypt(indata.legacy)
        legacy_user_data = json.loads(dec_str)
        indata_dict['legacy_id'] = legacy_user_data['LOGIN_ID']
        indata_dict['legacy_pw'] = legacy_user_data['PASSWD']
        indata_dict['legacy_shop'] = legacy_user_data['SHOP_ID']

    data = Customer.create(session, auto_commit=True, **indata_dict)

    if not indata.legacy and store_code:
        store = session.query(Store).filter(Store.code == store_code).first()
        if store:
            if store.able_target_use == 'E':
                domain = indata.email.split('@')[-1]
                if domain and domain == store.verify_code:
                    ms = MemberStore()
                    ms.customer_id = data.id
                    ms.store_code = store_code
                    ms.value = "EMAIL_CERT"
                    ms.confirm = "Y"
                    session.add(ms)
                    session.commit()

    if indata.name and indata.mobile and indata.address and indata.address_detail and indata.zipcode:
        default_delivery = AddDeliveryAddress(title="기본배송지",
                                              name=indata.name,
                                              address=indata.address,
                                              address_detail=indata.address_detail,
                                              zipcode=indata.zipcode,
                                              mobile=indata.mobile,
                                              default_yn="Y")
        DeliveryAddress.create(session=session, auto_commit=True, customer_id=data.id, **default_delivery.dict())

    if indata.legacy:
        dec_str = AES256(AES_KEY, AES_IV).decrypt(indata.legacy)
        legacy_user_data = json.loads(dec_str)

        ms = MemberStore()
        ms.customer_id = data.id
        ms.store_code = legacy_user_data['SHOP_ID']
        ms.value = "LEGACY_SYSTEM"
        ms.confirm = "Y"
        session.add(ms)
        session.commit()

    # email = SendEmail()
    ses = SES()

    enc = AES256(AES_KEY, AES_IV).encrypt(f"{store_code},customer,{data.id}")
    c = conf()
    store = Store.get(session=session, code=store_code)
    email_body = f"""
<html>
<body style='font-size:16px;'>
    <div style='font-size:24px; font-weight:bold; text-align:center; padding-top:30px;'>환영합니다. <span style='color:#e24502;'>이메일</span>을 인증해 주세요.</div>
    <div style='margin:30px 0 60px; color:#676565; text-align:center;'>
회원가입 완료를 위한 이메일 인증을 진행해주세요.<br>본인이 요청하신 내용이 아니면 무시하세요.
    </div>
    <a href='{c.API_HOST}/auth/cert-email/{enc}' style='display:block; width:364px; margin:auto; padding:12px 0; background:#e24502; color:#fff; text-align:center; text-decoration:none;'>이메일 인증하기</a>
    <div style='margin:30px 0 30px;'>
본 메일은 발신전용이며, 회신이 되지 않습니다.<br>
추가 문의사항은 고객센터(1644-7370)를 통해서 문의하여 주시기 바랍니다.<br>
Copyright © ConiaLab Corp. All rights reserved.
    </div>
</body>
</html>
"""
    # email.send(to=indata.email, subject=f"[{store.title}] 이메일 인증을 위한 안내메일 입니다.", body=email_body)
    ses.send_email(to=indata.email, subject=f"[{store.title}] 이메일 인증을 위한 안내메일 입니다.", message=email_body)

    history = EmailHistory()
    history.customer_id = data.id
    history.type = 'cert'
    history.to = indata.email
    history.title = f"[{store.title}] 이메일 인증을 위한 안내메일 입니다."
    history.body = email_body
    history.provider = "ses"
    history.store_code = store_code
    session.add(history)
    session.commit()

    coupon_groups = session.query(CouponGroup).filter(CouponGroup.status == 'Y', CouponGroup.auto == '회원가입').all()
    for coupon_group in coupon_groups:
        now = D().now
        if coupon_group.publish_begin_date and coupon_group.publish_begin_date > now:
            continue
        if coupon_group.publish_end_date and coupon_group.publish_end_date < now:
            continue

        if coupon_group.publish_limit:
            published_coupon_cnt = Coupon.filter(session, coupon_group_id=coupon_group.id).count()
            if 1 > (coupon_group.publish_limit - published_coupon_cnt):
                continue

        publishing_coupon(session, coupon_group, data.id)

    return CreatedID(id=data.id)


@router.get("/exist", response_model=Exist, name="회원 중복 확인")
def check_member(email: EmailStr):
    is_exist = is_email_exist(email)
    return Exist(exist=is_exist)


@router.get("", response_model=DataCustomer, name="회원 정보(본인)")
def get_member_me(session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    member = Customer.get(session=session, id=user.id)
    return member


@router.put("", response_model=Success, name="회원 수정(본인)")
def update_me(indata: ModCustomer, session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    # 본인인증 및 성인인증 변경시 검증 프로세스 필요

    data: Customer = Customer.get(session=session, id=user.id)
    if not data:
        raise exc.NotFoundDataEx

    if indata.password:
        hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
        indata.password = hash_pw

    if indata.mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
        indata.mobile = enc_mobile

    data.update_optional(session, True, **indata.dict())

    return Success()


@router.post("/signout", response_model=Success, name="회원 탈퇴")
def signout(indata: SingOut,
            res: Response,
            session: Session = Depends(db.session),
            user: MemberToken = Depends(token_user)):
    data: Customer = Customer.get(session=session, id=user.id)
    if not data:
        raise exc.NotFoundDataEx

    if indata.passwd:
        if not bcrypt.checkpw(indata.passwd.encode("utf8"), data.password.encode("utf8")):
            raise exc.CheckLoginEx

    data.status = 'D'
    session.commit()

    res.set_cookie('access_token', '', httponly=True)
    res.set_cookie('refresh_token', '', httponly=True)

    return Success()


@router.post("/delivery-address", response_model=CreatedID, name="배송지 추가")
def add_delivery_address(indata: AddDeliveryAddress,
                         session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    if indata.default_yn == 'Y':
        DeliveryAddress.filter(session, customer_id=user.id, default_yn='Y').update_q(auto_commit=True, default_yn='N')

    indata.mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
    data = DeliveryAddress.create(session=session, auto_commit=True, customer_id=user.id, **indata.dict())

    return CreatedID(id=data.id)


@router.get("/delivery-address", response_model=List[DataDeliveryAddress], name="배송지 목록")
def list_delivery_address(customer_id: int,
                          session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    if customer_id != user.id:
        raise exc.PermissionEx

    list_data = DeliveryAddress.filter(session=session, customer_id=user.id).all()
    return list_data


@router.get("/delivery-address/{address_id}", response_model=DataDeliveryAddress, name="배송지")
def get_delivery_address(address_id: str,
                         session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    data = DeliveryAddress.get(session=session, customer_id=user.id, id=address_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/delivery-address/{address_id}", response_model=Success, name="배송지 수정")
def mod_delivery_address(address_id: int, indata: ModDeliveryAddress,
                         session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    data: DeliveryAddress = DeliveryAddress.get(session=session, id=address_id)
    if not data:
        raise exc.NotFoundDataEx

    if data.customer_id != user.id:
        raise exc.PermissionEx

    if indata.default_yn == 'Y':
        DeliveryAddress.filter(session, customer_id=user.id, default_yn='Y').update_q(auto_commit=True, default_yn='N')

    if indata.mobile:
        indata.mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)

    data.update_optional(session=session, auto_commit=True, **indata.dict())
    return Success()


@router.delete("/delivery-address/{address_id}", response_model=Success, name="배송지 삭제")
def del_delivery_address(address_id: int,
                         session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    data: DeliveryAddress = DeliveryAddress.get(session=session, id=address_id)
    if not data:
        raise exc.NotFoundDataEx

    if data.customer_id != user.id:
        raise exc.PermissionEx

    session.delete(data)
    session.commit()

    return Success()


def is_email_exist(email: str):
    """
    회원 계정 중복 체크
    :param email:
    :return:
    """
    get_email = Customer.get(email=email)
    if get_email:
        return True
    return False


def generate_random_string(length):
    import string
    import random
    letters = string.ascii_letters  # 알파벳 (소문자 및 대문자)
    numbers = string.digits  # 숫자
    all_characters = letters + numbers  # 모든 문자

    random_string = ''.join(random.choice(all_characters) for _ in range(length))
    return random_string


def publishing_coupon(session: Session, group: CouponGroup, customer_id: int):
    data = Coupon()
    data.code = generate_random_string(10)
    data.name = group.name
    data.description = group.description

    if group.expire_days:
        data.end_date = D().add_day_last_hour(group.expire_days)
    else:
        data.begin_date = group.begin_date
        data.end_date = group.end_date

    data.amount = group.amount
    data.percent = group.percent

    data.min_price = group.min_price
    data.max_price = group.max_price

    data.issuer = group.issuer
    data.coupon_group_id = group.id
    data.target = group.target
    data.type = group.type
    data.customer_id = customer_id
    data.product_id = group.product_id

    session.add(data)
    session.commit()
