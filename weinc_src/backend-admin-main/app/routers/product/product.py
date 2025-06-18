from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, UploadFile, Request, Security, Query
from sqlalchemy.orm import Session

from app.common.consts import AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST
from app.database.conn import db
from app.database.schema import Product, ProductGroup, ProductStoreMemo, ProductBadge, Badge, LogProduct, ProductOption, ProductCategory, ProductBrand
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import *
from app.models.product.product import *
from app.utils.aws import S3
from app.utils.common_utils import get_ip, log_msg, extensions
from app.utils.date_utils import D
from app.utils.jwt import token_user
from app.utils.log import data_logger
from app.utils.telegram import telegram_send
from app.common.config import conf

router = APIRouter(prefix='/product')


@router.post("", response_model=CreatedID, name="상품 등록")
async def add_product(indata: AddProduct,
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=['write:product'])):
    indata_dict = indata.dict()
    indata_dict.update(writer_id=user.id)
    if not indata.code:
        indata_dict.update(code=f"CP{D.yyyymmdd()[2:]}{uuid4().hex[:8]}")
    data = Product.create(session, auto_commit=True, **indata_dict)

    # 로깅
    log_data = LogProductDataIn(action="등록", product_id=data.id, msg=log_msg("msg", "상품 등록"), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    c = conf()
    await telegram_send(f"[{c.ENV}] 신규 상품이 등록 되었습니다.\n상품명 : {indata.name}\n상품코드 : {data.code}\n등록자 : {user.name}")

    return CreatedID(id=data.id)


@router.get("", response_model=ListDataProduct, name="상품 목록")
def list_product(name: Optional[str] = Query(default=None, description="상품명"),
                 code: Optional[str] = Query(default=None, description="상품 코드"),
                 member_id: Optional[int] = Query(default=None, description="PA id"),
                 status: Optional[str] = Query(default=None, description="상품상태"),
                 prd_type: Optional[str] = Query(default=None, description="상품유형"),
                 view_yn: Optional[str] = Query(default=None, description="노출여부"),
                 prod_only: Optional[str] = Query(default='N', description="상품만 검색(그룹상품제외)"),
                 category: Optional[int] = Query(default=None, description="카테고리"),
                 brand: Optional[int] = Query(default=None, description="브랜드"),
                 pg_provider: Optional[str] = Query(default=None,description="결제수단제한"),
                 s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                 e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                 offset: int = 0, limit: int = 20,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=['read:product'])):
    if category:
        qry = session.query(Product).outerjoin(ProductCategory, ProductCategory.product_id == Product.id).filter(ProductCategory.category_id == category)
    elif brand:
        qry = session.query(Product).outerjoin(ProductBrand, ProductBrand.product_id == Product.id).filter(ProductBrand.brand_id == brand)
    else:
        qry = session.query(Product)

    qry = qry.filter(Product.status != 'D')

    if name:
        qry = qry.filter(Product.name.like(f'%{name}%'))

    if code:
        qry = qry.filter(Product.code.like(f'%{code}%'))

    if prd_type:
        qry = qry.filter(Product.type.like(f'{prd_type}%'))

    if member_id:
        qry = qry.filter(Product.member_id == member_id)

    if prod_only == 'Y':
        qry = qry.filter(Product.type != 'G')

    if status:
        qry = qry.filter(Product.status == status)

    if view_yn:
        qry = qry.filter(Product.view_yn == view_yn)

    if pg_provider:
        qry = qry.filter(Product.pg_provider == pg_provider)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Product.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Product.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Product.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(Product.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListDataProduct(total=total, datas=data_list)


@router.get("/exist", response_model=Exist, name="상품 코드 중복 확인")
def exist_code(code: str,
               session: Session = Depends(db.session)):
    data = Product.get(session, code=code)
    if data:
        return Exist(exist=True)
    return Exist(exist=False)


@router.post("/photo", response_model=CreatedURI, name="상품 상세 설명용 사진 등록")
def add_product_description_photo(file: UploadFile, req: Request,
                                  ext: str = Depends(extensions),
                                  user: MemberToken = Security(token_user, scopes=['write:product'])):
    s3 = S3()

    file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{ext}"
    s3.upload_file(file, AWS_S3_BUCKET_IMG, 'product/desc/', file_name)
    url: str = f"{AWS_S3_BUCKET_IMG_HOST}product/desc/{file_name}"

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

    return CreatedURI(uri=url)


@router.put("/update_status", response_model=SuccessFail, name="상품 상태 일괄 수정")
def update_status(indata: ModProductStatus,
                  session: Session = Depends(db.session),
                  user: MemberToken = Security(token_user, scopes=["write:product"])):
    target_ids = list(set(indata.product_ids))
    success_cnt = 0
    fail_list = []

    for product_id in target_ids:
        prd: Product = Product.get(session=session, id=product_id)
        if not prd:
            fail_list.append([product_id, '상품 데이터 없음'])
            continue

        if indata.status == "Y":
            if ProductOption.filter(session, product_id=product_id, status="Y").count() == 0:
                fail_list.append([product_id, '상품 옵션정보 없음'])
                continue
            if not prd.photos:
                fail_list.append([product_id, '상품 사진정보 없음'])
                continue
            if not prd.contents:
                fail_list.append([product_id, '상품 상세정보 없음'])
                continue
            if prd.type == "DP":
                if not prd.shipping_info_id:
                    fail_list.append([product_id, '상품 배송정보 없음'])
                    continue
            if prd.type == "UP-EC":
                if not prd.use_end_date and not prd.use_end_period:
                    fail_list.append([product_id, '상품(E쿠폰) 사용기한 정보 없음'])
                    continue

        status = indata.status
        if prd.status != status:
            before_status = prd.status
            prd.status = status
            session.commit()

            # 로깅
            log_data = LogProductDataIn(action="상품상태 일괄수정", product_id=prd.id, msg=log_msg("msg", f"{before_status} -> {status}"), writer=f"{user.name}:{user.id}")
            LogProduct.create(session, auto_commit=True, **log_data.dict())
            success_cnt += 1
        else:
            fail_list.append([product_id, '변경사항 없음'])

    return SuccessFail(success_count=success_cnt, fail_list=fail_list)



@router.get("/{product_id}", response_model=DataProduct, name="상품 정보")
def get_product(product_id: int,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=['read:product'])):
    data = Product.get(session=session, id=product_id)
    if not data:
        raise exc.NotFoundDataEx

    return data


