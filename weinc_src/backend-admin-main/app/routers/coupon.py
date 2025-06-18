from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends, Security, UploadFile, Request
from fastapi.params import Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from telegram.error import BadRequest

from app.database.conn import db
from app.database.schema import CouponGroup, Coupon, Customer, MemberStore, CouponTarget, CouponPublishTarget
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success, CreatedID, CreatedURI, SuccessCount
from app.models.coupon import *
from app.utils.jwt import token_user
from app.common.consts import AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST
from app.utils.aws import S3
from app.utils.common_utils import get_ip, generate_random_string, extensions
from app.utils.date_utils import D
from app.utils.log import data_logger

router = APIRouter(prefix='/coupon')


@router.post("", response_model=CreatedID, name="쿠폰 그룹 등록")
def add_coupon_group(indata: AddCouponGroup,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:coupon'])):
    indata_dict = indata.dict()

    data: CouponGroup = CouponGroup.create(session, auto_commit=True, **indata_dict)

    if indata.coupon_target:
        for target in indata.coupon_target:
            target_data = {
                "coupon_group_id": data.id
            }
            if target.member_id:
                target_data.update(member_id=target.member_id)
            elif target.product_id:
                target_data.update(product_id=target.product_id)
            else:
                continue
            CouponTarget.create(session, auto_commit=True, **target_data)

    return CreatedID(id=data.id)


@router.get("", response_model=ListCouponGroup, name="쿠폰 그룹 목록")
def list_coupon_group(name: Optional[str] = Query(default=None, description="이름"),
                      auto: Optional[str] = Query(default=None, description="자동 발급 쿠폰 여부"),
                      auto_type: Optional[str] = Query(default=None, description="자동 발급 쿠폰 구분"),
                      offset: int = 0, limit: int = 20,
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=['read:coupon'])):
    qry = session.query(CouponGroup).filter(CouponGroup.status != 'D')

    if name:
        qry = qry.filter(CouponGroup.name.like(f'%{name}%'))

    if auto and auto == 'Y':
        qry = qry.filter(CouponGroup.auto != None)
    else:
        qry = qry.filter(CouponGroup.auto == None)

    if auto_type:
        qry = qry.filter(CouponGroup.auto.like(f'%{auto_type}%'))

    total = qry.count()
    qry = qry.order_by(CouponGroup.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListCouponGroup(total=total, datas=data_list)


@router.get("/{group_id}", response_model=DataCouponGroup, name="쿠폰 그룹 상세")
def get_coupon_group(group_id: int,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['read:coupon'])):
    data: CouponGroup = CouponGroup.get(session=session, id=group_id)
    if not data:
        raise exc.NotFoundDataEx

    group_data: DataCouponGroup = DataCouponGroup.from_orm(data)
    group_data.publish_cnt = Coupon.filter(session, coupon_group_id=group_id).count()

    return group_data


@router.put("/{group_id}", response_model=Success, name="쿠폰 그룹 상태 변경")
def mod_coupon_group(group_id: int,
                     status: str,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:coupon'])):
    data: CouponGroup = CouponGroup.get(session=session, id=group_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session, True, status=status)

    return Success()


@router.delete("/{group_id}", response_model=Success, name="쿠폰 그룹 삭제")
def del_coupon_group(group_id: int,
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=['write:coupon'])):
    data: CouponGroup = CouponGroup.get(session=session, id=group_id)
    if not data:
        raise exc.NotFoundDataEx

    coupon_cnt = Coupon.filter(session, coupon_group_id=group_id).count()
    if coupon_cnt > 0:
        raise exc.BadRequestEx

    data.update_optional(session, True, status='D')

    return Success()


@router.post("/photo", response_model=CreatedURI, name="쿠폰 이미지 등록")
def add_photo(file: UploadFile, req: Request,
              ext: str = Depends(extensions),
              user: MemberToken = Security(token_user, scopes=['write:coupon'])):
    s3 = S3()

    file_name = f"{D.yyyymmdd()}-{uuid4().hex[:16]}.{ext}"
    s3.upload_file(file, AWS_S3_BUCKET_IMG, 'coupon/', file_name)
    url: str = f"{AWS_S3_BUCKET_IMG_HOST}coupon/{file_name}"

    log_dict = dict(
        category="coupon",
        action="add file",
        type="coupon_image",
        ip=get_ip(req),
        user=user.id,
        user_name=user.name,
        data=url,
    )
    data_logger(log_dict)

    return CreatedURI(uri=url)


