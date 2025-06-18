from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Commission, Product, LogCommission
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.commission import *
from app.models.common import Success, LogCommissionDataIn
from app.utils.jwt import token_user
from app.utils.common_utils import log_msg

router = APIRouter(prefix='/commission')


@router.get("", response_model=ListCommission, name="수수료 목록")
def list_commission(target_id: int = Query(description="조회 대상(회원)"),
                    member_id: Optional[int] = Query(default=None, description="중개 설정 대상(회원)"),
                    store_code: Optional[str] = Query(default=None, description="조회 대상(상점)"),
                    name: Optional[str] = Query(default=None, description="상품명"),
                    offset: int = 0, limit: int = 20,
                    session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:commission"])):
    qry = session.query(Commission).outerjoin(Product, Commission.product_id == Product.id)
    if member_id:
        qry = qry.filter(Commission.member_id == member_id, Commission.default == 'N')
    else:
        qry = qry.filter(Commission.target == target_id, Commission.default == 'N')

    if store_code:
        qry = qry.filter(Commission.store_code == store_code)

    if name:
        qry = qry.filter(Product.name.like(f"%{name}%"))

    total = qry.count()
    # qry = qry.order_by(Commission.mod_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListCommission(total=total, datas=datas)


@router.post("", response_model=Success, name="수수료 등록")
def add_commission(indata: AddCommission,
                   session: Session = Depends(db.session),
                   user: MemberToken = Security(token_user, scopes=["write:commission"])):
    # 권한 체크 본인/하위/전체

    new_data = Commission()
    new_data.target = indata.target
    if indata.target_type:
        new_data.target_type = indata.target_type

    if indata.store_code:
        new_data.store_code = indata.store_code
    if indata.product_id:
        new_data.product_id = indata.product_id
    if indata.member_id:
        new_data.member_id = indata.member_id

    new_data.type = indata.type
    new_data.value = indata.value
    new_data.kind = indata.kind
    # 지급방식 추가
    if indata.payment:
        new_data.payment = indata.payment

    session.add(new_data)
    session.commit()

    # 로깅
    log_data = LogCommissionDataIn(action="등록", member_id=indata.target, msg=log_msg("msg", f"{indata.dict()}"), writer=f"{user.name}:{user.id}")
    LogCommission.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.put("", response_model=Success, name="수수료 수정")
def mod_commission(indata: ModCommission,
                   session: Session = Depends(db.session),
                   user: MemberToken = Security(token_user, scopes=["write:commission"])):
    # 권한 체크 본인/하위/전체

    data = Commission.get(session, id=indata.id)
    if not data:
        raise exc.NotFoundDataEx

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())
    change_data.insert(0, {"id": indata.id})

    # 로깅
    log_data = LogCommissionDataIn(action="수정", member_id=data.target, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogCommission.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{commission_id}", response_model=Success, name="수수료 삭제")
def del_commission(commission_id: int = Query(title="수수료 ID"),
                   session: Session = Depends(db.session),
                   user: MemberToken = Security(token_user, scopes=["write:commission"])):
    data = Commission.get(session, id=commission_id)
    if not data:
        raise exc.NotFoundDataEx
    del_data = data.__dict__.copy()
    del del_data["_sa_instance_state"]

    session.delete(data)
    session.commit()

    # 로깅
    log_data = LogCommissionDataIn(action="삭제", member_id=data.target, msg=log_msg("msg", f"{del_data}"), writer=f"{user.name}:{user.id}")
    LogCommission.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/default", response_model=DataDefaultCommission, name="기본 수수료")
def get_default(member_id: int = Query(description="조회 대상(회원)"),
                kind: str = Query(default=None, description="kind"),
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=["read:commission"])):
    if kind and kind == 'ship':
        if member_id == 1:
            data = session.query(Commission).filter(Commission.target == 1, Commission.default == "Y", Commission.kind == kind).first()
        else:
            data = session.query(Commission).filter(Commission.target == 1, Commission.member_id == member_id, Commission.kind == kind).first()
    else:
        data = session.query(Commission).filter(Commission.target == member_id, Commission.default == "Y").first()

    if data:
        return DataDefaultCommission(id=data.id, default_commission=data.value)

    return DataDefaultCommission(id=0, default_commission=0)


@router.get("/pg", response_model=List[DataCommission], name="PG 수수료")
def get_pg(session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=["read:commission"])):
    data = session.query(Commission).filter(Commission.target == 1, Commission.target_type == "PG").all()

    return data


@router.put("/default", response_model=Success, name="기본 수수료 수정")
def mod_default(indata: ModDefaultCommission,
                member_id: int = Query(description="변경 대상(회원)"),
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=["write:commission"])):
    data = session.query(Commission).filter(Commission.target == member_id, Commission.default == "Y").first()

    if not data:
        new_data = Commission()
        new_data.target = member_id
        new_data.default = "Y"
        new_data.type = indata.type
        new_data.value = indata.value
        new_data.kind = 'prd'
        session.add(new_data)
        session.commit()

        log_data = LogCommissionDataIn(action="기본 수수료 등록", member_id=member_id, msg=log_msg("msg", f"등록"), writer=f"{user.name}:{user.id}")
    else:
        change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())
        log_data = LogCommissionDataIn(action="기본 수수료 수정", member_id=data.target, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")

    # 로깅
    LogCommission.create(session, auto_commit=True, **log_data.dict())

    return Success()
