from typing import Union
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from sqlalchemy.orm import Session

from app.common.consts import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Member

from app.models.auth import MemberToken
from app.utils.date_utils import D

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
oauth2_refresh_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    JWT Access 토큰 발행
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(member: Member, session: Session, expires_delta: Union[timedelta, None] = None):
    """
    JWT Refresh 토큰 발행
    :param member:
    :param expires_delta:
    :param session:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    encoded_jwt = jwt.encode({"id": member.id, "exp": expire}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    member.update(session, True, refresh_token=encoded_jwt)

    return encoded_jwt


def token_user(req: Request, security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """
    JWT 토큰을 이용 하여 사용자 정보 반환
    :param security_scopes:
    :param token:
    :return:
    """
    if not token:
        raise exc.NotAuthorized
    return token_proc(token, security_scopes)


def token_user_option(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """
    JWT 토큰을 이용 하여 사용자 정보 반환 (Optional)
    :param security_scopes:
    :param token:
    :return:
    """
    if not token:
        return None
    return token_proc(token, security_scopes)



def token_user_refresh(session: Session = Depends(db.session),
                       token: HTTPAuthorizationCredentials = Depends(oauth2_refresh_scheme)):
    """
    JWT 리프레쉬 토큰을 이용 하여 사용자 정보 반환
    :param session:
    :param token:
    :return:
    """
    if not token or not token.credentials:
        raise exc.NotAuthorized
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        member_id: int = payload.get("id")
        if member_id is None:
            raise exc.TokenDecodeEx
    except ExpiredSignatureError:
        raise exc.TokenExpiredEx
    except JWTError:
        raise exc.TokenDecodeEx

    user = Member.get(session, id=member_id)
    if user is None:
        raise exc.NotFoundUserEx()
    if user.refresh_token != token.credentials:
        raise exc.TokenDecodeEx()
    if user.status != "Y":
        raise exc.NotFoundUserEx()
    user.lastlogin_date = D().now
    return user


def token_proc(token, security_scopes):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        member: MemberToken = MemberToken(**payload)
        if member is None:
            raise exc.TokenDecodeEx
        if security_scopes.scopes:
            check_scope = False
            for scope in security_scopes.scopes:
                if member.admin == 'Y':
                    member.scopes[scope] = ["*"]
                if scope in member.scopes.keys():
                    check_scope = True
                    break
            if not check_scope:
                raise exc.PermissionEx
    except ExpiredSignatureError:
        raise exc.TokenExpiredEx
    except JWTError:
        raise exc.TokenDecodeEx

    return member
