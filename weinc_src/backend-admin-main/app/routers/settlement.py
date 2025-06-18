from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.common.consts import AES_KEY, AES_IV
from app.database.conn import db
from app.database.schema import SettlementShip, SettlementData, Member, MemberClass, SettlementExcel
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success
from app.models.settlement import ListData, ListShipData, ModSettlementData, ListSettlementHistoryData, SettlementExcelReq
from app.models.user.member import ListDataMember
from app.utils.crypto_utils import AES256
from app.utils.date_utils import D
from app.utils.jwt import token_user

router = APIRouter(prefix='/settlement')


@router.get("", response_model=ListData, name="정산 목록")
def settlement_list(member_id: Optional[int] = None,
                    kind: Optional[str] = None,
                    status: Optional[str] = Query(default=None, description="상태"),
                    minus: Optional[str] = Query(default=None, description="마이너스 금액만"),
                    s_reg_date: Optional[date] = Query(default=None, description="시작일"),
                    e_reg_date: Optional[date] = Query(default=None, description="종료일"),
                    offset: int = 0, limit: int = 20,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    qry = session.query(SettlementData)
    sum_qry = session.query(func.sum(SettlementData.amount))

    if status:
        qry = qry.filter(SettlementData.status == status)
        sum_qry = sum_qry.filter(SettlementData.status == status)

    if minus:
        qry = qry.filter(SettlementData.amount < 0)
        sum_qry = sum_qry.filter(SettlementData.amount < 0)

    if member_id:
        if member_id == 1:
            if not user.admin == "Y":
                raise exc.PermissionEx
        qry = qry.filter(SettlementData.member_id == member_id)
        sum_qry = sum_qry.filter(SettlementData.member_id == member_id)
    else:
        if not user.admin == "Y":
            raise exc.PermissionEx

    if kind:
        if kind == 'PG':
            if not user.admin == "Y":
                raise exc.PermissionEx
        qry = qry.filter(SettlementData.type == kind)
        sum_qry = sum_qry.filter(SettlementData.type == kind)
    else:
        qry = qry.filter(SettlementData.type != 'PG')
        sum_qry = sum_qry.filter(SettlementData.type != 'PG')

    if s_reg_date and e_reg_date:
        qry = qry.filter(SettlementData.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
        sum_qry = sum_qry.filter(SettlementData.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(SettlementData.reg_date > s_reg_date)
        sum_qry = sum_qry.filter(SettlementData.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(SettlementData.reg_date < D().make235959(e_reg_date))
        sum_qry = sum_qry.filter(SettlementData.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    total_sum = sum_qry.scalar()
    # qry = qry.order_by(SettlementData.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListData(total=total, total_sum=total_sum, datas=datas)


@router.post("", response_model=Success, name="정산 데이터 일괄 수정")
def settlement_update(indata: ModSettlementData,
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=['write:settlement'])):
    member = {}
    for target in indata.ids:
        data = SettlementData.get(session=session, id=target)
        if not data:
            raise exc.NotFoundDataEx
        if indata.status:
            data.status = indata.status
        if indata.reject:
            data.reject = indata.reject

        if member.get(data.member_id):
            member.get(data.member_id)['settlement_targets'].append(data)
        else:
            member[data.member_id] = {
                "member": data.member,
                "settlement_targets": [data]
            }
    session.commit()

    if indata.status == 'C':
        for row in member.values():
            enc_mobile = row['member'].mobile
            if enc_mobile:
                mobile = AES256(AES_KEY, AES_IV).decrypt(enc_mobile)
                count = len(row['settlement_targets'])
                total = 0
                for s in row['settlement_targets']:
                    total += s.amount
                date_range_str = f"\n기간 {indata.date_range}" if indata.date_range else ''
                msg = f"""[코니아 정산 안내]{date_range_str}\n정산 대상 확정\n{int(total):,}원 ({count:,}건)"""
                print(msg)

    # 로깅
    # log_data = LogStoreDataIn(action="상점 테마 상품 연결", store_code=store_code, msg=log_msg("msg", f'테마 - {theme.name}:{theme.id} / 대상 - {added_prd_id}'), writer=f"{user.name}:{user.id}")
    # LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/excel", response_model=List[SettlementExcelReq], name="정산 목록 엑셀 요청 목록")
def settlement_excel(session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    qry = session.query(SettlementExcel)

    qry = qry.filter(SettlementExcel.request_member == user.id)

    qry = qry.order_by(SettlementExcel.reg_date.desc())

    return qry.all()


@router.post("/excel", response_model=Success, name="정산 목록 엑셀 요청")
def settlement_excel(member_id: Optional[int] = None,
                     member_type: Optional[str] = None,
                     kind: Optional[str] = None,
                     status: Optional[str] = Query(default=None, description="상태"),
                     s_reg_date: Optional[date] = Query(default=None, description="시작일"),
                     e_reg_date: Optional[date] = Query(default=None, description="종료일"),
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    req_data = SettlementExcel()
    req_data.member_id = member_id
    req_data.member_type = member_type
    req_data.target_kind = kind
    req_data.target_status = status
    req_data.s_reg_date = s_reg_date
    req_data.e_reg_date = e_reg_date
    req_data.request_member = user.id
    req_data.status = 'R'
    session.add(req_data)
    session.commit()

    return Success()


@router.get("/member", response_model=ListDataMember, name="정산 대상 회원 목록")
def member_list(status: Optional[str] = Query(default=None, description="상태"),
                class_code: Optional[str] = Query(default=None, description="회원 타입"),
                s_reg_date: Optional[date] = Query(default=None, description="시작일"),
                e_reg_date: Optional[date] = Query(default=None, description="종료일"),
                offset: int = 0, limit: int = 20,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    qry = session.query(Member).outerjoin(SettlementData, SettlementData.member_id == Member.id).join(MemberClass, MemberClass.member_id == Member.id).group_by(Member.id)

    if status:
        qry = qry.filter(SettlementData.status == status)

    if class_code:
        qry = qry.filter(MemberClass.class_code == class_code)

    qry = qry.filter(SettlementData.type != 'PG', SettlementData.member_id != 1)

    if s_reg_date and e_reg_date:
        qry = qry.filter(SettlementData.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(SettlementData.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(SettlementData.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(Member.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()
    # datas = qry.all()

    return ListDataMember(total=total, datas=datas)


@router.get("/shipping", response_model=ListShipData, name="정산 목록 (배송비)")
def shipping_list(member_id: Optional[int] = None,
                  kind: Optional[str] = None,
                  status: Optional[str] = Query(default=None, description="상태"),
                  s_reg_date: Optional[date] = Query(default=None, description="시작일"),
                  e_reg_date: Optional[date] = Query(default=None, description="종료일"),
                  offset: int = 0, limit: int = 20,
                  session: Session = Depends(db.session),
                  user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    qry = session.query(SettlementShip)
    sum_qry = session.query(func.sum(SettlementShip.amount))

    if status:
        qry = qry.filter(SettlementShip.status == status)
        sum_qry = sum_qry.filter(SettlementShip.status == status)

    if member_id:
        if member_id == 1:
            if not user.admin == "Y":
                raise exc.PermissionEx
        qry = qry.filter(SettlementShip.member_id == member_id)
        sum_qry = sum_qry.filter(SettlementShip.member_id == member_id)

    if kind:
        if kind == 'PG':
            if not user.admin == "Y":
                raise exc.PermissionEx
        qry = qry.filter(SettlementShip.type == kind)
        sum_qry = sum_qry.filter(SettlementShip.type == kind)
    else:
        qry = qry.filter(SettlementShip.type != 'PG')
        sum_qry = sum_qry.filter(SettlementShip.type != 'PG')

    if s_reg_date and e_reg_date:
        qry = qry.filter(SettlementShip.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
        sum_qry = sum_qry.filter(SettlementShip.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(SettlementShip.reg_date > s_reg_date)
        sum_qry = sum_qry.filter(SettlementShip.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(SettlementShip.reg_date < D().make235959(e_reg_date))
        sum_qry = sum_qry.filter(SettlementShip.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    total_sum = sum_qry.scalar()
    # qry = qry.order_by(SettlementShip.reg_date.desc())
    # datas = qry.offset(offset).limit(limit).all()
    datas = qry.all()

    return ListShipData(total=total, total_sum=total_sum, datas=datas)


@router.post("/shipping", response_model=Success, name="정산 데이터 일괄 수정 (배송비)")
def settlement_s_update(indata: ModSettlementData,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=['write:settlement'])):
    member = {}
    for target in indata.ids:
        data = SettlementShip.get(session=session, id=target)
        if not data:
            raise exc.NotFoundDataEx
        if indata.status:
            data.status = indata.status

        if indata.reject:
            data.reject = indata.reject

        if member.get(data.member_id):
            member.get(data.member_id)['settlement_targets'].append(data)
        else:
            member[data.member_id] = {
                "member": data.member,
                "settlement_targets": [data]
            }
    session.commit()

    if indata.status == 'C':
        for row in member.values():
            enc_mobile = row['member'].mobile
            if enc_mobile:
                mobile = AES256(AES_KEY, AES_IV).decrypt(enc_mobile)
                count = len(row['settlement_targets'])
                total = 0
                for s in row['settlement_targets']:
                    total += s.amount
                date_range_str = f"\n기간 {indata.date_range}" if indata.date_range else ''
                msg = f"""[코니아 배송비 정산 안내]{date_range_str}\n정산 대상 확정\n{int(total):,}원 ({count:,}건)"""
                print(msg)

    # 로깅
    # log_data = LogStoreDataIn(action="상점 테마 상품 연결", store_code=store_code, msg=log_msg("msg", f'테마 - {theme.name}:{theme.id} / 대상 - {added_prd_id}'), writer=f"{user.name}:{user.id}")
    # LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/shipping/member", response_model=ListDataMember, name="정산 대상 회원 목록 (배송비)")
def member_s_list(status: Optional[str] = Query(default=None, description="상태"),
                  class_code: Optional[str] = Query(default=None, description="회원 타입"),
                  s_reg_date: Optional[date] = Query(default=None, description="시작일"),
                  e_reg_date: Optional[date] = Query(default=None, description="종료일"),
                  offset: int = 0, limit: int = 20,
                  session: Session = Depends(db.session),
                  user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    qry = session.query(Member).outerjoin(SettlementShip, SettlementShip.member_id == Member.id).join(MemberClass, MemberClass.member_id == Member.id).group_by(Member.id)

    if status:
        qry = qry.filter(SettlementShip.status == status)

    if class_code:
        qry = qry.filter(MemberClass.class_code == class_code)

    qry = qry.filter(SettlementShip.type != 'PG', SettlementShip.member_id != 1)

    if s_reg_date and e_reg_date:
        qry = qry.filter(SettlementShip.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(SettlementShip.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(SettlementShip.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(Member.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()
    # datas = qry.all()

    return ListDataMember(total=total, datas=datas)


@router.get("/history/{target}", response_model=ListSettlementHistoryData, name="정산 내역 산출 히스토리")
def history(target: int,
            kind: str = Query(title='종류'),
            session: Session = Depends(db.session),
            user: MemberToken = Security(token_user, scopes=["read:settlement"])):
    if kind == 'prd':
        target_data = session.query(SettlementData).filter(SettlementData.id == target).first()
    else:
        target_data = session.query(SettlementShip).filter(SettlementShip.id == target).first()

    if target_data is None:
        raise exc.NotFoundDataEx

    if kind == 'prd':
        datas = session.query(SettlementData).filter(SettlementData.account_raw_id == target_data.account_raw_id).all()
    else:
        datas = session.query(SettlementShip).filter(SettlementShip.order_shipping_id == target_data.order_shipping_id).all()

    return ListSettlementHistoryData(datas=datas)
