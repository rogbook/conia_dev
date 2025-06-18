from typing import List
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, StorePopup
from app.models.auth import MemberToken
from app.routers.views import auth, member, order, theme, product, category, board, terms, shop, ecoupon
from app.utils.common_utils import check_store, make_view_context_data, update_shop
from app.utils.jwt import token_user_option
from app.utils.templates import templates
from app.utils.date_utils import D

router = APIRouter()

router.include_router(auth.router)
router.include_router(member.router)
router.include_router(order.router)
router.include_router(theme.router)
router.include_router(shop.router)
router.include_router(product.router)
router.include_router(category.router)
router.include_router(board.router)
router.include_router(terms.router)
router.include_router(ecoupon.router)


@router.get("")
def index(req: Request, store_code: str,
          store: Store = Depends(check_store),
          session: Session = Depends(db.session), user: MemberToken = Depends(token_user_option)):

    context_data = make_view_context_data(session, req, store, user)
    update_shop(session, context_data)

    now = D().now

    if context_data.get("dupl_store"):
        popups: List[StorePopup] = StorePopup.filter(session, store_code=context_data.get("dupl_store").code, duplicate='Y', status="Y").order_by("sort").all()
    else:
        popups: List[StorePopup] = StorePopup.filter(session, store_code=store_code, status="Y").order_by("sort").all()
    target_popup = []
    for row in popups:
        if row.view_start_date and row.view_end_date:
            if row.view_start_date < now < row.view_end_date:
                target_popup.append(row)
        elif row.view_start_date:
            if row.view_start_date < now:
                target_popup.append(row)
        elif row.view_end_date:
            if now < row.view_end_date:
                target_popup.append(row)
        else:
            target_popup.append(row)
    context_data.update(popups=target_popup)

    return templates.TemplateResponse("index.jinja2", context=context_data)
