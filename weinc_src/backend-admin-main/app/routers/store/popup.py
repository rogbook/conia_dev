from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, StoreProduct, Product, LogStore, StorePopup
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, LogStoreDataIn
from app.models.store import *
from app.utils.common_utils import delete_layout_product, log_msg
from app.utils.jwt import token_user

router = APIRouter(prefix='/store')


@router.post("/{store_code}/popup", response_model=Success, name="상점 팝업 생성")
def add_store_popup(store_code: str, indata: AddStorePopup,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    popup = StorePopup.create(session, True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action="상점 팝업 생성", store_code=store_code, msg=log_msg("msg", f'대상 - {popup.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/popup", response_model=ListStorePopup, name="상점 팝업 목록")
def list_store_popup(store_code: str,
                     title: Optional[str] = Query(default=None, description="제목"),
                     offset: int = 0, limit: int = 20,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['read:store'])):
    qry = session.query(StorePopup).filter(StorePopup.store_code == store_code, StorePopup.status != 'D')

    if title:
        qry = qry.filter(StorePopup.title.like(f'%{title}%'))

    total = qry.count()
    qry = qry.order_by(StorePopup.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListStorePopup(total=total, datas=data_list)


@router.delete("/{store_code}/popup/{target}", response_model=Success, name="상점 팝업 삭제")
def del_store_popup(store_code: str, target: int,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store'])):
    popup = StorePopup.get(session, store_code=store_code, id=target)

    if not popup:
        raise exc.NotFoundDataEx

    popup.update(session, True, status='D')

    # 로깅
    log_data = LogStoreDataIn(action="상점 팝업 삭제", store_code=store_code, msg=log_msg("msg", f'대상 - {popup.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.put("/{store_code}/popup/{target}", response_model=Success, name="상점 팝업 수정")
def mod_store_popup(store_code: str, target: int, indata: ModStorePopup,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=['write:store'])):
    popup = StorePopup.get(session, store_code=store_code, id=target)

    if not popup:
        raise exc.NotFoundDataEx

    change_data = popup.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action=f"상점 팝업 수정 ({popup.id})", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()