@router.put("/{product_id}", response_model=Success, name="상품 수정")
async def mod_product(product_id: int, indata: ModProduct,
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=['write:product'])):
    data: Product = Product.get(session=session, id=product_id)
    if not data:
        raise exc.NotFoundDataEx

    if indata.status == "Y" or indata.view_yn == "Y":
        if ProductOption.filter(session, product_id=product_id, status="Y").count() == 0:
            raise exc.BadRequestEx(reason="상품 옵션정보 없음")
        if not data.photos:
            raise exc.BadRequestEx(reason="상품 사진정보 없음")
        if not data.contents:
            raise exc.BadRequestEx(reason="상품 상세정보 없음")
        if data.type == "DP":
            if not data.shipping_info_id:
                raise exc.BadRequestEx(reason="상품 배송정보 없음")
        if data.type == "UP-EC":
            if not data.use_end_date and not data.use_end_period:
                raise exc.BadRequestEx(reason="상품(E쿠폰) 사용기한 정보 없음")

    change_data = data.update_optional(session=session, auto_commit=True, **indata.dict())

    # 로깅
    log_data = LogProductDataIn(action="수정", product_id=product_id, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    c = conf()
    await telegram_send(f"[{c.ENV}] 상품 정보가 변경 되었습니다.\n상품명 : {data.name}\n상품코드 : {data.code}\n등록자 : {user.name}")

    return Success()


@router.get("/{product_id}/log", response_model=ListLog, name="상품 Log")
def product_log(product_id: int,
                offset: int = 0, limit: int = 20,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=['write:product'])):
    qry = session.query(LogProduct).filter(LogProduct.product_id == product_id, LogProduct._del != "Y")

    total = qry.count()
    qry = qry.order_by(LogProduct.reg_date.desc())
    datas = qry.offset(offset).limit(limit).all()

    return ListLog(total=total, datas=datas)


