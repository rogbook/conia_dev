import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, MemberStore, StoreProduct, StoreTheme, Customer, AbleTarget
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success
from app.models.store import *
from app.utils.common_utils import list_to_dict, make_tree
from app.utils.jwt import token_user

router = APIRouter(prefix='/store')


@router.get("/{store_code}", response_model=DataStore, name="상점 정보")
def get_store(store_code: str,
              session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    data_list_top = StoreTheme.filter(session=session, store_code=store_code).all()
    data = list_to_dict(data_list_top)
    theme_list = make_tree(data)

    return data


@router.post("/{store_code}/user", response_model=Success, name="상점 이용자 등록")
def add_member_store(store_code: str, indata: AddMemberStore,
                     session: Session = Depends(db.session)):
    member = Customer.get(session, email=indata.email)
    if not member:
        raise exc.NotFoundDataEx
    if not bcrypt.checkpw(indata.password.encode("utf8"), member.password.encode("utf8")):
        raise exc.NotFoundDataEx

    store = Store.get(session, code=store_code)
    if not store:
        raise exc.NotFoundDataEx

    ms = MemberStore()
    ms.customer_id = member.id
    ms.store_code = store_code
    if indata.value:
        ms.value = indata.value

    confirm_flag = False

    if store.able_target_use == "A":
        qry = session.query(AbleTarget).filter(AbleTarget.store_code == store_code,
                                               AbleTarget.unique_value == indata.value,
                                               AbleTarget.name == member.name,
                                               AbleTarget.mobile == member.mobile,
                                               AbleTarget.used == "N")
        target = qry.first()
        if target:
            ms.confirm = "Y"
            target.used = "Y"
            confirm_flag = True
    elif store.able_target_use == "F":
        if store.verify_code == indata.value:
            ms.confirm = "Y"
            confirm_flag = True
        else:
            return Success(msg="failed")

    session.add(ms)
    session.commit()

    if confirm_flag:
        return Success(msg="confirmed")
    else:
        return Success()


@router.get("/{store_code}/product", response_model=List[DataStoreProduct], name="상점 상품 목록")
def list_store_product_link(store_code: str,
                            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data_list = StoreProduct.filter(session=session, store_code=store_code).all()

    return data_list
