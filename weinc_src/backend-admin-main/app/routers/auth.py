import json
from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
import random

from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.database.conn import db
from app.database.schema import Member, CertSms, MemberClass, ClassPermission, MemberWorker, DeptPermission, \
    MemberPermission, Store, MemberCompany, Cert, MenuClass, Menu, Customer
from app.database.crud import Auth

from app.errors import exceptions as exc
from app.utils.date_utils import D
from app.utils.crypto_utils import AES256
from app.utils.common_utils import get_ip
from app.utils.niceid import enc_req_data, dec_res_data
from app.utils.jwt import create_access_token, create_refresh_token, token_user, token_user_refresh, token_user_option

from app.models.common import Success
from app.models.auth import Token, Login, SnsLogin, CertSmsReq, CertSmsVerify, CertNiceIdReq, CertNiceId, MemberToken, \
    CertNiceIdResult, PasswordChange, FindId, ChangePassword, MenuList

from app.common.consts import CERT_SMS_ABLE_COUNT_MOBILE, CERT_SMS_ABLE_COUNT_IP, CERT_SMS_ABLE_TIME_MINUTE, RANDOM_STRING_POOL, AES_KEY, AES_IV
from app.common.template_string import CERT_SMS
from app.utils.log import L
from app.common.config import conf

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token, name="로그인")
def login(indata: Login, req: Request, session: Session = Depends(db.session)):
    member = id_pw_check(indata.email, indata.password, session)
    access_token, refresh_token = login_proc(member, session)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/sns_login", response_model=Token, name="SNS 로그인")
def sns_login(indata: SnsLogin, req: Request, session: Session = Depends(db.session)):
    member = None

    if indata.type == 'naver':
        member = Member.get(session, sns_naver=indata.token)
    elif indata.type == 'kakao':
        member = Member.get(session, sns_kakao=indata.token)
    elif indata.type == 'payco':
        member = Member.get(session, sns_payco=indata.token)
    elif indata.type == 'google':
        member = Member.get(session, sns_google=indata.token)
    elif indata.type == 'apple':
        member = Member.get(session, sns_apple=indata.token)

    if not member:
        raise exc.NotFoundUserEx(user_id=indata.type)

    if not (member.status == 'Y' or member.status == 'R'):
        raise exc.NotAvailableEx

    access_token, refresh_token = login_proc(member, session)
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/send-reset-password-mail", response_model=Success, name="패스워드 재설정 메일 전송")
def send_reset_password_mail(email: EmailStr, req: Request, session: Session = Depends(db.session)):
    member = Member.get(session, email=email)
    if not member:
        raise exc.NotFoundDataEx

    random_pw = ""
    for i in range(8):
        random_pw += random.choice(RANDOM_STRING_POOL)

    hash_pw = bcrypt.hashpw(random_pw.encode('utf8'), bcrypt.gensalt())
    member.password = hash_pw

    member.update(session, True, password=hash_pw)

    L().info(random_pw)

    # TODO : send email

    return Success()


@router.post("/token", response_model=Token, name="Swagger 전용 토큰 생성")
def token(req: Request, session: Session = Depends(db.session), form_data: OAuth2PasswordRequestForm = Depends()):
    member = id_pw_check(form_data.username, form_data.password, session)
    access_token, refresh_token = login_proc(member, session, scopes=form_data.scopes)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/password-change", response_model=Success, name="패스워드 변경")
