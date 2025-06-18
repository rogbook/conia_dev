from typing import List, Optional

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Badge, ProductBadge

from app.models.common import Success
from app.models.product.badge import DataBadge, AddBadge, ModBadge
from app.models.auth import MemberToken

router = APIRouter(prefix='/product/badge')


@router.post("", response_model=Success, name="뱃지 등록")
def add(indata: AddBadge,
        session: Session = Depends(db.session),
        user: MemberToken = Security(token_user, scopes=["write:badge"])):
    indata_dict = indata.dict()
    Badge.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("", response_model=List[DataBadge], name="뱃지 목록")
def datas(name: Optional[str] = Query(default=None, description="뱃지 이름"),
          session: Session = Depends(db.session),
          user: MemberToken = Security(token_user, scopes=[])):
    qry = session.query(Badge)

    if name:
        qry = qry.filter(Badge.name.like(f'%{name}%'))

    return qry.all()


@router.post("/link", response_model=Success, name="뱃지 상품 연결")
def link(badge_id: List[int], product_id: int,
         session: Session = Depends(db.session),
         user: MemberToken = Security(token_user, scopes=["write:product"])):
    for b_id in badge_id:
        data = ProductBadge.get(session=session, badge_id=b_id, product_id=product_id)
        if data:
            continue

        mapping_data = {
            "product_id": product_id,
            "badge_id": b_id,
        }
        ProductBadge.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/link", response_model=Success, name="뱃지 상품 연결 해제")
def unlink(badge_id: List[int], product_id: int,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=["write:product"])):
    for b_id in badge_id:
        ProductBadge.filter(session=session, badge_id=b_id, product_id=product_id).delete(auto_commit=True)

    return Success()


@router.put("/{badge_id}", response_model=Success, name="뱃지 수정")
def update(badge_id: int, indata: ModBadge,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=["write:badge"])):
    data: Badge = Badge.get(session=session, id=badge_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()
