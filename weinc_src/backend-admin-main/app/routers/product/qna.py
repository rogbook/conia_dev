from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import ProductQna, Product
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.product.qna import *
from app.models.common import Success, CreatedID
from app.utils.jwt import token_user

router = APIRouter(prefix='/product/qna')


@router.get("", response_model=ListProductQna, name="상품 QNA 목록")
def list_qna(customer_id: Optional[int] = Query(default=None, description="질문자 아이디"),
             product_id: Optional[int] = Query(default=None, description="상품 아이디"),
             member_id: Optional[int] = Query(default=None, description="PA 아이디"),
             offset: int = 0, limit: int = 20,
             session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    qry = session.query(ProductQna).join(Product, Product.id == ProductQna.product_id).filter(ProductQna.product_qna_id == None, ProductQna.status != 'D')

    if member_id:
        qry = qry.filter(Product.member_id == member_id)

    if customer_id:
        qry = qry.filter(ProductQna.customer_id == customer_id)

    if product_id:
        qry = qry.filter(ProductQna.product_id == product_id)

    total = qry.count()
    qry = qry.order_by(ProductQna.mod_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListProductQna(total=total, datas=datas)


@router.get("/{qna_id}", response_model=DataProductQna, name="상품 QNA 상세")
def get_qna(qna_id: int,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: ProductQna = ProductQna.get(session=session, id=qna_id)
    if not data:
        raise exc.NotFoundDataEx
    result = DataProductQna.from_orm(data)

    a_data: ProductQna = ProductQna.get(session=session, product_qna_id=qna_id)
    if a_data:
        result.answer = DataProductQna.from_orm(a_data)

    return result


@router.post("/answer", response_model=CreatedID, name="상품 QNA 답변 등록")
def add_qna_answer(qna_id: int, indata: AddProductQnaAnswer,
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    # 질문이 없으면 답변 불가
    question: ProductQna = ProductQna.get(session=session, id=qna_id)
    if not question:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    indata_dict.update(product_qna_id=qna_id)
    # 답변 등록
    data: ProductQna = ProductQna.create(session, auto_commit=True, **indata_dict)

    # 질문 상태 업데이트
    question.update_optional(session=session, auto_commit=True, status='C')

    return CreatedID(id=data.id)


@router.put("/answer/{answer_id}", response_model=Success, name="상품 QNA 답변 수정")
def mod_qna(answer_id: int, indata: ModQna,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: ProductQna = ProductQna.get(session=session, id=answer_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()
