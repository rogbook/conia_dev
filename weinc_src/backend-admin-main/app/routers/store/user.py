import os
from typing import Union

from fastapi import APIRouter, Depends, Security, UploadFile
from fastapi.params import Query
from sqlalchemy.orm import Session
import openpyxl

from app.database.conn import db
from app.database.schema import MemberStore, LogStore, AbleTarget, Customer
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, LogStoreDataIn
from app.models.store import *
from app.utils.common_utils import log_msg
from app.utils.jwt import token_user
from app.utils.date_utils import D

router = APIRouter(prefix='/store')


@router.post("/{store_code}/user", response_model=Success, name="상점 이용자 등록")
def add_member_store(store_code: str, indata: AddMemberStore,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:store_member'])):
    indata_dict = indata.dict()
    data: MemberStore = MemberStore.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("/{store_code}/user", response_model=ListMemberStore, name="상점 이용자 목록")
def list_member_store(store_code: str,
                      name: Optional[str] = Query(default=None, description="이름"),
                      email: Optional[str] = Query(default=None, description="이메일"),
                      confirm: Optional[str] = Query(default=None, description="승인여부"),
                      recommend: Optional[str] = Query(default=None, description="추천인"),
                      offset: int = 0, limit: int = 20,
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=['read:store_member'])):
    qry = session.query(MemberStore).join(Customer, Customer.id == MemberStore.customer_id).filter(MemberStore.store_code == store_code)

    if name:
        qry = qry.filter(Customer.name.like(f'%{name}%'))

    if email:
        qry = qry.filter(Customer.email.like(f'%{email}%'))

    if confirm:
        qry = qry.filter(MemberStore.confirm == confirm)

    if recommend:
        qry = qry.filter(Customer.recommend == recommend)

    total = qry.count()
    qry = qry.order_by(MemberStore.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListMemberStore(total=total, datas=datas)


@router.put("/{store_code}/user/{req_id}", response_model=Success, name="상점 이용자 수정")
def mod_member_store(store_code: str, req_id: int, indata: ModMemberStore,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:store_member'])):
    data: MemberStore = MemberStore.get(session=session, id=req_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action="상점 이용자 수정", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{store_code}/user/{req_id}", response_model=Success, name="상점 이용자 삭제")
def del_member_store(store_code: str, req_id: int,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:store_member'])):
    data: MemberStore = MemberStore.get(session=session, id=req_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    # 로깅
    log_data = LogStoreDataIn(action="상점 이용자 삭제", store_code=store_code, msg=log_msg("msg", f'삭제 대상 - {data.customer.name}:{data.customer_id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    session.delete(data)
    session.commit()

    return Success()


@router.post("/{store_code}/able_target", response_model=Success, name="상점 이용 가능자 일괄 추가(Excel)")
async def list_able_target(store_code: str, file: UploadFile,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:store_member'])):

    allowed_extensions = {'xlsx'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        raise exc.NotAllowedFileEx

    file_path = os.path.join(os.getcwd(), 'app/upload/', f'StoreAbleTarget-{store_code}-{D.now_str_trim()}.xlsx')

    with open(file_path, 'wb') as buffer:
        buffer.write(await file.read())

    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    try:
        for row in ws.rows:
            row_a = row[0].value
            if not row_a:
                break

            if not str(row[2].value).isdigit():
                raise exc.BadRequestEx(reason='전화번호 오류')

            data = AbleTarget()
            data.store_code = store_code
            data.unique_value = row[0].value
            data.name = row[1].value
            data.mobile = AES256(AES_KEY, AES_IV).encrypt(row[2].value)
            session.add(data)
        try:
            session.commit()
        except Exception as e:
            raise exc.BadRequestEx(reason='식별값 중복 오류.')

    finally:
        try:
            wb.close()
            os.remove(file_path)
        except:
            pass

    return Success()


@router.get("/{store_code}/able_target", response_model=ListAbleTarget, name="상점 이용 가능자 목록")
def list_able_target(store_code: str,
                     name: Optional[str] = Query(default=None, description="이름"),
                     unique_value: Optional[str] = Query(default=None, description="사번"),
                     offset: int = 0, limit: int = 20,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['read:store_member'])):
    qry = session.query(AbleTarget).filter(AbleTarget.store_code == store_code)

    if name:
        qry = qry.filter(AbleTarget.name.like(f"%{name}%"))

    if unique_value:
        qry = qry.filter(AbleTarget.unique_value == unique_value)

    total = qry.count()
    qry = qry.order_by(AbleTarget.id.asc())
    datas = qry.offset(offset).limit(limit).all()

    return ListAbleTarget(total=total, datas=datas)


@router.put("/{store_code}/able_target/{target_id}", response_model=Success, name="상점 이용 가능자 수정")
def mod_able_target(store_code: str, target_id: int, indata: ModAbleTarget,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store_member'])):
    target = session.query(AbleTarget).filter(AbleTarget.store_code == store_code, AbleTarget.id == target_id).first()

    if not target:
        raise exc.NotFoundDataEx

    target.update_optional(session, auto_commit=True, **indata.dict())

    return Success()


@router.delete("/{store_code}/able_target/{target_id}", response_model=Success, name="상점 이용 가능자 삭제")
def del_able_target(store_code: str, target_id: int,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store_member'])):
    target = session.query(AbleTarget).filter(AbleTarget.store_code == store_code, AbleTarget.id == target_id).first()

    if not target:
        raise exc.NotFoundDataEx

    session.delete(target)
    session.commit()

    return Success()


@router.post("/{store_code}/able_target/one", response_model=Success, name="상점 이용 가능자 개별등록")
def add_able_target(store_code: str, indata: AddAbleTarget,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store_member'])):
    target = session.query(AbleTarget).filter(AbleTarget.store_code == store_code, AbleTarget.unique_value == indata.unique_value).first()

    if target:
        raise exc.AlreadyDataEx

    indata_dict = indata.dict()
    indata_dict['store_code'] = store_code
    data = AbleTarget.create(session, auto_commit=True, **indata_dict)

    return Success()