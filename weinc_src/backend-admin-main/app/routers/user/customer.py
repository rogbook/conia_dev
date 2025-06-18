import os
from datetime import date
from datetime import timedelta
from typing import List, Optional
import random

import bcrypt
from fastapi import APIRouter, Depends, Security, Query, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.common.consts import AES_KEY, AES_IV, MEMBER_STATUS, RANDOM_STRING_POOL
from app.common.template_string import BULK_ADD_CUSTOMER_MAIL_BODY, PASSWORD_RESET_CUSTOMER
from app.common.config import conf
from app.database.conn import db
from app.database.schema import MemberStore, Customer, Store, Cert, DeliveryAddress, EmailHistory, SmsHistory, LogCustomer
from app.errors import exceptions as exc
from app.models.auth import MemberToken, Login, Token, SnsLogin, ChangePassword, FindId
from app.models.common import Success, CreatedID, SuccessFail, LogCustomerDataIn
from app.models.user.customer import ListDataCustomer, DataCustomer, ModCustomer, AddCustomer, AddDeliveryAddress
from app.utils.crypto_utils import AES256
from app.utils.date_utils import D
from app.utils.jwt import token_user, create_access_token
from app.utils.common_utils import get_ip, is_valid_email, log_msg, generate_random_string_num
from app.models.store import DataSimpleStore
from app.utils.aws import SES
from app.utils.sms import SMS

router = APIRouter(prefix='/customer')


@router.get("", response_model=ListDataCustomer, name="회원 목록")
def list_member(user_id: Optional[str] = Query(default=None, description="아이디(이메일)"),
                name: Optional[str] = Query(default=None, description="이름"),
                mobile: Optional[str] = Query(default=None, description="전화번호"),
                recommander: Optional[str] = Query(default=None, description="추천인"),
                s_reg_date: Optional[date] = Query(default=None, description="가입일 시작"),
                e_reg_date: Optional[date] = Query(default=None, description="가입일 종료"),
                store_code: Optional[str] = Query(default=None, description="상점 코드"),
                status: Optional[List[str]] = Query(default=None, description="상태"),
                offset: int = 0, limit: int = 20,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['read:member'])):
    """
    **store_code, company_id, parent_member_id, class_code** 조건은 1개만 선택 가능
    """
    target_list = user.scopes.get("read:member")
    store_list = [user.organization.get("my_store"), user.organization.get("owner_store")]

    if "*" not in target_list:
        if store_code:
            if "store" not in target_list or store_code not in store_list:
                raise exc.PermissionEx

    if store_code:
        qry = session.query(Customer).join(MemberStore, Customer.id == MemberStore.customer_id).filter(MemberStore.store_code == store_code)
    else:
        if "*" not in target_list:
            raise exc.PermissionEx

        qry = session.query(Customer)

    if user_id:
        qry = qry.filter(Customer.email.like(f'%{user_id}%'))

    if name:
        qry = qry.filter(Customer.name.like(f'%{name}%'))

    if mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(mobile)
        qry = qry.filter(Customer.mobile == enc_mobile)

    if recommander:
        qry = qry.filter(Customer.recommend == recommander)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Customer.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Customer.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Customer.reg_date < D().make235959(e_reg_date))

    if status:
        qry = qry.filter(Customer.status.in_(status))

    # qry = qry.filter(Customer.admin_yn != 'Y')

    total = qry.count()
    qry = qry.order_by(Customer.reg_date.desc())
    customer_list = qry.offset(offset).limit(limit).all()

    return ListDataCustomer(total=total, datas=customer_list)


@router.post("", response_model=CreatedID, name="고객 회원 등록")
def add_customer(indata: AddCustomer, req: Request,
                 session: Session = Depends(db.session)):
    is_exist = is_email_exist(indata.email)
    if is_exist:
        raise exc.AlreadyUserEx
    ip = get_ip(req)

    hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
    enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
    indata.mobile = enc_mobile
    indata.password = hash_pw

    indata_dict = indata.dict()

    data = Customer.create(session, auto_commit=True, **indata_dict)

    if indata.address and indata.address_detail and indata.zipcode:
        default_delivery = AddDeliveryAddress(title="기본배송지",
                                              name=indata.name,
                                              address=indata.address,
                                              address_detail=indata.address_detail,
                                              zipcode=indata.zipcode,
                                              mobile=indata.mobile,
                                              default_yn="Y")
        DeliveryAddress.create(session=session, auto_commit=True, customer_id=data.id, **default_delivery.dict())

    return CreatedID(id=data.id)


