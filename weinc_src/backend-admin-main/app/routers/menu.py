from typing import Union, List, Optional
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import Menu, MenuClass

from app.models.common import Success
from app.models.menu import DataMenuClass, DataMenu
from app.models.auth import MemberToken


router = APIRouter(prefix="/menu")


@router.get('', response_model=List[DataMenu], name="메뉴 목록")
def get_menu(session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["read:menu"])):
    data = Menu.filter(session=session).all()
    return data


@router.get("/{code}", response_model=List[DataMenuClass], name="타입별 메뉴 목록")
def get_type_menu(code: str,
                  session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["read:menu"])):
    data = MenuClass.filter(session=session, class_code=code).all()
    return data


@router.post("/{class_code}/link", response_model=Success, name="메뉴 연결")
def class_link(class_code: str, target: int,
               session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["link:menu"])):
    data = Menu.get(session=session, id=target)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
        "class_code": class_code,
        "menu_id": target
    }
    MenuClass.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/{class_code}/link", response_model=Success, name="메뉴 연결 해제")
def class_unlink(class_code: str, menu_id: int,
                 session: Session = Depends(db.session), member: MemberToken = Security(token_user, scopes=["link:menu"])):
    data = Menu.get(session=session, id=menu_id)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
       "class_code": class_code,
       "menu_id": menu_id
    }
    MenuClass.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()
