import os
from datetime import date

from fastapi import APIRouter, Depends, Query, Security
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, StoreBoardGroup, StoreBoard, StoreBoardCmt, LogStore
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, LogStoreDataIn
from app.models.store import *
from app.utils.common_utils import log_msg
from app.utils.jwt import token_user
from app.utils.date_utils import D

router = APIRouter(prefix='/store')


@router.post("/{store_code}/board-group", response_model=Success, name="상점 게시판 그룹 생성")
def add_group(store_code: str, indata: AddBoardGroup,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    in_data = indata.dict()
    in_data.update(store_code=store_code)

    target = StoreBoardGroup.create(session, True, **in_data)

    # 로깅
    log_data = LogStoreDataIn(action="상점 게시판 그룹 생성", store_code=store_code, msg=log_msg("msg", f'대상 - {target.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/board-group", response_model=ListBoardGroup, name="상점 게시판 그룹 목록")
def list_group(store_code: str,
               name: Optional[str] = Query(default=None, description="이름"),
               offset: int = 0, limit: int = 20,
               session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=['read:store'])):
    qry = session.query(StoreBoardGroup).filter(StoreBoardGroup.store_code == store_code, StoreBoardGroup.status != 'D')

    if name:
        qry = qry.filter(StoreBoardGroup.title.like(f'%{name}%'))

    total = qry.count()
    qry = qry.order_by(StoreBoardGroup.id.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListBoardGroup(total=total, datas=data_list)


@router.delete("/{store_code}/board-group/{target}", response_model=Success, name="상점 게시판 그룹 삭제")
def del_group(store_code: str, target: int,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    target = StoreBoardGroup.get(session, store_code=store_code, id=target)

    if not target:
        raise exc.NotFoundDataEx

    target.update(session, True, status='D')

    # 로깅
    log_data = LogStoreDataIn(action="상점 게시판 그룹 삭제", store_code=store_code, msg=log_msg("msg", f'대상 - {target.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.put("/{store_code}/board-group/{target}", response_model=Success, name="상점 게시판 그룹 수정")
def mod_group(store_code: str, target: int, indata: ModBoardGroup,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    target = StoreBoardGroup.get(session, store_code=store_code, id=target)

    if not target:
        raise exc.NotFoundDataEx

    change_data = target.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action=f"상점 게시판 그룹 수정 ({target.id})", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.post("/{store_code}/board", response_model=Success, name="상점 게시글 생성")
def add_board(store_code: str, indata: AddBoard,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    group = StoreBoardGroup.get(session, store_code=store_code, id=indata.store_board_group_id)
    if not group:
        raise exc.NotFoundDataEx

    target = StoreBoard.create(session, True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action="상점 게시글 생성", store_code=store_code, msg=log_msg("msg", f'대상 - {target.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/board", response_model=ListBoard, name="상점 게시판 글 목록")
def list_board(store_code: str,
               group_id: int,
               title: Optional[str] = Query(default=None, description="제목"),
               s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
               e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
               offset: int = 0, limit: int = 20,
               session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=['read:store'])):
    group = StoreBoardGroup.get(session, store_code=store_code, id=group_id)

    if not group:
        raise exc.NotFoundDataEx

    qry = session.query(StoreBoard).filter(StoreBoard.store_board_group_id == group_id, StoreBoard.status != 'D')

    if title:
        qry = qry.filter(StoreBoard.title.like(f'%{title}%'))

    if s_reg_date and e_reg_date:
        qry = qry.filter(StoreBoard.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(StoreBoard.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(StoreBoard.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(StoreBoard.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListBoard(total=total, datas=data_list)


@router.delete("/{store_code}/board/{target}", response_model=Success, name="상점 게시글 삭제")
def del_board(store_code: str, target: int,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    target = StoreBoard.get(session, id=target)

    if not target:
        raise exc.NotFoundDataEx

    target.update(session, True, status='D')

    # 로깅
    log_data = LogStoreDataIn(action="상점 게시글 삭제", store_code=store_code, msg=log_msg("msg", f'대상 - {target.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.put("/{store_code}/board/{target}", response_model=Success, name="상점 게시글 수정")
def mod_board(store_code: str, target: int, indata: ModBoard,
              session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=['write:store'])):
    target = StoreBoard.get(session, id=target)

    if not target:
        raise exc.NotFoundDataEx

    change_data = target.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action=f"상점 게시글 수정 ({target.id})", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.post("/{store_code}/board-comment", response_model=Success, name="상점 게시글 댓글 생성")
def add_comment(store_code: str, indata: AddBoardComment,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=['write:store'])):
    data: Store = Store.get(session=session, code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    board = StoreBoard.get(session, id=indata.store_board_id)
    if not board:
        raise exc.NotFoundDataEx

    target = StoreBoardCmt.create(session, True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action="댓글 생성", store_code=store_code, msg=log_msg("msg", f'대상 - {target.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{store_code}/board-comment", response_model=ListBoardComment, name="상점 게시판 글 댓글 목록")
def list_comment(store_code: str,
                 board_id: int,
                 q: Optional[str] = Query(default=None, description="내용"),
                 s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                 e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                 # offset: int = 0, limit: int = 20,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=['read:store'])):
    board = StoreBoard.get(session, id=board_id)

    if not board:
        raise exc.NotFoundDataEx

    qry = session.query(StoreBoardCmt).filter(StoreBoardCmt.store_board_id == board_id, StoreBoardCmt.status != 'D')

    if q:
        qry = qry.filter(StoreBoardCmt.title.like(f'%{q}%'))

    if s_reg_date and e_reg_date:
        qry = qry.filter(StoreBoardCmt.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(StoreBoardCmt.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(StoreBoardCmt.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(StoreBoardCmt.reg_date.desc())
    # data_list = qry.offset(offset).limit(limit).all()
    data_list = qry.all()

    return ListBoardComment(total=total, datas=data_list)


@router.get("/{store_code}/board-comment/excel", name="상점 게시판 글 댓글 엑셀 다운로드")
def excel_comment(store_code: str,
                  board_id: int,
                  q: Optional[str] = Query(default=None, description="내용"),
                  s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                  e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                  # offset: int = 0, limit: int = 20,
                  session: Session = Depends(db.session),
                  user: MemberToken = Security(token_user, scopes=['read:store'])):
    board = StoreBoard.get(session, id=board_id)

    if not board:
        raise exc.NotFoundDataEx

    qry = session.query(StoreBoardCmt).filter(StoreBoardCmt.store_board_id == board_id, StoreBoardCmt.status != 'D', StoreBoardCmt.p_id == None, StoreBoardCmt.member_id == None)

    if q:
        qry = qry.filter(StoreBoardCmt.title.like(f'%{q}%'))

    if s_reg_date and e_reg_date:
        qry = qry.filter(StoreBoardCmt.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(StoreBoardCmt.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(StoreBoardCmt.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(StoreBoardCmt.reg_date.desc())
    # data_list = qry.offset(offset).limit(limit).all()
    data_list = qry.all()

    import openpyxl
    file_name = f'ConiaBoardComment-{board.id}-{D.now_str_trim()}.xlsx'
    file_path = os.path.join(os.getcwd(), 'app/upload/', file_name)
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(["작성자", "아이디", "연락처", "상점명", "작성 내용", "등록일시"])

    for row in data_list:
        mobile = AES256(AES_KEY, AES_IV).decrypt(row.customer.mobile)
        sheet.append([row.customer.name, row.customer.email, mobile, row.store.title, row.comment, row.reg_date])
    wb.save(file_path)

    return FileResponse(file_path, filename=file_name)


@router.delete("/{store_code}/board-comment/{target}", response_model=Success, name="상점 게시글 댓글 삭제")
def del_comment(store_code: str, target: int,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=['write:store'])):
    target = StoreBoardCmt.get(session, id=target)

    if not target:
        raise exc.NotFoundDataEx

    target.update(session, True, status='D')

    # 로깅
    log_data = LogStoreDataIn(action="댓글 삭제", store_code=store_code, msg=log_msg("msg", f'대상 - {target.id}'), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    session.commit()

    return Success()


@router.put("/{store_code}/board-comment/{target}", response_model=Success, name="상점 게시글 댓글 수정")
def mod_comment(store_code: str, target: int, indata: ModBoardComment,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=['write:store'])):
    target = StoreBoardCmt.get(session, id=target)

    if not target:
        raise exc.NotFoundDataEx

    change_data = target.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogStoreDataIn(action=f"댓글 수정 ({target.id})", store_code=store_code, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogStore.create(session, auto_commit=True, **log_data.dict())

    return Success()
