from datetime import date
from typing import List, Optional, Union

import bcrypt
import pyotp
import random
from fastapi import APIRouter, Depends, Security, Query, Request
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.common.consts import AES_KEY, AES_IV, RANDOM_STRING_POOL
from app.common.config import conf
from app.database.conn import db
from app.database.schema import Member, Class, MemberClass, MemberMember, MemberStore, LogMember, MemberWorker, Dept, MemberCompany, Store, EmailHistory, SmsHistory
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, LogMemberDataIn, CreatedID, Exist
from app.models.user.member import DataMember, AddMember, ModMember, AddClass, DataClass, ModClass, ModMemberMe, ListDataMember, DataSimplePMember, PasswordChange
from app.utils.common_utils import get_ip, log_msg
from app.utils.crypto_utils import AES256
from app.utils.jwt import token_user, token_user_option
from app.utils.date_utils import D
from app.utils.aws import SES
from app.utils.sms import SMS

router = APIRouter(prefix='/member')


@router.post("", response_model=CreatedID, name="회원 등록")
def add_member(indata: AddMember, req: Request,
               session: Session = Depends(db.session), user: MemberToken = Security(token_user_option, scopes=["write:member"])):
    is_exist = is_email_exist(indata.email)
    if is_exist:
        raise exc.AlreadyUserEx
    ip = get_ip(req)

    hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
    indata.confirm_pass = indata.mobile[-4:]
    otp_secret_code = pyotp.random_base32()
    enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
    indata.mobile = enc_mobile
    indata.password = hash_pw

    indata_dict = indata.dict()

    data = Member.create(session, auto_commit=True, **indata_dict, otp=otp_secret_code)

    # 로깅
    writer = f"{user.name}:{user.id}" if user else f"{data.name}:{data.id}"
    log_data = LogMemberDataIn(action="등록", member_id=data.id, msg=log_msg("msg", "회원 가입"), writer=writer)
    LogMember.create(session, auto_commit=True, **log_data.dict())

    # ses = SES()
    # c = conf()
    #
    # enc = AES256(AES_KEY, AES_IV).encrypt(f"0,member,{data.id}")
    # email_subject = f"이메일 인증을 위한 안내메일 입니다."
    # email_body = f"""
    # <html>
    # <body style='font-size:16px;'>
    #     <div style='font-size:24px; font-weight:bold; text-align:center; padding-top:30px;'>환영합니다. <span style='color:#e24502;'>이메일</span>을 인증해 주세요.</div>
    #     <div style='margin:30px 0 60px; color:#676565; text-align:center;'>
    # 회원가입 완료를 위한 이메일 인증을 진행해주세요.<br>본인이 요청하신 내용이 아니면 무시하세요.
    #     </div>
    #     <a href='{c.ADMIN_HOST}/auth/cert-email/{enc}' style='display:block; width:364px; margin:auto; padding:12px 0; background:#e24502; color:#fff; text-align:center; text-decoration:none;'>이메일 인증하기</a>
    #     <div style='margin:30px 0 30px;'>
    # 본 메일은 발신전용이며, 회신이 되지 않습니다.<br>
    # 추가 문의사항은 고객센터(1644-7370)를 통해서 문의하여 주시기 바랍니다.<br>
    # Copyright © ConiaLab Corp. All rights reserved.
    #     </div>
    # </body>
    # </html>
    # """
    # ses.send_email(to=indata.email, subject=email_subject, message=email_body)
    #
    # history = EmailHistory()
    # history.member_id = data.id
    # history.type = 'cert'
    # history.to = indata.email
    # history.title = email_subject
    # history.body = email_body
    # history.provider = "ses"
    # session.add(history)
    # session.commit()

    return CreatedID(id=data.id)


@router.get("/exist", response_model=Exist, name="회원 중복 확인")
def check_member(email: EmailStr):
    is_exist = is_email_exist(email)
    return Exist(exist=is_exist)