@router.put("/bulk_excel_customer", response_model=SuccessFail, name="고객회원 일괄등록(Excel)")
async def bulk_excel_customer(file: UploadFile,
                              store_code: str = Query(default=None, description='상점 연결시 입력'),
                              session: Session = Depends(db.session),
                              user: MemberToken = Security(token_user, scopes=['write:member'])):
    allowed_extensions = {'xlsx'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        raise exc.NotAllowedFileEx

    file_path = os.path.join(os.getcwd(), 'app/upload/', f'ConiaCustomerBulk-{D.now_str_trim()}.xlsx')

    with open(file_path, 'wb') as buffer:
        buffer.write(await file.read())

    import openpyxl
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    success_cnt = 0
    fail_list = []
    success_email = []
    success_list = []

    try:
        for row in ws.rows:
            row_a = row[0].value
            row_b = row[1].value

            if row_a == '이메일':
                continue
            if not row_a:
                break

            email_data = str(row_a).strip()
            email_data = email_data.replace(':mailto', '')
            name_data = None
            if row_b:
                name_data = str(row_b).strip()

            if not is_valid_email(email_data):
                fail_list.append([email_data, '이메일 형식 오류'])
                continue
            if email_data in success_email:
                fail_list.append([email_data, '중복 이메일'])
                continue
            is_exist = is_email_exist(email_data)
            if is_exist:
                fail_list.append([email_data, '중복 이메일'])
                continue

            rand_pw = generate_random_string_num(6)
            hash_pw = bcrypt.hashpw(rand_pw.encode('utf8'), bcrypt.gensalt())

            customer_data = Customer()
            customer_data.email = email_data
            customer_data.password = hash_pw
            if name_data:
                customer_data.name = name_data
            customer_data.referer = 'admin'
            customer_data.referer_domain = 'admin'
            customer_data.join_platform = 'ADM'

            session.add(customer_data)
            session.flush()

            success_list.append([customer_data.id, email_data, rand_pw, name_data])
            success_email.append(email_data)
            success_cnt += 1

        # 회원 가입 처리
        session.commit()

        # 상점 연결 및 안내 이메일 전송 예약 처리
        email_subject = f"[윙크] 임직원 전용몰 회원가입 안내"

        for success in success_list:
            if store_code:
                ms = MemberStore()
                ms.confirm = 'Y'
                ms.customer_id = success[0]
                ms.store_code = store_code
                ms.value = 'ADMIN_BULK'
                session.add(ms)

            email_body = BULK_ADD_CUSTOMER_MAIL_BODY.format(name=success[3], email=success[1], password=success[2])

            history = EmailHistory()
            history.customer_id = success[0]
            history.type = 'bulk'
            history.status = 'R'
            history.to = success[1]
            history.title = email_subject
            history.body = email_body
            history.res_date = D().now_str()
            history.provider = "ses"
            session.add(history)
        session.commit()

    except Exception as e:
        raise exc.APIException(msg=str(e.args))
    finally:
        try:
            wb.close()
            os.remove(file_path)
        except:
            pass

    return SuccessFail(success_count=success_cnt, fail_list=fail_list)


@router.get("/excel", name="고객 회원 목록 엑셀 다운로드")
def excel_customer(user_id: Optional[str] = Query(default=None, description="아이디(이메일)"),
                   name: Optional[str] = Query(default=None, description="이름"),
                   mobile: Optional[str] = Query(default=None, description="전화번호"),
                   recommander: Optional[str] = Query(default=None, description="추천인"),
                   s_reg_date: Optional[date] = Query(default=None, description="가입일 시작"),
                   e_reg_date: Optional[date] = Query(default=None, description="가입일 종료"),
                   store_code: Optional[str] = Query(default=None, description="상점 코드"),
                   status: Optional[List[str]] = Query(default=None, description="상태"),
                   session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['read:member'])):
    target_list = user.scopes.get("read:member")
    store_list = [user.organization.get("my_store"), user.organization.get("owner_store")]

    if "*" not in target_list:
        if store_code:
            if "store" not in target_list or store_code not in store_list:
                raise exc.PermissionEx

    if store_code:
        qry = session.query(Customer).join(MemberStore, Customer.id == MemberStore.customer_id).filter(MemberStore.store_code == store_code)
    else:
        if "*" not in target_list:
            raise exc.PermissionEx

        qry = session.query(Customer)

    if user_id:
        qry = qry.filter(Customer.email.like(f'%{user_id}%'))

    if name:
        qry = qry.filter(Customer.name.like(f'%{name}%'))

    if mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(mobile)
        qry = qry.filter(Customer.mobile == enc_mobile)

    if recommander:
        qry = qry.filter(Customer.recommend == recommander)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Customer.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Customer.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Customer.reg_date < D().make235959(e_reg_date))

    if status:
        qry = qry.filter(Customer.status.in_(status))

    total = qry.count()
    qry = qry.order_by(Customer.reg_date.desc())
    customer_list = qry.all()

    import openpyxl
    file_name = f'ConiaCustomerList-{store_code}-{D.now_str_trim()}.xlsx' if store_code else f'ConiaCustomerList-{D.now_str_trim()}.xlsx'
    file_path = os.path.join(os.getcwd(), 'app/upload/', file_name)
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["이름", "아이디", "휴대전화", "가입일", "상태", "추천인", "이용 상점(상점명:승인상태)", "마케팅(SMS)", "마케팅(EMAIL)"])

    for row in customer_list:
        data = DataCustomer.from_orm(row)
        use_store_list = []
        for row in data.member_store:
            use_store_list.append(f"{row.store.title}:{row.confirm}")
        sheet.append([data.name, data.email, data.mobile, data.reg_date, MEMBER_STATUS.get(data.status, ''), data.recommend, ",".join(use_store_list) if use_store_list else '', data.sms, data.mailling])
    wb.save(file_path)

    return FileResponse(file_path, filename=file_name)


