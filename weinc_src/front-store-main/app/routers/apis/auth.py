import json
import re
import hashlib
from jose import jwt, ExpiredSignatureError, JWTError
from typing import List
from datetime import timedelta

import bcrypt
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.common.consts import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, AES_IV, AES_KEY, JWT_SECRET_KEY, JWT_ALGORITHM
from app.database.conn import db
from app.database.crud import Legacy
from app.database.schema import Customer, MemberStore, Store, Cert, SmsHistory
from app.errors import exceptions as exc
from app.models.auth import Token, Login, MemberToken, PasswordChange, TargetCheck, PasswordReset
from app.models.common import Success
from app.utils.date_utils import D
from app.utils.jwt import create_token, token_user
from app.utils.crypto_utils import AES256
from app.utils.sms import SMS

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=MemberToken, name="로그인")
def login(indata: Login, res: Response, session: Session = Depends(db.session)):
    member_token = login_proc(res, indata.email, indata.password, indata.store_code, session)
    return member_token


@router.post("/token", response_model=Token, name="Swagger 전용 토큰 생성")
def token(res: Response, session: Session = Depends(db.session), form_data: OAuth2PasswordRequestForm = Depends()):
    login_proc(res, form_data.username, form_data.password, "", session)
    return {"access_token": "string", "refresh_token": "string", "token_type": "bearer"}


@router.post("/target-check", name="패스워드 변경 대상 검증")
def target_check(indata: TargetCheck,
                 session: Session = Depends(db.session)):
    data: Cert = Cert.get(session, req_token_version_id=indata.token_version_id, status='Y')
    if not data:
        raise exc.CertFailEx

    v = AES256(AES_KEY, AES_IV).encrypt(data.mobileno)

    customer: Customer = session.query(Customer).filter(Customer.mobile == v, Customer.status == 'Y', Customer.email == indata.id).first()
    if not customer:
        raise exc.NotFoundDataEx

    pw_token = create_token({"sub": indata.id}, timedelta(minutes=30))

    return pw_token


