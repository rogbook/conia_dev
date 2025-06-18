from typing import Union

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.utils.common_utils import get_ip
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import StoreBoardCmt, QnaStore, ProductQna

from app.models.common import Success, CreatedID
from app.models.board import *
from app.models.auth import MemberToken

router = APIRouter(prefix='/board')


@router.post("/comment", response_model=CreatedID, name="댓글 등록")
def add_comment(indata: AddComment,
                req: Request,
                session: Session = Depends(db.session),
                user: MemberToken = Depends(token_user)):
    indata_dict = indata.dict()
    indata_dict.update(customer_id=user.id)
    indata_dict.update(ip=get_ip(req))

    data: StoreBoardCmt = StoreBoardCmt.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.delete("/comment/{target_id}", response_model=Success, name="댓글 삭제")
def del_comment(target_id: int,
                session: Session = Depends(db.session),
                user: MemberToken = Depends(token_user)):
    data: StoreBoardCmt = StoreBoardCmt.get(session, id=target_id, customer_id=user.id)

    if not data:
        raise exc.NotFoundDataEx

    data.update(session=session, auto_commit=True, status='D')

    return Success()


@router.delete("/qna/{target_id}", response_model=Success, name="문의 삭제")
def del_qna(target_id: int,
            session: Session = Depends(db.session),
            user: MemberToken = Depends(token_user)):
    data: QnaStore = QnaStore.get(session, id=target_id, customer_id=user.id)

    if not data:
        raise exc.NotFoundDataEx

    data.update(session=session, auto_commit=True, status='D')

    return Success()


@router.delete("/qna_prd/{target_id}", response_model=Success, name="상품문의 삭제")
def del_qna_prd(target_id: int,
                session: Session = Depends(db.session),
                user: MemberToken = Depends(token_user)):
    data: ProductQna = ProductQna.get(session, id=target_id, customer_id=user.id)

    if not data:
        raise exc.NotFoundDataEx

    data.update(session=session, auto_commit=True, status='D')

    return Success()