@router.get("", response_model=ListDataMember, name="회원 목록")
def list_member(user_id: Optional[str] = Query(default=None, description="아이디(이메일)"),
                name: Optional[str] = Query(default=None, description="이름"),
                mobile: Optional[str] = Query(default=None, description="전화번호"),
                recommander: Optional[str] = Query(default=None, description="추천인"),
                company_name: Optional[str] = Query(default=None, description="회사명"),
                store_title: Optional[str] = Query(default=None, description="상점명"),
                s_reg_date: Optional[date] = Query(default=None, description="가입일 시작"),
                e_reg_date: Optional[date] = Query(default=None, description="가입일 종료"),
                company_id: Optional[int] = Query(default=None, description="회사 ID"),
                parent_member_id: Optional[int] = Query(default=None, description="상위 회원 ID"),
                class_code: Optional[str] = Query(default=None, description="회원 클래스"),
                status: Optional[List[str]] = Query(default=None, description="상태"),
                offset: int = 0, limit: int = 20,
                session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['read:member'])):
    """
    **store_code, company_id, parent_member_id, class_code** 조건은 1개만 선택 가능
    """
    target_list = user.scopes.get("read:member")
    company_list = [user.organization.get("my_company"), user.organization.get("owner_company")]

    parameter_check_count = 0
    if company_id: parameter_check_count += 1
    if parent_member_id: parameter_check_count += 1
    if class_code: parameter_check_count += 1

    if parameter_check_count > 1:
        raise exc.BadRequestEx(reason="검색 조건(store_code, company_id, parent_member_id, class_code)은 1가지만 선택 되어야 합니다.")

    if "*" not in target_list:
        if company_id:
            if "company" not in target_list or company_id not in company_list:
                raise exc.PermissionEx

    if company_id:
        subquery = session.query(Dept.id).filter(Dept.member_company_id == company_id).subquery()
        qry = session.query(Member).join(MemberWorker, Member.id == MemberWorker.member_id).filter(MemberWorker.dept_id.in_(subquery))
    elif parent_member_id:
        if "*" not in target_list and parent_member_id != user.id:
            raise exc.PermissionEx

        top_q = session.query(MemberMember).filter(MemberMember.pid == parent_member_id).cte('cte', recursive=True)
        bottom_q = session.query(MemberMember).join(top_q, top_q.c.member_id == MemberMember.pid)
        recursive_q = top_q.union(bottom_q)

        qry = session.query(Member).join(recursive_q, Member.id == recursive_q.c.member_id)
    elif class_code:
        if class_code == "NONE":
            qry = session.query(Member).outerjoin(MemberClass, Member.id == MemberClass.member_id).outerjoin(MemberCompany, Member.id == MemberCompany.member_id).outerjoin(Store, Member.id == Store.member_id).filter(MemberClass.class_code == None)
        else:
            qry = session.query(Member).join(MemberClass, Member.id == MemberClass.member_id).outerjoin(MemberCompany, Member.id == MemberCompany.member_id).outerjoin(Store, Member.id == Store.member_id).filter(MemberClass.class_code == class_code)
    else:
        if "*" not in target_list:
            raise exc.PermissionEx

        qry = session.query(Member).outerjoin(MemberCompany, Member.id == MemberCompany.member_id).outerjoin(Store, Member.id == Store.member_id)

    if user_id:
        qry = qry.filter(Member.email.like(f'%{user_id}%'))

    if name:
        qry = qry.filter(Member.name.like(f'%{name}%'))

    if mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(mobile)
        qry = qry.filter(Member.mobile == enc_mobile)

    if recommander:
        qry = qry.filter(Member.recommend == recommander)

    if company_name:
        qry = qry.filter(MemberCompany.name.like(f"%{company_name}%"))

    if store_title:
        qry = qry.filter(Store.title.like(f"%{store_title}%"))

    if s_reg_date and e_reg_date:
        qry = qry.filter(Member.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Member.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Member.reg_date < D().make235959(e_reg_date))

    if status:
        qry = qry.filter(Member.status.in_(status))

    qry = qry.filter(Member.admin_yn != 'Y')

    total = qry.count()
    qry = qry.order_by(Member.reg_date.desc())
    member_list = qry.offset(offset).limit(limit).all()

    return ListDataMember(total=total, datas=member_list)