@router.post("/login", response_model=Token, name="고객 로그인")
def customer_login(indata: Login,
                   store_code: str = Query(description="대상 상점"),
                   session: Session = Depends(db.session)):
    member = Customer.get(session, email=indata.email)
    if not member:
        raise exc.NotFoundUserEx
    if not bcrypt.checkpw(indata.password.encode("utf8"), member.password.encode("utf8")):
        raise exc.NotMatchPWEx

    return customer_login_proc(session, member, store_code)


@router.post("/sns-login", response_model=Token, name="고객 SNS 로그인")
def customer_sns_login(indata: SnsLogin,
                       store_code: str = Query(description="대상 상점"),
                       session: Session = Depends(db.session)):
    member = None

    if indata.type == "naver":
        member = Customer.get(session, sns_naver=indata.token)
    elif indata.type == "kakao":
        member = Customer.get(session, sns_kakao=indata.token)
    elif indata.type == "payco":
        member = Customer.get(session, sns_payco=indata.token)
    elif indata.type == "google":
        member = Customer.get(session, sns_google=indata.token)
    elif indata.type == "apple":
        member = Customer.get(session, sns_apple=indata.token)

    if not member:
        raise exc.NotFoundUserEx

    return customer_login_proc(session, member, store_code)


@router.post("/password-change-cert", response_model=Success, name="패스워드 변경(본인인증)")
def password_change(indata: ChangePassword,
                    session: Session = Depends(db.session)):
    data: Cert = Cert.get(session, req_token_version_id=indata.token_version_id, status='Y')
    if not data:
        raise exc.CertFailEx

    member: Customer = Customer.get(session, email=indata.email_id)
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

    member: Customer = session.query(Customer).filter(Customer.mobile == v).first()

    return member.email


@router.get("/able_store", response_model=List[DataSimpleStore], name="상점 목록")
def able_store(group: str = Query(default=None, title="상점 그룹"),
               session: Session = Depends(db.session)):
    qry = session.query(Store).filter(Store.status == 'Y')

    if group:
        qry = qry.filter(Store.group == group)

    return qry.all()


