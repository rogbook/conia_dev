from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Shop, ShopBadge
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, CreatedID
from app.models.user.shop import *
from app.utils.jwt import token_user

router = APIRouter(prefix='/shop')


@router.post("/{member_id}", response_model=CreatedID, name="매장 등록")
def add_shop(member_id: int,
             indata: AddShop,
             session: Session = Depends(db.session),
             user: MemberToken = Security(token_user, scopes=[])):
    shop = Shop.get(session=session, member_id=member_id)
    if shop:
        # 1계정 1매장 정책
        raise exc.AlreadyDataEx

    # if member_id != user.id:
    #     if "write:shop" not in user.scopes:
    #         raise exc.PermissionEx

    indata_dict = indata.dict()
    indata_dict.update(member_id=member_id)

    data = Shop.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("/{member_id}", response_model=DataShop, name="매장 정보")
def get_shop(member_id: int,
             session: Session = Depends(db.session),
             user: MemberToken = Security(token_user, scopes=[])):
    data = Shop.get(session=session, member_id=member_id)
    if not data:
        raise exc.NotFoundDataEx
    return data


@router.put("/{member_id}", response_model=Success, name="매장 수정")
def mod_shop(member_id: int, indata: ModShop,
             session: Session = Depends(db.session),
             user: MemberToken = Security(token_user, scopes=[])):
    data: Shop = Shop.get(session=session, member_id=member_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/badge/link", response_model=Success, name="뱃지 매장 연결")
def link(badge_id: List[int], shop_id: int,
         session: Session = Depends(db.session),
         user: MemberToken = Security(token_user, scopes=[])):
    for b_id in badge_id:
        data = ShopBadge.get(session=session, badge_id=b_id, shop_id=shop_id)
        if data:
            continue

        mapping_data = {
            "shop_id": shop_id,
            "badge_id": b_id,
        }
        ShopBadge.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/badge/link", response_model=Success, name="뱃지 매장 연결 해제")
def unlink(badge_id: List[int], shop_id: int,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=[])):
    for b_id in badge_id:
        ShopBadge.filter(session=session, badge_id=b_id, shop_id=shop_id).delete(auto_commit=True)

    return Success()