@router.get("/mc", response_model=ListDataMember, name="회원(MC) 목록")
def list_member_mc(user_id: Optional[str] = Query(default=None, description="아이디(이메일)"),
                   name: Optional[str] = Query(default=None, description="이름"),
                   mobile: Optional[str] = Query(default=None, description="전화번호"),
                   parent_member_id: Optional[int] = Query(default=None, description="상위 회원 ID"),
                   offset: int = 0, limit: int = 20,
                   session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['read:member'])):
    if parent_member_id:
        top_q = session.query(MemberMember).filter(MemberMember.pid == parent_member_id).cte('cte', recursive=True)
        bottom_q = session.query(MemberMember).join(top_q, top_q.c.member_id == MemberMember.pid)
        recursive_q = top_q.union(bottom_q)

        qry = session.query(Member).join(recursive_q, Member.id == recursive_q.c.member_id)

    else:
        qry = session.query(Member)

    qry = qry.join(MemberClass, Member.id == MemberClass.member_id).filter(
        MemberClass.class_code == 'MC')

    if user_id:
        qry = qry.filter(Member.email.like(f'%{user_id}%'))

    if name:
        qry = qry.filter(Member.name.like(f'%{name}%'))

    if mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(mobile)
        qry = qry.filter(Member.mobile == enc_mobile)

    qry = qry.filter(Member.admin_yn != 'Y')

    total = qry.count()
    qry = qry.order_by(Member.reg_date.desc())
    member_list = qry.offset(offset).limit(limit).all()

    return ListDataMember(total=total, datas=member_list)


@router.get("/me", response_model=DataMember, name="회원 정보(본인)")
def get_member_me(session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=[])):
    member = Member.get(session=session, id=user.id)
    return member


@router.put("/me", response_model=Success, name="회원 수정(본인)")
def update_me(indata: ModMemberMe, session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=[])):
    if indata.password:
        hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
        indata.password = hash_pw

    if indata.mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
        indata.mobile = enc_mobile

    if indata.sns_naver:
        already = Member.get(session, sns_naver=indata.sns_naver)
        if already:
            already.sns_naver = ''
            session.commit()

    if indata.sns_kakao:
        already = Member.get(session, sns_naver=indata.sns_kakao)
        if already:
            already.sns_kakao = ''
            session.commit()

    if indata.sns_payco:
        already = Member.get(session, sns_naver=indata.sns_payco)
        if already:
            already.sns_payco = ''
            session.commit()

    if indata.sns_google:
        already = Member.get(session, sns_naver=indata.sns_google)
        if already:
            already.sns_google = ''
            session.commit()

    if indata.sns_apple:
        already = Member.get(session, sns_naver=indata.sns_apple)
        if already:
            already.sns_apple = ''
            session.commit()

    # 본인인증 및 성인인증 변경시 검증 프로세스 필요

    member_update(user.id, indata, user, session)
    return Success()


