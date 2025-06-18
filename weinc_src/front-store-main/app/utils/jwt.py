from datetime import datetime, timedelta
from typing import Optional, Dict

from fastapi import Depends, Request, Response
from fastapi import HTTPException
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError, ExpiredSignatureError

from app.common.consts import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.errors import exceptions as exc
from app.models.auth import MemberToken, Token
from app.database.schema import Store, MemberStore, Customer


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[Token]:
        access_token: str = request.cookies.get("access_token")  # changed to accept access token from httpOnly Cookie
        refresh_token: str = request.cookies.get("refresh_token")  # changed to accept access token from httpOnly Cookie
        # print("access_token is",access_token)
        # print("refresh_token is",refresh_token)

        scheme, param = get_authorization_scheme_param(access_token)
        refresh_token_scheme, refresh_token_param = get_authorization_scheme_param(refresh_token)
        if not access_token or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return Token(access_token=param, refresh_token=refresh_token_param)


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/token", auto_error=False)


def create_token(data: dict, expires_delta: timedelta):
    """
    JWT 토큰 발행
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return f"Bearer {encoded_jwt}"


def token_user(req: Request, token: Token = Depends(oauth2_scheme)):
    """
    JWT 토큰을 이용 하여 사용자 정보 반환
    :param req:
    :param res:
    :param token:
    :return:
    """
    if not token:
        raise exc.NotAuthorized
    return token_proc(token, req)


def token_user_option(req: Request, res: Response, token: Token = Depends(oauth2_scheme)):
    """
    JWT 토큰을 이용 하여 사용자 정보 반환 (Optional)
    :param req:
    :param res:
    :param token:
    :return:
    """
    if not token:
        return None
    return token_proc(token, req)


def token_proc(token: Token, req: Request):
    try:
        payload = jwt.decode(token.access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        member = get_member(req, payload)
    except ExpiredSignatureError:
        try:
            payload = jwt.decode(token.refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            member = get_member(req, payload)
        except ExpiredSignatureError:
            raise exc.TokenExpiredEx
    except JWTError:
        raise exc.TokenDecodeEx

    return member


def get_member(req: Request, payload):
    member: MemberToken = MemberToken(**payload)
    if member is None:
        raise exc.TokenDecodeEx

    customer = Customer.get(id=member.id, status="Y")
    if customer is None:
        raise exc.NotAuthorized

    store_code = req.path_params.get("store_code")
    if store_code:
        store = Store.get(code=store_code)
        if store.type == "C":  # 폐쇄몰 일 경우
            ms = MemberStore.get(customer_id=member.id, store_code=store_code)
            if ms:
                if ms.confirm == "N":
                    raise exc.NotAuthorized
            else:
                if store.able_target_use in ["Y", "A", "F"]:
                    raise exc.NotAuthorized
                else:
                    raise exc.NotAuthorized
    return member