@router.post("/password-reset", response_model=Success, name="패스워드 변경")
def password_reset(indata: PasswordReset,
                   session: Session = Depends(db.session)):

    try:
        payload = jwt.decode(indata.token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise exc.BadRequestEx
    except JWTError:
        raise exc.BadRequestEx

    customer: Customer = Customer.get(session, email=payload['sub'])
    hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
    customer.password = hash_pw
    customer.update(session, True, password=hash_pw)

    return Success()


@router.post("/password-change", response_model=Success, name="패스워드 변경")
def password_change(indata: PasswordChange,
                    session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    member: Customer = Customer.get(session, id=user.id)
    if not bcrypt.checkpw(indata.password.encode("utf8"), member.password.encode("utf8")):
        raise exc.NotMatchPWEx

    hash_pw = bcrypt.hashpw(indata.new_password.encode('utf8'), bcrypt.gensalt())
    member.password = hash_pw

    member.update(session, True, password=hash_pw)

    store = Store.get(session, code=indata.store_code)
    if store and member.mobile:
        mobile = AES256(AES_KEY, AES_IV).decrypt(member.mobile)
        sms = SMS()
        try:
            msg = f'[{store.title}]\n회원님의 패스워드가 정상적으로 변경 되었습니다.'
            res = sms.send(mobile, msg)

            sh = SmsHistory()
            sh.type = 'system'
            sh.mobile = member.mobile
            sh.body = msg
            sh.mid = res['mid']
            sh.provider = ''
            sh.customer_id = member.id
            sh.store_code = indata.store_code
            session.add(sh)
            session.commit()
        except:
            pass

    return Success()


@router.get("/logout", response_model=Success, name="로그아웃")
def logout(res: Response, user: MemberToken = Depends(token_user)):
    res.set_cookie('access_token', '', httponly=True)
    res.set_cookie('refresh_token', '', httponly=True)
    return Success()


@router.delete("/unlink", response_model=Success, name="소셜로그인 연결 해제")
def sns_unlink(service: str,
               session: Session = Depends(db.session),
               user: MemberToken = Depends(token_user)):
    customer = Customer.get(session=session, id=user.id)

    if service == 'naver':
        customer.sns_naver = None
    elif service == 'kakao':
        customer.sns_kakao = None
    elif service == 'payco':
        customer.sns_payco = None
    elif service == 'google':
        customer.sns_google = None
    elif service == 'apple':
        customer.sns_apple = None
    session.commit()

    return Success()


def login_proc(res: Response, user_id: str, user_pw: str, store_code: str, session: Session) -> MemberToken:
    """
    로그인 프로세스 단일화
    :param res:
    :param user_id:
    :param user_pw:
    :param session:
    :return:
    """
    if not is_valid_email(user_id):
        ldb = Legacy()
        res = ldb.execute(f"""
SELECT BL.LOGIN_ID
     , BL.PASSWD
     , PL.LOGIN_ID AS SHOP_ID
     , BU.MOBILE_NO
     , BU.EMAIL_ADDRESS
     , BU.USER_NAME
FROM BAS_LOGIN BL
INNER JOIN BAS_USER BU
ON BL.USER_ID = BU.USER_ID
INNER JOIN BAS_SALES_CUSTOMER SC
ON BU.USER_ID = SC.CUSTOMER_USER_ID
LEFT JOIN BAS_SALES_ORGANIZATION RG
ON SC.SALES_GROUP_ID = RG.SALES_GROUP_ID
AND RG.SALES_USER_ID = (IF(SC.CUSTOMER_TYPE = 'ME', SC.RECOMMEND_USER_ID, SC.CUSTOMER_USER_ID))
LEFT JOIN BAS_SALES_GROUP SG
ON RG.SALES_GROUP_ID = SG.SALES_GROUP_ID
LEFT JOIN BAS_CODE BC
ON BC.CODE_KEY = 'SYS_0013' AND BU.USER_TYPE = BC.CODE_ID
LEFT JOIN BAS_SALES_SHOP SS
ON RG.SHOP_ID = SS.SHOP_ID
LEFT JOIN BAS_USER PU
ON PARENT_USER_ID = PU.USER_ID
LEFT JOIN BAS_LOGIN PL
ON PU.USER_ID = PL.USER_ID
WHERE BL.LOGIN_ID = '{user_id}'""")
        row = res.fetchone()
        if row:
            if hash_sha256(user_pw) != row.PASSWD:
                raise exc.LegacyPWEx

            if store_code != row.SHOP_ID:
                raise exc.LegacyPWEx

            target_data = {
                "LOGIN_ID": row.LOGIN_ID,
                "PASSWD": row.PASSWD,
                "SHOP_ID": row.SHOP_ID,
                "EMAIL_ADDRESS": row.EMAIL_ADDRESS,
                "MOBILE_NO": str(row.MOBILE_NO).replace('-', ''),
                "USER_NAME": row.USER_NAME,
            }

            data = AES256(AES_KEY, AES_IV).encrypt(json.dumps(target_data, ensure_ascii=False))

            raise exc.LegacyUserEx(data=data)
        else:
            raise exc.LegacyPWEx

    member = Customer.get(session, email=user_id)
    if not member:
        error = exc.CheckLoginEx
        raise error
    if not bcrypt.checkpw(user_pw.encode("utf8"), member.password.encode("utf8")):
        raise exc.CheckLoginEx
    if member.status == 'E':
        raise exc.NotCertEmailEx
    if member.status == 'D':
        raise exc.CheckLoginEx
    if member.status != 'Y':
        raise exc.DisableUserEx

    if store_code:
        store = Store.get(session, code=store_code)
        if store.type == "C":  # 폐쇄몰 일 경우
            ms = MemberStore.get(session, customer_id=member.id, store_code=store_code)
            if ms:
                if ms.confirm == "N":
                    raise exc.ReadyConfirmEx
            else:
                if store.able_target_use in ["Y", "A", "F"]:
                    raise exc.ReadyConfirmUniqueEx
                else:
                    raise exc.PermissionEx

    member.lastlogin_date = D().now
    member.login_cnt += 1
    session.commit()

    able_store: List[MemberStore] = MemberStore.filter(session, customer_id=member.id, confirm="Y").all()
    able_store_list = []
    for row in able_store:
        able_store_list.append(row.store_code)

    token_data: MemberToken = MemberToken.from_orm(member)
    token_data.store_code = able_store_list

    access_token = create_token(token_data.dict(), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(token_data.dict(), timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    res.set_cookie('access_token', access_token, httponly=True, expires=3600*24*365*10)
    res.set_cookie('refresh_token', refresh_token, httponly=True, expires=3600*24*365*10)

    return member


def login_sns(res: Response, member: Customer, store_code: str, session: Session) -> MemberToken:
    """
    로그인 프로세스 단일화
    :param res:
    :param member:
    :param session:
    :return:
    """
    if not member:
        error = exc.NotMatchSnsEx(store_code=store_code)
        raise error

    if store_code:
        store = Store.get(session, code=store_code)
        if store.type == "C":  # 폐쇄몰 일 경우
            ms = MemberStore.get(session, customer_id=member.id, store_code=store_code)
            if ms:
                if ms.confirm == "N":
                    raise exc.ReadyConfirmEx
            else:
                if store.able_target_use in ["Y", "A", "F"]:
                    raise exc.ReadyConfirmUniqueEx
                else:
                    raise exc.PermissionEx

    member.lastlogin_date = D().now
    member.login_cnt += 1
    session.commit()

    able_store: List[MemberStore] = MemberStore.filter(session, customer_id=member.id, confirm="Y").all()
    able_store_list = []
    for row in able_store:
        able_store_list.append(row.store_code)

    token_data: MemberToken = MemberToken.from_orm(member)
    token_data.store_code = able_store_list

    access_token = create_token(token_data.dict(), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(token_data.dict(), timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    res.set_cookie('access_token', access_token, httponly=True, expires=3600*24*365*10)
    res.set_cookie('refresh_token', refresh_token, httponly=True, expires=3600*24*365*10)

    return member


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


def hash_sha256(data):
    return hashlib.sha256(data.encode("utf-8")).hexdigest()
