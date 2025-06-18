from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import WishProduct
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success
from app.utils.jwt import token_user

router = APIRouter(prefix='/wish')


@router.post("/{product_id}", response_model=Success, name="관심 상품 등록")
def wish(product_id: int,
         store_code: str = Query(title="상점 코드"),
         session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data = WishProduct.get(session, customer_id=member.id, product_id=product_id, store_code=store_code)

    if not data:
        WishProduct.create(session, auto_commit=True, customer_id=member.id, product_id=product_id, store_code=store_code)

    return Success()


@router.delete("/{product_id}", response_model=Success, name="관심 상품 삭제")
def wish(product_id: int,
         store_code: str = Query(title="상점 코드"),
         session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data = WishProduct.get(session, customer_id=member.id, product_id=product_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    session.delete(data)
    session.commit()

    return Success()
