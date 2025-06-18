from typing import Optional
from datetime import date

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import ProductRequest, ProductRequestPrd
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success
from app.models.product.request import AddProductRequest, ModProductRequest, ListProductRequest, DetailProductRequest
from app.utils.jwt import token_user
from app.utils.date_utils import D

router = APIRouter(prefix='/product/request')


@router.post("", response_model=Success, name="상품 요청 등록")
def add(indata: AddProductRequest,
        session: Session = Depends(db.session),
        user: MemberToken = Security(token_user, scopes=["write:product_request"])):
    indata_dict = indata.dict()
    indata_dict.update(member_id=user.id)

    pr: ProductRequest = ProductRequest.create(session, auto_commit=True, **indata_dict)

    for prd_id in indata.product_ids:
        ProductRequestPrd.create(session, auto_commit=False, product_request_id=pr.id, product_id=prd_id)
    session.commit()

    return Success()


@router.get("", response_model=ListProductRequest, name="상품 요청 목록")
def datas(store_code: Optional[str] = Query(default=None, description="상점 코드"),
          status: Optional[str] = Query(default=None, description="상태 (R: 요청, C:완료, D:반려)"),
          member_id: Optional[int] = Query(default=None, description="요청자 id"),
          s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
          e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
          offset: int = 0, limit: int = 20,
          session: Session = Depends(db.session),
          user: MemberToken = Security(token_user, scopes=["read:product_request"])):
    qry = session.query(ProductRequest)

    if store_code:
        qry = qry.filter(ProductRequest.store_code.like(f'%{store_code}%'))

    if status:
        qry = qry.filter(ProductRequest.status == status)

    if member_id:
        qry = qry.filter(ProductRequest.member_id == member_id)

    if s_reg_date and e_reg_date:
        qry = qry.filter(ProductRequest.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(ProductRequest.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(ProductRequest.reg_date < D().make235959(e_reg_date))

    # 본인 요청
    # if user.scope 체크:
    #     qry = qry.filter(ProductRequest.member_id == user.id)

    total = qry.count()
    qry = qry.order_by(ProductRequest.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListProductRequest(total=total, datas=data_list)


@router.get("/{request_id}", response_model=DetailProductRequest, name="상품 요청 상세")
def data(request_id: int,
         session: Session = Depends(db.session),
         user: MemberToken = Security(token_user, scopes=["read:product_request"])):
    data: ProductRequest = ProductRequest.get(session=session, id=request_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/{request_id}", response_model=Success, name="상품 요청 수정")
def update(request_id: int, indata: ModProductRequest,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=["write:product_request"])):
    data: ProductRequest = ProductRequest.get(session=session, id=request_id)
    if not data:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    indata_dict.update(manager=user.id)

    data.update_optional(session=session, auto_commit=True, **indata_dict)

    return Success()


@router.delete("/{request_id}", response_model=Success, name="상품 요청 삭제")
def delete(request_id: int,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=["write:product_request"])):
    data: ProductRequest = ProductRequest.get(session=session, id=request_id)
    if not data:
        raise exc.NotFoundDataEx

    session.delete(data)
    session.commit()

    return Success()
