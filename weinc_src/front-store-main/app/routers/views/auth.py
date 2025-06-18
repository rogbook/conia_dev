from typing import List
from fastapi import APIRouter, Request, Response, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.models.auth import MemberToken
from app.utils.templates import templates
from app.utils.jwt import token_user, token_user_option
from app.database.conn import db
from app.database.schema import Store, Cert, Customer
from app.utils.common_utils import check_store, make_view_context_data, get_base_url
from app.utils.crypto_utils import AES256
from app.common.consts import AES_KEY, AES_IV
from app.errors import exceptions as exc

router = APIRouter(prefix="/auth")


@router.get("/login")
def login(store_code: str, req: Request,
          store: Store = Depends(check_store),
          session: Session = Depends(db.session),
          user: MemberToken = Depends(token_user_option)):
    if user:
        if req.query_params.get("next"):
            return RedirectResponse(f"/{store_code}/{req.query_params.get('next')}")
        else:
            return RedirectResponse(f"/{store_code}")

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(base_url=get_base_url(req))

    ex_menu = context_data.get("exclude_menu")
    if ex_menu and 'MENU_LOGIN' in ex_menu:
        return RedirectResponse(f"/{store_code}")

    return templates.TemplateResponse("account-signin.html", context=context_data)


@router.get("/find-id")
def find_id(store_code: str,
            req: Request,
            store: Store = Depends(check_store),
            session: Session = Depends(db.session),
            user: MemberToken = Depends(token_user_option)):
    if user:
        return RedirectResponse(f"/{store_code}")

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(base_url=get_base_url(req))

    return templates.TemplateResponse("account-find-id.html", context=context_data)


@router.get("/find-id/result")
def find_id_result(req: Request,
                   store_code: str,
                   token_version_id: str = Query(),
                   store: Store = Depends(check_store),
                   session: Session = Depends(db.session),
                   user: MemberToken = Depends(token_user_option)):
    if user:
        return RedirectResponse(f"/{store_code}")

    data: Cert = Cert.get(session, req_token_version_id=token_version_id, status='Y')
    if not data:
        raise exc.BadRequestEx

    v = AES256(AES_KEY, AES_IV).encrypt(data.mobileno)

    data_list: List[Customer] = session.query(Customer).filter(Customer.mobile == v, Customer.status == 'Y').all()
    customer_list = []
    for customer in data_list:
        customer_list.append(customer.email)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(ids=customer_list)

    return templates.TemplateResponse("account-find-id-result.html", context=context_data)


@router.get("/password-recovery")
def password_recovery(store_code: str, req: Request,
                      store: Store = Depends(check_store),
                      session: Session = Depends(db.session),
                      user: MemberToken = Depends(token_user_option)):
    if user:
        return RedirectResponse(f"/{store_code}")

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(base_url=get_base_url(req))

    return templates.TemplateResponse("account-password-recovery.html", context=context_data)


@router.get("/password-reset")
def password_reset(req: Request,
                   store_code: str,
                   token: str = Query(),
                   store: Store = Depends(check_store),
                   session: Session = Depends(db.session),
                   user: MemberToken = Depends(token_user_option)):
    if user:
        return RedirectResponse(f"/{store_code}")

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(token=token)

    return templates.TemplateResponse("account-password-recovery-reset.html", context=context_data)


@router.get("/logout")
def logout(store_code: str, user: MemberToken = Depends(token_user)):
    res = RedirectResponse(f"/{store_code}")
    res.set_cookie('access_token', '', httponly=True)
    res.set_cookie('refresh_token', '', httponly=True)
    return res


@router.get("/cert-result")
def cert_result(req: Request):
    context_data = dict(
        request=req,
        token_version_id=req.query_params.get("token_version_id"),
        enc_data=req.query_params.get("enc_data"),
        integrity_value=req.query_params.get("integrity_value"),
    )

    return templates.TemplateResponse("cert-result.html", context=context_data)


@router.get("/verify")
def verify(req: Request,
           store: Store = Depends(check_store),
           session: Session = Depends(db.session),
           user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)
    context_data.update(base_url=get_base_url(req))

    return templates.TemplateResponse("account-verify.html", context=context_data)
