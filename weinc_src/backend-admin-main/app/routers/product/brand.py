from typing import List

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Product, Brand, ProductBrand

from app.models.common import Success
from app.models.product.category_brand import *
from app.models.auth import MemberToken

router = APIRouter(prefix='/product/brand')


@router.post("", response_model=Success, name="브랜드 등록")
def add_brand(indata: AddCategoryBrand,
              session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:brand"])):
    brand = Brand.get(session, name=indata.name)
    if brand:
        raise exc.AlreadyDataEx

    indata_dict = indata.dict()
    Brand.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("", response_model=List[DataCategoryBrand], name="브랜드 목록")
def list_brand(pid: Optional[int] = Query(default=None, description="상위 브랜드 ID"),
               name: Optional[str] = Query(default=None, description="브랜드 이름"),
               offset: int = 0, limit: int = 100,
               session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=[])):
    qry = session.query(Brand).filter(Brand.pid == pid)

    if name:
        if not pid:
            qry = session.query(Brand).filter(Brand.name.like(f'%{name}%'))
        else:
            qry = qry.filter(Brand.name.like(f'%{name}%'))

    return qry.offset(offset).limit(limit).all()


@router.post("/link", response_model=Success, name="브랜드 상품 연결")
def link_brand(brand_id: List[int], product_id: int,
               session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:product"])):
    for b_id in brand_id:
        data = ProductBrand.get(session=session, brand_id=b_id, product_id=product_id)
        if data:
            continue

        mapping_data = {
            "product_id": product_id,
            "brand_id": b_id,
        }
        ProductBrand.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/link", response_model=Success, name="브랜드 상품 연결 해제")
def unlink_brand(product_id: int,
                 session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:product"])):
    data = Product.get(session=session, id=product_id)
    if not data:
        raise exc.NotFoundDataEx

    ProductBrand.filter(session=session, product_id=product_id).delete(auto_commit=True)

    return Success()


@router.put("/{brand_id}", response_model=Success, name="브랜드 수정")
def mod_brand(brand_id: int, indata: ModCategoryBrand,
              session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:brand"])):
    data: Brand = Brand.get(session=session, id=brand_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()