@router.put("/me-passwd", response_model=Success, name="패스워드 수정(본인)")
def update_me_passwd(indata: PasswordChange,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=[])):
    member = Member.get(session=session, id=user.id)

    if not member:
        raise exc.NotFoundDataEx

    if not bcrypt.checkpw(indata.origin_password.encode('utf8'), member.password):
        raise exc.NotMatchPWEx

    hash_pw = bcrypt.hashpw(indata.new_password.encode('utf8'), bcrypt.gensalt())
    member.password = hash_pw
    session.commit()

    if member.mobile:
        mobile = AES256(AES_KEY, AES_IV).decrypt(member.mobile)
        sms = SMS()
        try:
            msg = f'[코니아월드]\n회원님의 패스워드가 정상적으로 변경 되었습니다.'
            res = sms.send(mobile, msg)

            sh = SmsHistory()
            sh.type = 'system'
            sh.mobile = member.mobile
            sh.body = msg
            sh.mid = res['mid']
            sh.provider = ''
            sh.member_id = member.id
            session.add(sh)
            session.commit()
        except:
            pass

    # 로깅
    log_data = LogMemberDataIn(action="수정", member_id=member.id, msg=log_msg("msg", "패스워드 변경"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.post("/class", response_model=Success, name="회원 분류 추가")
def add_class(indata: AddClass, session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:class"])):
    data = Class.get(session=session, code=indata.code)
    if data:
        raise exc.AlreadyDataEx

    indata_dict = indata.dict()
    Class.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("/class", response_model=List[DataClass], name="회원 분류 목록")
def list_class(session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:class"])):
    list_data = Class.filter(session=session).all()
    return list_data


@router.get("/class/exist", response_model=Exist, name="회원 분류 중복 확인")
def check_class(code: str):
    is_exist = is_class_exist(code)
    return Exist(exist=is_exist)


@router.put("/class/{code}", response_model=Success, name="회원 분류 수정")
def update_class(code: str, indata: ModClass, session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:class"])):
    data = Class.get(session=session, code=code)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/class/{code}/link", response_model=Success, name="회원 분류 연결")
def class_link(code: str, member_id: int,
               session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["link:class"])):
    data = Class.get(session=session, code=code)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
        "class_code": code,
        "member_id": member_id
    }
    MemberClass.create(session=session, auto_commit=True, **mapping_data)

    # 로깅
    log_data = LogMemberDataIn(action="Class 연결", member_id=member_id, msg=log_msg("msg", f"Class 연결 : {code}"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/class/{code}/link", response_model=Success, name="회원 분류 연결 해제")
def class_unlink(code: str, member_id: int,
                 session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["link:class"])):
    data = Class.get(session=session, code=code)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
        "class_code": code,
        "member_id": member_id
    }
    MemberClass.filter(session=session, **mapping_data).delete(auto_commit=True)

    # 로깅
    log_data = LogMemberDataIn(action="Class 연결", member_id=member_id, msg=log_msg("msg", f"Class 연결 해제 : {code}"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.post("/link", response_model=Success, name="회원간 연결")
def member_mapping(member_id: int, parent_id: int,
                   session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["link:member"])):
    member_check(member_id, session)
    member_check(parent_id, session)

    mapping_data = {
        "member_id": member_id,
        "pid": parent_id,
    }
    MemberMember.create(session=session, auto_commit=True, **mapping_data)

    # 로깅
    log_data = LogMemberDataIn(action="회원 연결", member_id=member_id, msg=log_msg("msg", f"상위 회원 연결 : {parent_id}"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())
    log_data = LogMemberDataIn(action="회원 연결", member_id=parent_id, msg=log_msg("msg", f"하위 회원 연결 : {member_id}"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/link", response_model=Success, name="회원간 연결 해제")
def member_unlink(member_id: int, parent_id: int,
                  session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["link:member"])):
    member_check(member_id, session)
    member_check(parent_id, session)

    # TODO : 해제 조건 체크

    mapping_data = {
        "member_id": member_id,
        "pid": parent_id,
    }
    MemberMember.filter(session=session, **mapping_data).delete(auto_commit=True)

    # 로깅
    log_data = LogMemberDataIn(action="회원 연결", member_id=member_id, msg=log_msg("msg", f"상위 회원 연결 해제 : {parent_id}"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())
    log_data = LogMemberDataIn(action="회원 연결", member_id=parent_id, msg=log_msg("msg", f"하위 회원 연결 해제 : {member_id}"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{member_id}", response_model=DataMember, name="회원 정보")
def get_member(member_id: int,
               target: str = Query(description="대상 테이블"),
               session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['read:member'])):
    target_list = user.scopes.get("read:member")
    store_list = [user.organization.get("my_store"), user.organization.get("owner_store")]
    company_list = [user.organization.get("my_company"), user.organization.get("owner_company")]

    if "*" not in target_list:
        if target == 'store':
            if "store" in target_list:
                using_store: List[MemberStore] = MemberStore.filter(session, member_id=member_id).all()
                p_flag = False
                for row in using_store:
                    if row.store_code in store_list:
                        p_flag = True
                        break
                if not p_flag:
                    raise exc.PermissionEx
            else:
                raise exc.PermissionEx
        elif target == 'company':
            if "company" in target_list:
                using_worker: List[MemberWorker] = MemberWorker.filter(session, member_id=member_id).all()
                p_flag = False
                for row in using_worker:
                    if row.member_company_id in company_list:
                        p_flag = True
                        break
                if not p_flag:
                    raise exc.PermissionEx
            else:
                raise exc.PermissionEx

    member = Member.get(session=session, id=member_id)

    if not member:
        raise exc.NotFoundDataEx

    data: DataMember = DataMember.from_orm(member)
    p_members = MemberMember.filter(session, member_id=member_id).all()

    p_list = []
    row: MemberMember
    for row in p_members:
        p_list.append(DataSimplePMember(id=row.pid, name=row.member1.name, email=row.member1.email))
    data.p_member = p_list

    return data


@router.put("/{member_id}", response_model=Success, name="회원 수정")
def update_member(member_id: int, indata: ModMember,
                  session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['write:member'])):
    if indata.password:
        hash_pw = bcrypt.hashpw(indata.password.encode('utf8'), bcrypt.gensalt())
        indata.password = hash_pw

    if indata.mobile:
        enc_mobile = AES256(AES_KEY, AES_IV).encrypt(indata.mobile)
        indata.mobile = enc_mobile

    member_update(member_id, indata, user, session)

    return Success()


@router.put("/{member_id}/force-change-passwd", response_model=Success, name="회원 임시비밀번호 발급")
def force_change_passwd(member_id: int,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=['write:member'])):
    member = Member.get(session=session, id=member_id)

    if not member:
        raise exc.NotFoundDataEx

    random_pw = ""
    for i in range(8):
        random_pw += random.choice(RANDOM_STRING_POOL)

    hash_pw = bcrypt.hashpw(random_pw.encode('utf8'), bcrypt.gensalt())
    member.password = hash_pw
    session.commit()

    if member.mobile:
        mobile = AES256(AES_KEY, AES_IV).decrypt(member.mobile)
        sms = SMS()
        try:
            msg = f'[코니아월드]\n회원님의 임시 패스워드는 {random_pw} 입니다.\nhttps://admin.coniaworld.com'
            res = sms.send(mobile, msg)

            sh = SmsHistory()
            sh.type = 'system'
            sh.mobile = member.mobile
            sh.body = msg
            sh.mid = res['mid']
            sh.provider = ''
            sh.member_id = member.id
            session.add(sh)
            session.commit()
        except:
            pass

    # 로깅
    log_data = LogMemberDataIn(action="수정", member_id=member.id, msg=log_msg("msg", "임시 패스워드 발급"), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())

    return Success()


def is_email_exist(email: str):
    """
    회원 계정 중복 체크
    :param email:
    :return:
    """
    get_email = Member.get(email=email)
    if get_email:
        return True
    return False


def member_check(member_id: int, session: Session):
    """
    회원 체크
    :param member_id:
    :param session:
    :return:
    """
    data = Member.get(session=session, id=member_id)
    if not data:
        raise exc.NotFoundDataEx


def member_update(target: int, indata: Union[ModMember, ModMemberMe], user: MemberToken, session: Session):
    """
    회원 수정
    :param target:
    :param indata:
    :param user:
    :param session:
    :return:
    """
    data: Member = Member.get(session=session, id=target)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())
    for row in change_data:
        if row.get("mobile"):
            before = AES256(AES_KEY, AES_IV).decrypt(row["mobile"]["before"])
            after = AES256(AES_KEY, AES_IV).decrypt(row["mobile"]["after"])
            row["mobile"] = {
                "before": before,
                "after": after
            }

    # 로깅
    log_data = LogMemberDataIn(action="수정", member_id=data.id, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogMember.create(session, auto_commit=True, **log_data.dict())


def is_class_exist(code: str):
    """
    회원 분류 중복 체크
    :param code:
    :return:
    """
    get_class_code = Class.get(code=code)
    if get_class_code:
        return True
    return False
