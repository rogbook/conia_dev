from typing import Optional

from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.conn import db
from app.database.schema import ProductReview, ProductReviewPhoto, Product, StoreProduct
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success
from app.models.product.review import ListDataReview
from app.utils.jwt import token_user

router = APIRouter(prefix='/product/review')


@router.get("", response_model=ListDataReview, name="리뷰 목록")
def review(product_id: Optional[int] = Query(default=None, description="상품 아이디"),
           member_id: Optional[int] = Query(default=None, description="PA idx"),
           store_code: Optional[str] = Query(default=None, description="상점 코드(상점에서 팔고 있는 상품만)"),
           offset: int = 0, limit: int = 20,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=["read:product_review"])):
    if member_id:
        qry = session.query(ProductReview).join(Product, and_(ProductReview.product_id == Product.id, Product.member_id == member_id)).filter(ProductReview.status == 'Y')
    elif store_code:
        qry = session.query(ProductReview).join(StoreProduct, and_(ProductReview.product_id == StoreProduct.product_id, StoreProduct.store_code == store_code)).filter(ProductReview.status == 'Y')
    else:
        qry = session.query(ProductReview).filter(ProductReview.status == 'Y')

    if product_id:
        qry = qry.filter(ProductReview.product_id == product_id)

    total = qry.count()
    qry = qry.order_by(ProductReview.mod_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListDataReview(total=total, datas=datas)


@router.put("/{review_id}", response_model=Success, name="리뷰 삭제")
def del_review(review_id: int,
               session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=["write:product_review"])):
    data: ProductReview = ProductReview.get(session=session, id=review_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, status="D")

    return Success()


@router.delete("/{review_id}/photo/{photo_id}", response_model=Success, name="상품 리뷰 사진 삭제")
def del_review_photo(review_id: int,
                     photo_id: int,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=["write:product_review"])):
    data: ProductReviewPhoto = ProductReviewPhoto.get(session=session, id=photo_id, product_review_id=review_id)
    if not data:
        raise exc.NotFoundDataEx

    session.delete(data)
    session.commit()

    return Success()
