from fastapi import APIRouter, Request, Depends, Query, Form
from sqlalchemy import or_
from sqlalchemy.orm import Session
from operator import itemgetter

from app.database.conn import db
from app.database.schema import Store, Notice, Faq, FaqCategory, ProductQna, ProductReview, QnaStore, StoreProduct, StoreBoardGroup, StoreBoard, StoreBoardCmt
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.utils.common_utils import check_store, make_view_context_data, list_to_dict
from app.utils.jwt import token_user_option, token_user
from app.utils.templates import templates
from app.utils.paging import Page
from app.utils.date_utils import D

router = APIRouter(prefix="/board")


@router.get("/notice")
def notice(req: Request,
           session: Session = Depends(db.session),
           q: str = Query(default=None),
           page: int = Query(default=1, gt=0),
           page_size: int = Query(default=50),
           store: Store = Depends(check_store),
           user: MemberToken = Depends(token_user)):
    pin_qry = session.query(Notice).filter(Notice.target == 'customer', Notice.pin == 'Y')
    pin_qry = pin_qry.filter(or_(Notice.store_code == store.code, Notice.store_code.is_(None)))
    pin_qry = pin_qry.order_by(Notice.mod_date.desc())
    pin_notice = pin_qry.all()

    qry = session.query(Notice).filter(Notice.target == 'customer', Notice.pin == 'N')
    qry = qry.filter(or_(Notice.store_code == store.code, Notice.store_code.is_(None)))
    qry = qry.order_by(Notice.mod_date.desc())

    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas = qry.all()

    paginate = Page(datas, page, page_size, total)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(notice_list=pin_notice + datas)
    context_data.update(paginate=paginate)

    return templates.TemplateResponse("account-notice.html", context=context_data)


@router.get("/faq")
def faq(req: Request,
        session: Session = Depends(db.session),
        q: str = Query(default=None),
        store: Store = Depends(check_store),
        user: MemberToken = Depends(token_user)):
    qry = session.query(Faq).filter(Faq.target == 'customer')
    qry = qry.filter(or_(Faq.store_code == store.code, Faq.store_code.is_(None)))

    datas = qry.all()

    faq_category = FaqCategory.filter(session).order_by('sort').all()

    category_dict = {}
    for row in datas:
        data = dict(
            title=row.title,
            contents=row.contents,
        )
        if category_dict.get(row.category):
            category_dict[row.category].append(data)
        else:
            category_dict[row.category] = [data]

    result = []
    for item in faq_category:
        if category_dict.get(item.category):
            result.append(dict(
                category=item.category,
                items=category_dict.get(item.category),
            ))

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(faq_list=result)

    return templates.TemplateResponse("account-faq.html", context=context_data)


@router.get("/qna")
def qna(req: Request,
        session: Session = Depends(db.session),
        store: Store = Depends(check_store),
        user: MemberToken = Depends(token_user)):
    qry = session.query(QnaStore).filter(QnaStore.customer_id == user.id, QnaStore.store_code == store.code, QnaStore.status != "D")
    qry = qry.order_by(QnaStore.reg_date.desc())

    pq_qry = session.query(ProductQna).filter(ProductQna.customer_id == user.id, ProductQna.store_code == store.code, ProductQna.status != "D")
    pq_qry = pq_qry.order_by(ProductQna.reg_date.desc())

    datas = qry.all()
    pq_datas = pq_qry.all()

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(qna_list=datas)
    context_data.update(product_qna_list=pq_datas)

    return templates.TemplateResponse("account-qna-list.html", context=context_data)


@router.get("/review")
def review(req: Request,
           session: Session = Depends(db.session),
           store: Store = Depends(check_store),
           user: MemberToken = Depends(token_user)):
    qry = session.query(ProductReview).join(StoreProduct, StoreProduct.product_id == ProductReview.product_id)
    qry = qry.filter(ProductReview.customer_id == user.id, ProductReview.status == "Y")
    qry = qry.order_by(ProductReview.reg_date.desc())

    datas = qry.all()

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(reviews=datas)

    return templates.TemplateResponse("account-reviews.html", context=context_data)


@router.get("/review/{review_id}")
def review_detail(req: Request,
                  review_id: int,
                  session: Session = Depends(db.session),
                  store: Store = Depends(check_store),
                  user: MemberToken = Depends(token_user)):
    qry = session.query(ProductReview).join(StoreProduct, StoreProduct.product_id == ProductReview.product_id)
    qry = qry.filter(ProductReview.customer_id == user.id, ProductReview.status == "Y", ProductReview.id == review_id)

    data = qry.first()

    if not data:
        raise exc.ViewNotFoundEx

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(review=data)

    return templates.TemplateResponse("account-review-detail.html", context=context_data)


@router.post("/qna/add")
def qna(req: Request,
        q_type: str = Form(),
        title: str = Form(),
        contents: str = Form(),
        session: Session = Depends(db.session),
        store: Store = Depends(check_store),
        user: MemberToken = Depends(token_user)):
    qna = QnaStore(type=q_type, title=title, contents=contents, store_code=store.code, customer_id=user.id, status="R")
    session.add(qna)
    session.commit()

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(result=True)

    return templates.TemplateResponse("account-qna-add.html", context=context_data)