@router.post("/{group_id}", response_model=SuccessCount, name="쿠폰 발행")
def publish_coupon(group_id: int, indata: CouponPublish,
                   session: Session = Depends(db.session),
                   user: MemberToken = Security(token_user, scopes=['write:coupon'])):
    data: CouponGroup = CouponGroup.get(session=session, id=group_id, status='Y')
    if not data:
        raise exc.NotFoundDataEx

    success_cnt = 0
    target = []

    if indata.type == 'all':
        qry = session.query(Customer.id).join(Coupon, and_(Coupon.customer_id == Customer.id, Coupon.coupon_group_id == group_id), isouter=True)
        qry = qry.filter(Coupon.customer_id.is_(None))
        target = qry.distinct().all()
    elif indata.type == 'store':
        qry = session.query(Customer.id).join(MemberStore, MemberStore.customer_id == Customer.id).join(Coupon, and_(Coupon.customer_id == Customer.id, Coupon.coupon_group_id == group_id), isouter=True)
        qry = qry.filter(MemberStore.store_code == indata.store_code)
        qry = qry.filter(Coupon.customer_id.is_(None))
        target = qry.distinct().all()
    elif indata.type == 'customer':
        qry = session.query(Customer.id).join(Coupon, and_(Coupon.customer_id == Customer.id, Coupon.coupon_group_id == group_id), isouter=True)
        qry = qry.filter(Coupon.customer_id.is_(None))
        qry = qry.filter(Customer.id.in_(indata.customer_ids))
        target = qry.distinct().all()

    if data.publish_limit:
        published_coupon_cnt = Coupon.filter(session, coupon_group_id=group_id).count()
        if len(target) > (data.publish_limit - published_coupon_cnt):
            raise exc.BadRequestEx('발행 가능 수를 초과하였습니다.')

    try:
        for row in target:
            publishing_coupon(session, data, row.id)
            success_cnt += 1
        session.commit()
    except Exception as e:
        session.rollback()
        raise exc.SqlFailureEx

    return SuccessCount(count=success_cnt)


@router.get("/{group_id}/published", response_model=ListCoupon, name="발급 쿠폰 목록")
def list_coupon(group_id: int,
                code: Optional[str] = Query(default=None, description="코드"),
                use_yn: Optional[str] = Query(default=None, description="사용 여부"),
                s_reg_date: Optional[date] = Query(default=None, description="발급일 시작"),
                e_reg_date: Optional[date] = Query(default=None, description="발급일 종료"),
                s_use_date: Optional[date] = Query(default=None, description="사용일 시작"),
                e_use_date: Optional[date] = Query(default=None, description="사용일 종료"),
                offset: int = 0, limit: int = 20,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=['read:coupon'])):
    data: CouponGroup = CouponGroup.get(session=session, id=group_id)
    if not data:
        raise exc.NotFoundDataEx

    qry = session.query(Coupon).filter(Coupon.coupon_group_id == group_id)

    if code:
        qry = qry.filter(Coupon.code == code)

    if use_yn:
        qry = qry.filter(Coupon.use_yn == use_yn)

    if s_reg_date and e_reg_date:
        qry = qry.filter(Coupon.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(Coupon.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(Coupon.reg_date < D().make235959(e_reg_date))

    if s_use_date and e_use_date:
        qry = qry.filter(Coupon.use_date.between(s_use_date, D().make235959(e_use_date)))
    elif s_use_date:
        qry = qry.filter(Coupon.use_date > s_use_date)
    elif e_use_date:
        qry = qry.filter(Coupon.use_date < D().make235959(e_use_date))

    total = qry.count()
    qry = qry.order_by(Coupon.reg_date.desc())
    data_list = qry.offset(offset).limit(limit).all()

    return ListCoupon(total=total, datas=data_list)


def publishing_coupon(session: Session, group: CouponGroup, customer_id: int):
    data = Coupon()
    data.code = generate_random_string(10)
    data.name = group.name
    data.description = group.description

    if group.expire_days:
        dutil = D()
        data.begin_date = dutil.now_str()
        data.end_date = dutil.generate235959(dutil.add_day(group.expire_days))
    elif group.begin_time and group.end_time:
        now = datetime.now()
        data.begin_date = now.replace(hour=group.begin_time.hour, minute=group.begin_time.minute, second=group.begin_time.second)
        data.end_date = now.replace(hour=group.end_time.hour, minute=group.end_time.minute, second=group.end_time.second)
    else:
        data.begin_date = group.begin_date
        data.end_date = group.end_date

    data.amount = group.amount
    data.percent = group.percent

    data.min_price = group.min_price
    data.max_price = group.max_price

    data.issuer = group.issuer
    data.coupon_group_id = group.id
    data.target = group.target
    data.type = group.type
    data.customer_id = customer_id
    data.product_id = group.product_id

    session.add(data)
