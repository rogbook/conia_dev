from typing import List, Optional

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Category, Product, ProductCategory

from app.models.common import Success
from app.models.product.category_brand import DataCategoryBrand, AddCategoryBrand, ModCategoryBrand
from app.models.auth import MemberToken

router = APIRouter(prefix='/product/category')


@router.post("", response_model=Success, name="카테고리 등록")
def add_category(indata: AddCategoryBrand,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=["write:category"])):
    if indata.pid:
        p_cate = Category.get(session, id=indata.pid)
        if not p_cate:
            raise exc.NotFoundDataEx

        cate = Category()
        cate.pid = indata.pid
        cate.name = indata.name
        if indata.description:
            cate.description = indata.description
        if indata.photo:
            cate.photo = indata.photo
        cate.depth = p_cate.depth + 1
        if p_cate.depth1_name:
            cate.depth1_name = p_cate.depth1_name
            cate.depth1_id = p_cate.depth1_id if p_cate.depth1_id else p_cate.id
        if p_cate.depth2_name:
            cate.depth2_name = p_cate.depth2_name
            cate.depth2_id = p_cate.depth2_id if p_cate.depth2_id else p_cate.id
        if p_cate.depth3_name:
            cate.depth3_name = p_cate.depth3_name
            cate.depth3_id = p_cate.depth3_id if p_cate.depth3_id else p_cate.id
    else:
        cate = Category()
        cate.name = indata.name
        if indata.description:
            cate.description = indata.description
        if indata.photo:
            cate.photo = indata.photo
        cate.depth = 1
        cate.depth1_name = indata.name

    session.add(cate)
    session.commit()

    return Success()


@router.get("", response_model=List[DataCategoryBrand], name="카테고리 목록")
def list_category(pid: Optional[int] = Query(default=None, description="상위 카테고리 ID"),
                  name: Optional[str] = Query(default=None, description="카테고리 이름"),
                  offset: int = 0, limit: int = 100,
                  session: Session = Depends(db.session),
                  user: MemberToken = Security(token_user, scopes=[])):
    qry = session.query(Category).filter(Category.pid == pid)

    if name:
        if not pid:
            qry = session.query(Category).filter(Category.name.like(f'%{name}%'))
        else:
            qry = qry.filter(Category.name.like(f'%{name}%'))

    return qry.offset(offset).limit(limit).all()


@router.post("/link", response_model=Success, name="카테고리 상품 연결")
def link_category(category_id: List[int], product_id: int,
                  session: Session = Depends(db.session),
                  user: MemberToken = Security(token_user, scopes=["write:product"])):
    for c_id in category_id:
        data = ProductCategory.get(session=session, category_id=c_id, product_id=product_id)
        if data:
            continue

        mapping_data = {
            "product_id": product_id,
            "category_id": c_id,
        }
        ProductCategory.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/link", response_model=Success, name="카테고리 상품 연결 해제")
def unlink_category(product_id: int,
                    session: Session = Depends(db.session),
                    user: MemberToken = Security(token_user, scopes=["write:product"])):
    data = Product.get(session=session, id=product_id)
    if not data:
        raise exc.NotFoundDataEx

    ProductCategory.filter(session=session, product_id=product_id).delete(auto_commit=True)

    return Success()


@router.put("/{category_id}", response_model=Success, name="카테고리 수정")
def mod_category(category_id: int, indata: ModCategoryBrand,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=["write:category"])):
    data: Category = Category.get(session=session, id=category_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()