@router.post("/{product_id}/store_memo", response_model=Success, name="상품 상점 메모 등록")
def add_product_store_memo(product_id: int, indata: AddProductStoreMemo,
                           session: Session = Depends(db.session),
                           user: MemberToken = Depends(token_user)):
    indata_dict = indata.dict()
    indata_dict.update(member_id=user.id)
    data = ProductStoreMemo.create(session, auto_commit=True, **indata_dict)

    # 로깅
    log_data = LogProductDataIn(action="메모 등록", product_id=product_id, msg=log_msg("msg", "메모 등록"), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    return CreatedID(id=data.id)


@router.post("/{product_id}/store_memo/{memo_id}", response_model=Success, name="상품 상점 메모 수정")
def mod_product_store_memo(product_id: int, store_code: str, memo_id: int, indata: ModProductStoreMemo,
                           session: Session = Depends(db.session),
                           user: MemberToken = Depends(token_user)):
    data: ProductStoreMemo = ProductStoreMemo.get(session=session, id=memo_id, product_id=product_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    indata_dict = indata.dict()
    indata_dict.update(member_id=user.id)
    change_data = data.update_optional(session=session, auto_commit=True, **indata_dict)

    # 로깅
    log_data = LogProductDataIn(action="메모 수정", product_id=product_id, msg=log_msg("list", change_data), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.delete("/{product_id}/store_memo/{memo_id}", response_model=Success, name="상품 상점 메모 삭제")
def del_product_review_photo(product_id: int, store_code: str, memo_id: int,
                             session: Session = Depends(db.session),
                             user: MemberToken = Depends(token_user)):
    data: ProductStoreMemo = ProductStoreMemo.get(session=session, id=memo_id, product_id=product_id, store_code=store_code)
    if not data:
        raise exc.NotFoundDataEx

    target_id = data.id

    session.delete(data)
    session.commit()

    # 로깅
    log_data = LogProductDataIn(action="메모 삭제", product_id=product_id, msg=log_msg("msg", f"메모 삭제: {target_id}"), writer=f"{user.name}:{user.id}")
    LogProduct.create(session, auto_commit=True, **log_data.dict())

    return Success()


@router.get("/{product_id}/badge", response_model=List[DataSimpleBadge], name="상품 배지 목록")
def get_product_badge_list(product_id: int,
                           session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    qry = session.query(Badge).join(ProductBadge, Badge.id == ProductBadge.badge_id)
    data_list = qry.filter(ProductBadge.product_id == product_id).all()

    return data_list


@router.post("/{product_id}/group-link", response_model=Success, name="그룹 상품 연결")
def group_link(child_id: List[int], product_id: int,
               session: Session = Depends(db.session),
               user: MemberToken = Security(token_user, scopes=["write:product"])):
    for c_id in child_id:
        data = ProductGroup.get(session=session, pid=product_id, product_id=c_id)
        if data:
            continue

        mapping_data = {
            "product_id": c_id,
            "pid": product_id,
        }
        ProductGroup.create(session=session, auto_commit=True, **mapping_data)

    return Success()


@router.delete("/{product_id}/group-link", response_model=Success, name="그룹 상품 연결 해제")
def group_unlink(child_id: List[int], product_id: int,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=["write:product"])):
    for c_id in child_id:
        ProductGroup.filter(session=session, pid=product_id, product_id=c_id).delete(auto_commit=True)

    return Success()


@router.get("/{product_id}/group", response_model=ListDataSimpleProduct, name="그룹 상품 목록")
def get_group_product_list(product_id: int,
                           session: Session = Depends(db.session),
                           s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                           e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                           offset: int = 0, limit: int = 20,
                           user: MemberToken = Security(token_user, scopes=["read:product"])):
    qry = session.query(Product).join(ProductGroup, Product.id == ProductGroup.product_id)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Product.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Product.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Product.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    qry = qry.order_by(Product.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListDataSimpleProduct(total=total, datas=data_list)