@router.get("/qna/add")
def qna(req: Request,
        session: Session = Depends(db.session),
        store: Store = Depends(check_store),
        user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    return templates.TemplateResponse("account-qna-add.html", context=context_data)


@router.get("/qna/detail/{qna_id}")
def qna(req: Request,
        qna_id: int,
        session: Session = Depends(db.session),
        store: Store = Depends(check_store),
        user: MemberToken = Depends(token_user)):
    q_data = session.query(QnaStore).filter(QnaStore.id == qna_id).first()
    a_data = session.query(QnaStore).filter(QnaStore.qna_id == qna_id).first()

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(q_data=q_data)
    context_data.update(a_data=a_data)

    return templates.TemplateResponse("account-qna-detail.html", context=context_data)


@router.get("/product-qna/detail/{qna_id}")
def qna(req: Request,
        qna_id: int,
        session: Session = Depends(db.session),
        store: Store = Depends(check_store),
        user: MemberToken = Depends(token_user)):
    q_data = session.query(ProductQna).filter(ProductQna.id == qna_id).first()
    a_data = session.query(ProductQna).filter(ProductQna.product_qna_id == qna_id).first()

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(q_data=q_data)
    context_data.update(a_data=a_data)

    return templates.TemplateResponse("account-qna-product-detail.html", context=context_data)


@router.get("/{board_grp_id}")
def board_grp(req: Request,
              board_grp_id: int,
              page: int = Query(default=1, gt=0),
              page_size: int = Query(default=50),
              session: Session = Depends(db.session),
              store: Store = Depends(check_store),
              user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    board_group = StoreBoardGroup.get(session, id=board_grp_id, store_code=(context_data['dupl_store'].code if context_data['dupl_store'] else store.code), status='Y')

    if not board_group:
        raise exc.ViewNotFoundEx

    top_boards = session.query(StoreBoard).filter(StoreBoard.store_board_group_id == board_grp_id, StoreBoard.status == 'Y', StoreBoard.pin == 'Y').order_by(StoreBoard.sort.asc(), StoreBoard.mod_date.desc()).all()
    boards = session.query(StoreBoard).filter(StoreBoard.store_board_group_id == board_grp_id, StoreBoard.status == 'Y', StoreBoard.pin == 'N').order_by(StoreBoard.sort.asc(), StoreBoard.mod_date.desc()).all()

    pin_future_boards = []
    pin_able_boards = []
    pin_disable_boards = []

    now = D().now

    for board in top_boards:
        if board.view_start_date:
            if board.view_start_date > now:
                continue
        if board.view_end_date:
            if board.view_end_date < now:
                continue
        if board.start_date and board.end_date:
            if board.start_date <= now <= board.end_date:
                pin_able_boards.append(board)
            elif now <= board.end_date:
                pin_future_boards.append(board)
            else:
                pin_disable_boards.append(board)
        elif board.start_date:
            if board.start_date <= now:
                pin_able_boards.append(board)
            else:
                pin_future_boards.append(board)
        elif board.end_date:
            if board.end_date >= now:
                pin_able_boards.append(board)
            else:
                pin_disable_boards.append(board)
        else:
            pin_able_boards.append(board)

    future_boards = []
    able_boards = []
    disable_boards = []

    for board in boards:
        if board.view_start_date:
            if board.view_start_date > now:
                continue
        if board.view_end_date:
            if board.view_end_date < now:
                continue
        if board.start_date and board.end_date:
            if board.start_date <= now <= board.end_date:
                able_boards.append(board)
            elif now <= board.end_date:
                future_boards.append(board)
            else:
                disable_boards.append(board)
        elif board.start_date:
            if board.start_date <= now:
                able_boards.append(board)
            else:
                future_boards.append(board)
        elif board.end_date:
            if board.end_date >= now:
                able_boards.append(board)
            else:
                disable_boards.append(board)
        else:
            able_boards.append(board)

    pin_future_boards.extend(future_boards)
    pin_able_boards.extend(able_boards)
    pin_disable_boards.extend(disable_boards)

    context_data.update(page_title=board_group.name)
    context_data.update(board_grp_data=board_group)
    context_data.update(future_boards=pin_future_boards)
    context_data.update(able_boards=pin_able_boards)
    context_data.update(disable_boards=pin_disable_boards)

    return templates.TemplateResponse("board-list.html", context=context_data)


@router.get("/{board_grp_id}/detail/{target_id}")
def board(req: Request,
          board_grp_id: int,
          target_id: int,
          session: Session = Depends(db.session),
          store: Store = Depends(check_store),
          user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)
    board_group = StoreBoardGroup.get(session, id=board_grp_id, store_code=(context_data['dupl_store'].code if context_data['dupl_store'] else store.code), status='Y')

    if not board_group:
        raise exc.ViewNotFoundEx

    post = StoreBoard.get(session, id=target_id)
    from typing import List
    comments: List[StoreBoardCmt] = StoreBoardCmt.filter(session, store_board_id=target_id, status='Y').order_by("-reg_date").all()

    for comment in comments:
        if comment.customer:
            comment.writer_name = comment.customer.name
        elif comment.member:
            comment.writer_name = comment.member.name

    comment_data = list_to_dict(comments, include=["writer_name"])

    context_data.update(page_title=board_group.name)
    context_data.update(board_grp_data=board_group)
    context_data.update(post=post)
    context_data.update(comments=make_comment_tree(comment_data))

    return templates.TemplateResponse("board-detail.html", context=context_data)


def make_comment_tree(data):
    nodes = {}
    for i in data:
        idx, parent_idx = i['id'], i['p_id']
        nodes[idx] = i

    forest = []
    for i in data:
        idx, parent_idx = i['id'], i['p_id']
        node = nodes[idx]

        if parent_idx is None:
            parent_idx = idx

        if idx == parent_idx:
            forest.append(node)
            forest.sort(key=itemgetter('reg_date'), reverse=True)
        else:
            parent = nodes.get(parent_idx, None)
            if parent:
                if 'sub' not in parent:
                    parent['sub'] = []
                sub = parent['sub']
                sub.append(node)
                sub.sort(key=itemgetter('reg_date'), reverse=True)
            # else:
            #     forest.append(node)
            #     forest.sort(key=itemgetter('reg_date'))
    return forest
