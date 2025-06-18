from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import CommonInfo

from app.models.common import Success
from app.models.product.info import *
from app.models.auth import MemberToken


router = APIRouter(prefix='/product/common-info')


@router.post("", response_model=Success, name="공통정보 등록")
def add_common_info(indata: AddCommonInfo,
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    indata_dict = indata.dict()
    CommonInfo.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("", response_model=List[DataCommonInfo], name="공통정보 목록")
def list_common_info(member_id: Optional[int] = Query(default=None, description="회원번호"),
                     session: Session = Depends(db.session),
                     member: MemberToken = Depends(token_user)):
    if member_id:
        data_list = session.query(CommonInfo).filter(CommonInfo.member_id == member_id).all()
    else:
        data_list = session.query(CommonInfo).all()

    return data_list


@router.get("/template", response_model=List[DataCommonInfo], name="공통정보 템플릿 목록")
def list_common_info_template(member_id: int = Query(description="회원번호"),
                              session: Session = Depends(db.session),
                              member: MemberToken = Depends(token_user)):
    data_list = (session.query(CommonInfo)
                 .filter(or_(CommonInfo.member_id.is_(None), CommonInfo.member_id == member_id)).all())

    return data_list


@router.get("/{info_id}", response_model=DataCommonInfo, name="공통정보")
def get_common_info(info_id: int,
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data = CommonInfo.get(session, id=info_id)

    return data


@router.put("/{info_id}", response_model=Success, name="공통정보 수정")
def mod_common_info(info_id: int, indata: ModCommonInfo,
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: CommonInfo = CommonInfo.get(session=session, id=info_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, **indata.dict())

    return Success()
