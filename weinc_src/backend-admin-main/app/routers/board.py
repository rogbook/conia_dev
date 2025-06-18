from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Faq, FaqCategory, Notice, Qna, QnaStore

from app.models.common import Success, CreatedID
from app.models.board import *
from app.models.auth import MemberToken

router = APIRouter(prefix='/board')


@router.post("/faq", response_model=CreatedID, name="FAQ 등록")
def add_faq(indata: AddFaq,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    indata_dict = indata.dict()

    data: Faq = Faq.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("/faq", response_model=List[DataFaq], name="FAQ 목록")
def list_faq(target: Optional[str] = Query(default=None, description="FAQ 대상"),
             offset: int = 0, limit: int = 20,
             session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    if target:
        data_list = Faq.filter(session=session, target=target).order_by("-reg_date").all()
    else:
        data_list = Faq.filter(session=session).order_by("-reg_date").all()

    return data_list


@router.get("/faq/category", response_model=List[DataFaqCate], name="FAQ 분류목록")
def list_faq_cate(session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data_list = FaqCategory.filter(session=session).all()

    return data_list


@router.get("/faq/{faq_id}", response_model=DataFaq, name="FAQ 상세")
def get_faq(faq_id: int,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Faq = Faq.get(session=session, id=faq_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/faq/{faq_id}", response_model=Success, name="FAQ 수정")
def mod_faq(faq_id: int, indata: ModFaq,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Faq = Faq.get(session=session, id=faq_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.delete("/faq/{faq_id}", response_model=Success, name="FAQ 삭제")
def del_faq(faq_id: int,
            session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:faq"])):
    data: Faq = Faq.get(session=session, id=faq_id)
    if not data:
        raise exc.NotFoundDataEx

    session.delete(data)
    session.commit()

    return Success()


@router.post("/notice", response_model=CreatedID, name="공지사항 등록")
def add_notice(indata: AddNotice,
               session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    indata_dict = indata.dict()

    data: Notice = Notice.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("/notice", response_model=ListNotice, name="공지사항 목록")
def list_notice(target: Optional[str] = Query(default=None, description="공지사항 대상"),
                sub_target: Optional[str] = Query(default=None, description="서브 타겟"),
                admin: Optional[str] = Query(default=None, description="관리여부"),
                offset: int = 0, limit: int = 20,
                session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    qry = session.query(Notice)

    if target:
        if target.startswith('partner'):
            if sub_target:
                if admin:
                    qry = qry.filter(Notice.target.endswith(sub_target))
                else:
                    qry = qry.filter(or_(Notice.target == target, Notice.target.endswith(sub_target)))
            else:
                qry = qry.filter(Notice.target.startswith('partner'))
        else:
            qry = qry.filter(Notice.target == target)

    total = qry.count()
    qry = qry.order_by(Notice.mod_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListNotice(total=total, datas=datas)


@router.get("/notice/{notice_id}", response_model=DataNotice, name="공지사항 상세")
def get_notice(notice_id: int,
               session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Notice = Notice.get(session=session, id=notice_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/notice/{notice_id}", response_model=Success, name="공지사항 수정")
def mod_notice(notice_id: int, indata: ModeNotice,
               session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Notice = Notice.get(session=session, id=notice_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/qna", response_model=CreatedID, name="QNA 등록")
def add_qna(indata: AddQna,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    indata_dict = indata.dict()

    data: Qna = Qna.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("/qna", response_model=ListQna, name="QNA 목록")
def list_qna(q_member_id: Optional[int] = Query(default=None, description="질문자 아이디"),
             offset: int = 0, limit: int = 20,
             session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    qry = session.query(Qna).filter(Qna.qna_id == None)

    if q_member_id:
        qry = qry.filter(Qna.q_member_id == q_member_id)

    total = qry.count()
    qry = qry.order_by(Qna.mod_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListQna(total=total, datas=datas)


@router.get("/qna/{qna_id}", response_model=DataQna, name="QNA 상세")
def get_qna(qna_id: int,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Qna = Qna.get(session=session, id=qna_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/qna/{qna_id}", response_model=Success, name="QNA 수정")
def mod_qna(qna_id: int, indata: ModQna,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Qna = Qna.get(session=session, id=qna_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/qna/answer", response_model=CreatedID, name="QNA 답변 등록")
def add_qna_answer(qna_id: int, indata: AddQna,
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    # 질문이 없으면 답변 불가
    question: Qna = Qna.get(session=session, id=qna_id)
    if not question:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    # 답변 등록
    data: Qna = Qna.create(session, auto_commit=True, **indata_dict)

    # 질문 상태 업데이트
    question.update_optional(session=session, auto_commit=True, status='C')

    return CreatedID(id=data.id)


@router.get("/qna/answer/{qna_id}", response_model=DataQna, name="QNA 답변 상세")
def get_qna_answer(qna_id: int,
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: Qna = Qna.get(session=session, qna_id=qna_id)
    if not data:
        raise exc.NotFoundDataEx
    return data


@router.get("/qna-store", response_model=ListQnaStore, name="상점 QNA 목록")
def list_qna(customer_id: Optional[int] = Query(default=None, description="질문자 아이디"),
             store_code: Optional[str] = Query(default=None, description="상점 코드"),
             offset: int = 0, limit: int = 20,
             session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    qry = session.query(QnaStore).filter(QnaStore.qna_id == None, QnaStore.status != 'D')

    if customer_id:
        qry = qry.filter(QnaStore.customer_id == customer_id)

    if store_code:
        qry = qry.filter(QnaStore.store_code == store_code)

    total = qry.count()
    qry = qry.order_by(QnaStore.mod_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListQnaStore(total=total, datas=datas)


@router.get("/qna-store/{qna_id}", response_model=DataQnaStore, name="상점 QNA 상세")
def get_qna(qna_id: int,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: QnaStore = QnaStore.get(session=session, id=qna_id)
    if not data:
        raise exc.NotFoundDataEx

    a_data: QnaStore = QnaStore.get(session=session, qna_id=qna_id)
    if a_data:
        data.answer = DataQnaStore.from_orm(a_data)

    return data


@router.post("/qna-store/answer", response_model=CreatedID, name="상점 QNA 답변 등록")
def add_qna_answer(qna_id: int, indata: AddQnaStore,
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    # 질문이 없으면 답변 불가
    question: QnaStore = QnaStore.get(session=session, id=qna_id)
    if not question:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    # customer_id 임시 작업 (스키마상으로 NOT null이라 답변 등록 안됨)
    indata_dict['customer_id'] = question.customer_id
    # 답변 등록
    data: QnaStore = QnaStore.create(session, auto_commit=True, **indata_dict)

    # 질문 상태 업데이트
    question.update_optional(session=session, auto_commit=True, status='C')

    return CreatedID(id=data.id)


@router.put("/qna-store/answer/{answer_id}", response_model=Success, name="상점 QNA 답변 수정")
def mod_qna(answer_id: int, indata: ModQna,
            session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: QnaStore = QnaStore.get(session=session, id=answer_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()