def password_change(indata: PasswordChange,
                    session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    member: Member = Member.get(session, id=user.id)
    if not bcrypt.checkpw(indata.password.encode("utf8"), member.password.encode("utf8")):
        raise exc.NotMatchPWEx

    hash_pw = bcrypt.hashpw(indata.new_password.encode('utf8'), bcrypt.gensalt())
    member.password = hash_pw

    member.update(session, True, password=hash_pw)

    return Success()


@router.post("/password-change-cert", response_model=Success, name="패스워드 변경(본인인증)")
def password_change(indata: ChangePassword,
                    session: Session = Depends(db.session)):
    data: Cert = Cert.get(session, req_token_version_id=indata.token_version_id, status='Y')
    if not data:
        raise exc.CertFailEx

    member: Member = Member.get(session, email=indata.email_id)
    if not member:
        raise exc.NotFoundDataEx

    hash_pw = bcrypt.hashpw(indata.new_password.encode('utf8'), bcrypt.gensalt())
    member.password = hash_pw

    member.update(session, True, password=hash_pw)

    return Success()


@router.post("/find-id-cert", response_model=str, name="아이디 찾기(본인인증)")
def find_id(indata: FindId,
            session: Session = Depends(db.session)):
    data: Cert = Cert.get(session, req_token_version_id=indata.token_version_id, status='Y')
    if not data:
        raise exc.CertFailEx

    v = AES256(AES_KEY, AES_IV).encrypt(data.mobileno)

    member: Member = session.query(Member).filter(Member.mobile == v).first()
    if not member:
        raise exc.NotFoundUserEx

    return member.email


@router.post("/logout", response_model=Success, name="로그아웃")
def logout(session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    member = Member.get(session=session, id=user.id)
    member.refresh_token = ''
    session.commit()

    return Success()


@router.get("/menu", response_model=MenuList, name="사용 가능한 메뉴 목록")
def menu(session: Session = Depends(db.session),
         user: MemberToken = Depends(token_user)):
    if user.admin == "Y":
        data = MenuList(
            depth1=Menu.filter(session, depth=1).all(),
            depth2=Menu.filter(session, depth=2).all(),
            depth3=Menu.filter(session, depth=3).all(),
        )
    else:
        data = MenuList(
            depth1=session.query(Menu).join(MenuClass, Menu.id == MenuClass.menu_id).filter(Menu.depth == 1, MenuClass.class_code.in_(user.member_class)).group_by(Menu.id).all(),
            depth2=session.query(Menu).join(MenuClass, Menu.id == MenuClass.menu_id).filter(Menu.depth == 2, MenuClass.class_code.in_(user.member_class)).group_by(Menu.id).all(),
            depth3=session.query(Menu).join(MenuClass, Menu.id == MenuClass.menu_id).filter(Menu.depth == 3, MenuClass.class_code.in_(user.member_class)).group_by(Menu.id).all(),
        )

    return data


@router.get("/refresh-token", response_model=Token, name="Access Token 갱신")
def req_refresh_token(session: Session = Depends(db.session), user: Member = Depends(token_user_refresh)):
    member = Member.get(id=user.id)

    token_data = make_token_data(session, member)

    access_token = create_access_token(token_data.dict())

    return Token(access_token=access_token)


@router.post("/cert-sms-req", response_model=Success, name="인증 코드 요청(SMS)")
def cert_sms_req(indata: CertSmsReq, req: Request, session: Session = Depends(db.session)):
    ip = get_ip(req)

    m_cnt = Auth.get_cert_sms_count(session, mobile=indata.mobile)
    i_cnt = Auth.get_cert_sms_count(session, ip=ip)

    if m_cnt < CERT_SMS_ABLE_COUNT_MOBILE and i_cnt < CERT_SMS_ABLE_COUNT_IP:  # 하루 동일 번호 x회 동일 IP x회 제한
        last = CertSms.filter(session, type="CERT_SMS", mobile=indata.mobile).order_by("-reg_date").first()
        if last:
            if D.diff_min(D().now, last.reg_date) < CERT_SMS_ABLE_TIME_MINUTE:
                raise exc.RequestNotYetEx
    else:
        raise exc.RequestCountEx

    code = str(random.randint(100000, 999999))
    msg = CERT_SMS.format(code=code)

    # TODO : SMS 전송

    data = {
        "type": "CERT_SMS",
        "mobile": indata.mobile,
        "code": code,
        "ip": ip,
    }
    CertSms.create(session, True, **data)

    return Success()


@router.post("/cert-sms-verify", response_model=Success, name="인증 코드 검증(SMS)")
def cert_sms_verify(indata: CertSmsVerify, req: Request, session: Session = Depends(db.session)):
    data: CertSms = CertSms.filter(session, type="CERT_SMS", mobile=indata.mobile, code=indata.code, status="R").first()

    if data:
        if D.diff_min(D().now, data.reg_date) < CERT_SMS_ABLE_TIME_MINUTE:
            data.update(session, True, status="C")
            return Success()
        else:
            raise exc.CertFailEx("2")
    else:
        raise exc.CertFailEx("1")


@router.post("/cert-niceid", response_model=CertNiceId, name="본인인증 요청")
def cert_req_nice_id(indata: CertNiceIdReq, req: Request, session: Session = Depends(db.session), user: Member = Depends(token_user_option)):
    """
    Response Data 를 아래와 같이 form 을 이용 하여 실행
    ```
    <form name="form" id="form" action="https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb">
        <input type="hidden" id="m" name="m" value="service"/>
        <input type="hidden" id="token_version_id" name="token_version_id" value="{{ data.token_version_id }}"/>
        <input type="hidden" id="enc_data" name="enc_data" value="{{ data.enc_data }}"/>
        <input type="hidden" id="integrity_value" name="integrity_value" value="{{ data.integrity_value }}"/>
    </form>

    <script>
        window.onload = function () {
            document.getElementById('form').submit();
        }
    </script>
    """
    ip = get_ip(req)
    user_id = ""
    if user:
        user_id = user.id

    data = enc_req_data(receive_data=str(user_id), return_url=indata.return_url)
    key = data["key"]
    iv = data["iv"]
    token_version_id = data["token_version_id"]
    enc_data = data["enc_data"]
    integrity_value = data["integrity_value"]
    Cert.create(session, auto_commit=True,
                req_token_version_id=token_version_id,
                ip=ip,
                key=key,
                iv=iv)

    return CertNiceId(token_version_id=token_version_id, enc_data=enc_data, integrity_value=integrity_value)


@router.post("/cert-niceid-verify", response_model=CertNiceIdResult, name="본인인증 요청 결과 확인")
def cert_nice_id_verify(indata: CertNiceId, session: Session = Depends(db.session)):
    data: Cert = Cert.get(session, req_token_version_id=indata.token_version_id, status='R')
    if not data:
        raise exc.CertFailEx

    dec_data = dec_res_data(data.key, data.iv, indata.enc_data)
    cert_data = json.loads(dec_data)

    if cert_data['resultcode'] == '0000':
        if cert_data.get("receivedata", None):
            data.user_id = cert_data.get("receivedata")
        data.responseno = cert_data.get("responseno", None)
        data.authtype = cert_data.get("authtype", None)
        data.name = cert_data.get("name", None)
        data.utf8_name = cert_data.get("utf8_name", None)
        data.birthdate = cert_data.get("birthdate", None)
        data.gender = cert_data.get("gender", None)
        data.nationalinfo = cert_data.get("nationalinfo", None)
        data.mobileco = cert_data.get("mobileco", None)
        data.mobileno = cert_data.get("mobileno", None)
        data.ci = cert_data.get("ci", None)
        data.di = cert_data.get("di", None)
        data.status = "Y"
        session.commit()
    else:
        raise exc.CertFailEx

    return CertNiceIdResult(name=cert_data.get("name"), mobile=cert_data.get("mobileno"), birth=cert_data.get("birthdate"), gender=cert_data.get("gender"))


@router.get("/cert-email/{data}", response_model=CertNiceIdResult, name="이메일 인증")
def cert_email(data: str,
               session: Session = Depends(db.session)):
    try:
        dec_data: str = AES256(AES_KEY, AES_IV).decrypt(data)
    except:
        raise exc.BadRequestEx

    cert_data = dec_data.split(',')
    store_code = cert_data[0]
    user_type = cert_data[1]
    user_id = cert_data[2]
    return_url = ''
    c = conf()

    if user_type == "customer":
        user = session.query(Customer).filter(Customer.id == user_id).first()
        user.status = 'Y'
        session.commit()
        return_url = f"{c.STORE_HOST}/{store_code}"
    elif user_type == "member":
        user = session.query(Member).filter(Member.id == user_id).first()
        user.status = 'Y'
        session.commit()
        return_url = c.ADMIN_HOST

    return RedirectResponse(url=return_url)


def login_proc(member: Member, session: Session, **kwargs):
    """
    로그인 프로세스 단일화
    :param member:
    :param session:
    :return:
    """
    member.lastlogin_date = D().now
    member.login_cnt += 1

    token_data = make_token_data(session, member)

    access_token = create_access_token(token_data.dict())
    refresh_token = create_refresh_token(member, session)

    return access_token, refresh_token


def make_token_data(session: Session, member: Member):
    member_company = MemberCompany.get(session, member_id=member.id)
    company_id = member_company.id if member_company else 0

    member_class = MemberClass.filter(session, member_id=member.id).all()
    member_class_list = []
    if member_class:
        for row in member_class:
            member_class_list.append(row.class_code)

    token_data: MemberToken = MemberToken(id=member.id, name=member.name, email=member.email, company_id=company_id, partner=member.partner, member_class=member_class_list, status=member.status)

    # 권한
    pm = get_permission(session, member_id=member.id)
    token_data.scopes = pm

    # 소속 조직
    org = get_organization(session, member_id=member.id)
    token_data.organization = org

    token_data.admin = member.admin_yn

    store = Store.get(session, member_id=member.id)
    if store:
        token_data.store_code = store.code

    return token_data


def get_organization(session: Session, member_id: int):
    res = {}
    stores = Store.filter(session, member_id=member_id).all()
    if stores:
        res["my_store"] = []
        for store in stores:
            res["my_store"].append(store.code)

    companys: List[MemberCompany] = MemberCompany.filter(session, member_id=member_id).all()
    if companys:
        res["my_company"] = []
        for company in companys:
            res["my_company"].append(company.id)

    worker: List[MemberWorker] = session.query(MemberWorker).filter(MemberWorker.member_id == member_id).group_by(MemberWorker.member_company_id).all()
    if worker:
        res["owner_store"] = []
        res["owner_company"] = []
        for row in worker:
            res["owner_company"].append(row.member_company_id)
            owner_id = row.member_company.member_id
            stores = Store.filter(session, member_id=owner_id).all()
            if stores:
                for store in stores:
                    res["owner_store"].append(store.code)
        res["owner_store"] = list(set(res["owner_store"]))
        res["owner_company"] = list(set(res["owner_company"]))

    return res


def put_permission(data: dict, code: str, target: str, exclude: str=None):
    if data.get(code):
        data[code].add(target)
    else:
        data[code] = set(target)

    if exclude is not None and exclude == 'Y':
        del data[code]


def get_permission(session: Session, member_id: int):
    res = {}
    mc: List[MemberClass] = MemberClass.filter(session, member_id=member_id).all()
    mw = session.query(MemberWorker).filter(MemberWorker.member_id == member_id).all()

    if mc:
        for row in mc:
            data_list = session.query(ClassPermission).filter(ClassPermission.class_code == row.class_code).all()
            for pm in data_list:
                put_permission(res, pm.permission_code, pm.target)

    if mw:
        for row in mw:
            data_list = session.query(DeptPermission).filter(DeptPermission.dept_id == row.dept_id).all()
            for pm in data_list:
                put_permission(res, pm.permission_code, pm.target)

    mp = session.query(MemberPermission).filter(MemberPermission.member_id == member_id).all()

    if mp:
        for pm in mp:
            put_permission(res, pm.permission_code, pm.target)

    for k, v in res.items():
        for row in v:
            if row == "*":
                res[k] = ["*"]
                break

    return res


def id_pw_check(email, password, session: Session):
    member = Member.get(session, email=email)
    if not member:
        raise exc.NotFoundUserEx(user_id=email)
    if not bcrypt.checkpw(password.encode("utf8"), member.password.encode("utf8")):
        raise exc.NotMatchPWEx

    if not (member.status == 'Y' or member.status == 'R'):
        raise exc.NotAvailableEx

    return member
