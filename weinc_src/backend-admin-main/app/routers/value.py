from typing import List, Optional

from fastapi import APIRouter, Depends, Security, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import SettingValue, OptionValue, NoticeInfoTemplate, FavoriteProductProperty, FavoriteProductPropertyDetail
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, CreatedID
from app.models.value import AddSettingValue, AddOptionValue, DataSettingValue, DataOptionValue, ModSettingValue, ModOptionValue
from app.models.value import AddFavoriteOption, DataFavoriteOption
from app.utils.jwt import token_user

router = APIRouter(prefix='/value')


@router.post("/setting", response_model=CreatedID, name="Setting Value 등록")
def add_setting_value(indata: AddSettingValue,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:setting_value"])):
    indata_dict = indata.dict()

    data: SettingValue = SettingValue.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("/settings", response_model=List[DataSettingValue], name="Setting Value 목록")
def list_setting_value(setting_type: Optional[str] = None,
                       name: Optional[str] = None,
                       session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:setting_value"])):
    qry = session.query(SettingValue)

    if setting_type:
        qry = qry.filter(SettingValue.type == setting_type)

    if name:
        qry = qry.filter(SettingValue.name == name)

    return qry.all()


@router.get("/setting", response_model=DataSettingValue, name="Setting Value")
def setting_value(setting_type: Optional[str] = None,
                  session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["read:setting_value"])):
    qry = session.query(SettingValue).filter(SettingValue.type == setting_type)
    return qry.first()


@router.put("/setting/{value_id}", response_model=Success, name="Setting Value 수정")
def mod_setting_value(value_id: int, indata: ModSettingValue,
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:setting_value"])):
    data: SettingValue = SettingValue.get(session=session, id=value_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.post("/option", response_model=CreatedID, name="Option Value 등록")
def add_option_value(indata: AddOptionValue,
                     session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:option_value"])):
    indata_dict = indata.dict()

    data: OptionValue = OptionValue.create(session, auto_commit=True, **indata_dict)

    return CreatedID(id=data.id)


@router.get("/option", response_model=List[DataOptionValue], name="Option Value 목록")
def list_option_value(option_type: Optional[str] = Query(default=None, description="옵션 타입 [은행 목록(bank_list)]"),
                      session: Session = Depends(db.session)):
    qry = session.query(OptionValue)

    if option_type:
        qry = qry.filter(OptionValue.type == option_type)

    return qry.all()


@router.put("/option/{value_id}", response_model=Success, name="Option Value 수정")
def mod_option_value(value_id: int, indata: ModOptionValue,
                     session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=["write:option_value"])):
    data: OptionValue = OptionValue.get(session=session, id=value_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()


@router.get("/notice-info-template", response_model=List[str], name="상품 정보 제공 고시 템플릿 목록")
def list_notice_info_template(category: Optional[str] = None,
                              session: Session = Depends(db.session)):
    result = []
    if category:
        res = session.query(NoticeInfoTemplate).filter(NoticeInfoTemplate.category == category).order_by(NoticeInfoTemplate.id).all()
        for row in res:
            result.append(row.item)
    else:
        res = session.query(NoticeInfoTemplate).group_by(NoticeInfoTemplate.category).order_by(NoticeInfoTemplate.id).all()
        for row in res:
            # result.append(f"({row.num}) {row.category}")
            result.append(row.category)
    return result


@router.post("/favorite-option", response_model=CreatedID, name="자주쓰는 상품 옵션 등록")
def add_favorite_option(indata: AddFavoriteOption,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=["write:option_value"])):
    fpp = FavoriteProductProperty()
    fpp.name = indata.name
    if indata.type:
        fpp.type = indata.type
    session.add(fpp)
    session.commit()

    for row in indata.propertys:
        detail = FavoriteProductPropertyDetail()
        detail.favorite_product_property_id = fpp.id
        detail.value = row.value
        detail.price = row.price
        detail.code = row.code
        session.add(detail)
    session.commit()

    return CreatedID(id=fpp.id)


@router.get("/favorite-option", response_model=List[DataFavoriteOption], name="자주쓰는 상품 옵션 목록")
def list_favorite_option(session: Session = Depends(db.session),
                         user: MemberToken = Security(token_user, scopes=["read:option_value"])):
    return FavoriteProductProperty.filter(session).all()


@router.delete("/favorite-option/{value_id}", response_model=Success, name="자주쓰는 상품 옵션 삭제")
def del_favorite_option(value_id: int,
                        session: Session = Depends(db.session),
                        user: MemberToken = Security(token_user, scopes=["write:option_value"])):
    FavoriteProductProperty.filter(session, id=value_id).delete(auto_commit=True)
    return Success()