@router.get("/{customer_id}", response_model=DataCustomer, name="회원 정보")
def get_customer(customer_id: int,
                 target: str = Query(description="대상 테이블"),
                 session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['read:member'])):
    target_list = user.scopes.get("read:member")
    store_list = [user.organization.get("my_store"), user.organization.get("owner_store")]

    if "*" not in target_list:
        if target == 'store':
            if "store" in target_list:
                using_store: List[MemberStore] = MemberStore.filter(session, customer_id=customer_id).all()
                p_flag = False
                for row in using_store:
                    if row.store_code in store_list:
                        p_flag = True
                        break
                if not p_flag:
                    raise exc.PermissionEx
            else:
                raise exc.PermissionEx

    customer = Customer.get(session=session, id=customer_id)

    return customer


@router.put("/{customer_id}", response_model=Success, name="회원 수정")
def update_customer(customer_id: int, indata: ModCustomer,
                    session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['write:member'])):
    if 'write:member' not in user.scopes:
        raise exc.PermissionEx

    if indata.password:
        hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
        indata.password = hash_pw

    if indata.mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
        indata.mobile = enc_mobile

    data: Customer = Customer.get(session=session, id=customer_id)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())
    log_data = LogCustomerDataIn(action="수정", customer_id=customer_id, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogCustomer.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.put("/{customer_id}/force-change-passwd", response_model=Success, name="회원 임시비밀번호 발급")
def force_change_passwd(customer_id: int,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=['write:member'])):
    customer = Customer.get(session=session, id=customer_id)

    if not customer:
        raise exc.NotFoundDataEx

    random_pw = ""
    for i in range(6):
        random_pw += random.choice(RANDOM_STRING_POOL)

    hash_pw = bcrypt.hashpw(random_pw.encode('utf8'), bcrypt.gensalt())
    customer.password = hash_pw
    session.commit()

    if customer.mobile:
        mobile = AES256(AES_KEY, AES_IV).decrypt(customer.mobile)
        sms = SMS()
        try:
            msg = f"""[윙크]
임시 비밀번호가 발급되었습니다.

아이디(이메일): {customer.email}
임시 비밀번호: {random_pw}
로그인 후 반드시 비밀번호를 변경해 주세요.
[마이메뉴 → 개인정보 수정 → 비밀번호 변경]

문의사항은 고객센터로 문의해 주세요.
https://pf.kakao.com/_JxnZxkxj
"""
            res = sms.send(mobile, msg)

            sh = SmsHistory()
            sh.type = 'system'
            sh.mobile = customer.mobile
            sh.body = msg
            sh.mid = res['mid']
            sh.provider = ''
            sh.customer_id = customer.id
            session.add(sh)
            session.commit()
        except:
            pass

    ses = SES()
    email_body = PASSWORD_RESET_CUSTOMER.format(email=customer.email, password=random_pw)
    ses.send_email(to=customer.email, subject=f"[윙크] 임시 비밀번호 발급", message=email_body)

    history = EmailHistory()
    history.customer_id = customer.id
    history.type = 'passwd'
    history.to = customer.email
    history.title = f"[윙크] 임시 비밀번호 발급"
    history.body = email_body
    history.provider = "ses"
    session.add(history)
    session.commit()

    # 로깅
    log_data = LogCustomerDataIn(action="수정", customer_id=customer.id, msg=log_msg("msg", "임시 패스워드 발급"), writer=f"{user.name}:{user.id}")
    LogCustomer.create(session, auto_commit=True, **log_data.dict())

    return Success()


def customer_login_proc(session, member, store_code):
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

    able_store: List[MemberStore] = MemberStore.filter(session, customer_id=member.id, confirm="Y").all()
    able_store_list = []
    for row in able_store:
        able_store_list.append(row.store_code)

    token_data: MemberToken = MemberToken.from_orm(member)
    token_data.store_code = able_store_list

    access_token = create_access_token(token_data.dict(), timedelta(minutes=10))
    refresh_token = create_access_token(token_data.dict(), timedelta(days=1))

    return Token(access_token=access_token, refresh_token=refresh_token)


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
