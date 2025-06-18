from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store
from app.utils.common_utils import check_store, make_view_context_data
from app.utils.templates import templates
from app.models.auth import MemberToken
from app.utils.jwt import token_user_option

router = APIRouter(prefix="/terms")


@router.get("")
def terms(req: Request,
          session: Session = Depends(db.session),
          store: Store = Depends(check_store),
          user: MemberToken = Depends(token_user_option)):
    context_data = make_view_context_data(session, req, store, user)

    return templates.TemplateResponse("terms.html", context=context_data)
