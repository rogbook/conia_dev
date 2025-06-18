from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile, Request, Security, Query
from sqlalchemy.orm import Session

from app.utils.jwt import token_user
from app.utils.common_utils import get_ip, extensions_check, get_extensions
from app.utils.aws import S3
from app.utils.log import data_logger
from app.errors import exceptions as exc

from app.database.conn import db
from app.database.schema import NoticeInfo, ExtraInfo, ProductPhoto, ProductOption

from app.models.common import Success
from app.models.product.info import *
from app.models.auth import MemberToken
from app.utils.date_utils import D
from app.common.consts import AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST

router = APIRouter(prefix='/product/{product_id}/info')


@router.post("/notice", response_model=Success, name="상품정보제공고시 등록")
def add_notice_info(indata: List[AddNoticeInfo],
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    for row in indata:
        indata_dict = row.dict()
        NoticeInfo.create(session, auto_commit=False, **indata_dict)
    session.commit()

    return Success()


@router.get("/notice", response_model=List[DataNoticeInfo], name="상품정보제공고시 목록")
def list_notice_info(product_id: int,
                     session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data_list = NoticeInfo.filter(session=session, product_id=product_id).all()

    return data_list


@router.put("/notice", response_model=Success, name="상품정보제공고시 수정")
def mod_notice_info(indata: List[ModNoticeInfo],
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    for row in indata:
        data: NoticeInfo = NoticeInfo.get(session, id=row.notice_id, product_id=row.product_id)
        data.update_optional(session=session, auto_commit=True, **row.dict())

    return Success()


@router.delete("/notice", response_model=Success, name="상품정보제공고시 삭제")
def del_notice_info(product_id: int, info_ids: List[int],
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    for row in info_ids:
        NoticeInfo.filter(session=session, id=row, product_id=product_id).delete()
    session.commit()

    return Success()


@router.post("/extra", response_model=Success, name="추가정보 등록")
def add_extra_info(indata: List[AddExtraInfo],
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    for row in indata:
        indata_dict = row.dict()
        ExtraInfo.create(session, auto_commit=True, **indata_dict)

    return Success()


@router.get("/extra", response_model=List[DataExtraInfo], name="추가정보 목록")
def list_extra_info(product_id: int, session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data_list = ExtraInfo.filter(session=session, product_id=product_id).all()

    return data_list


@router.put("/extra", response_model=Success, name="추가정보 수정")
def mod_extra_info(product_id: int,  indata: List[ModExtraInfo],
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):

    for row in indata:
        data: ExtraInfo = ExtraInfo.get(session=session, id=row.id, product_id=product_id)
        if not data:
            raise exc.NotFoundDataEx
        data.update_optional(session=session, auto_commit=True, **row.dict())

    return Success()


@router.delete("/extra", response_model=Success, name="추가정보 삭제")
def del_extra_info(product_id: int, info_ids: List[int],
                   session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):

    for info_id in info_ids:
        data: ExtraInfo = ExtraInfo.get(session=session, id=info_id, product_id=product_id)
        if not data:
            raise exc.NotFoundDataEx

        mapping_data = {
            "id": info_id,
            "product_id": product_id,
        }
        ExtraInfo.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()


@router.post("/photo", response_model=List[str], name="사진 등록")
def add_product_photo(product_id: int, files: List[UploadFile],
                      req: Request,
                      product_option_id: Optional[int] = Query(default=None),
                      session: Session = Depends(db.session), user: MemberToken = Security(token_user, scopes=['write:product'])):
    result = []
    for file in files:
        if not extensions_check(file.filename):
            raise exc.NotAllowedFileEx

    s3 = S3()
    for file in files:
        file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{get_extensions(file.filename)}"
        s3.upload_file(file, AWS_S3_BUCKET_IMG, 'product/thumb/', file_name)
        url: str = f"{AWS_S3_BUCKET_IMG_HOST}product/thumb/{file_name}"

        log_dict = dict(
            category="product",
            action="add",
            type="desc_photo",
            ip=get_ip(req),
            user=user.id,
            user_name=user.name,
            data=url,
        )
        data_logger(log_dict)

        if product_option_id:
            opt = ProductOption.get(session, product_id=product_id, id=product_option_id)
            if not opt:
                raise exc.NotFoundDataEx
            ProductPhoto.create(session, auto_commit=True, product_id=product_id, uri=url, product_option_id=product_option_id)
        else:
            ProductPhoto.create(session, auto_commit=True, product_id=product_id, uri=url)
        result.append(url)

    return result


@router.get("/photo", response_model=List[DataProductPhoto], name="사진 목록")
def list_product_photo(product_id: int,
                       session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data_list = ProductPhoto.filter(session=session, product_id=product_id).all()

    return data_list


@router.delete("/photo/{photo_id}", response_model=Success, name="사진 삭제")
def del_product_photo(product_id: int, photo_id: int,
                      session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data: ExtraInfo = ProductPhoto.get(session=session, id=photo_id, product_id=product_id)
    if not data:
        raise exc.NotFoundDataEx

    mapping_data = {
        "id": photo_id,
        "product_id": product_id,
    }
    ProductPhoto.filter(session=session, **mapping_data).delete(auto_commit=True)

    return Success()
