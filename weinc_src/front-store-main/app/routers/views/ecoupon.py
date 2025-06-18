from typing import List

from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Store, OrderProduct, Order, NoticeInfo, CommonInfo, Ecoupon
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.utils.common_utils import check_store, make_view_context_data, get_target_store_code
from app.utils.jwt import token_user
from app.utils.templates import templates
from app.utils.ecoupon_m12 import info, ReqInfo, ResInfo
from app.utils.ecoupon_dnc import info as dnc_info, ReqInfo as DncReqInfo, ResInfo as DncResInfo
from app.utils.ecoupon_kt import EcounponKt, ReqInfo as KtReqInfo, ResInfo as KtResInfo
from app.utils.date_utils import D

router = APIRouter(prefix="/ecoupon")


@router.get("")
def list_ecoupon(store_code: str, req: Request,
                 q: str = Query(default=None),
                 page: int = Query(default=1, gt=0),
                 page_size: int = Query(default=50),
                 session: Session = Depends(db.session),
                 store: Store = Depends(check_store),
                 user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(OrderProduct).join(Order, Order.id == OrderProduct.order_id).outerjoin(Ecoupon, OrderProduct.id == Ecoupon.order_product_id)
    qry = qry.filter(Order.store_code == store_code,
                     Order.customer_id == user.id,
                     OrderProduct.status != "D", OrderProduct.status != "CD",
                     OrderProduct.type == "UP-EC")
    qry = qry.order_by(Order.reg_date.desc())

    # if q:
    #     qry = qry.filter(Shop.name.like(f'%{q}%'))
    #
    # total = qry.count()
    # qry = qry.offset(page_size * (page - 1)).limit(page_size)
    datas: List[OrderProduct] = qry.all()
    target_list = []

    for prd in datas:
        if prd.ecoupon:
            if prd.ecoupon.status != 'D' and prd.ecoupon.status != 'DE':
                check_status(session, prd)
                target_list.append(prd)
        else:
            target_list.append(prd)

    # paginate = Page(datas, page, page_size, total)
    # context_data.update(page_title="매장 목록")
    context_data.update(datas=datas)
    # context_data.update(paginate=paginate)
    del context_data['layout_data']

    return templates.TemplateResponse("account-ecoupons.html", context=context_data)


@router.get("/{order_product_id}")
def view_ecoupon(store_code: str,
                 order_product_id: int,
                 req: Request,
                 session: Session = Depends(db.session),
                 store: Store = Depends(check_store),
                 user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    qry = session.query(OrderProduct).join(Order, Order.id == OrderProduct.order_id).outerjoin(Ecoupon, OrderProduct.id == Ecoupon.order_product_id)
    qry = qry.filter(Order.store_code == store_code,
                     Order.customer_id == user.id,
                     Order.status != "D", Order.status != "CD",
                     OrderProduct.type == "UP-EC",
                     OrderProduct.id == order_product_id)

    prd = qry.first()

    if not prd:
        raise exc.ViewNotFoundEx

    if prd.ecoupon:
        if prd.ecoupon.status != 'D' and prd.ecoupon.status != 'DE':
            check_status(session, prd)
        else:
            raise exc.ViewNotFoundEx

    notice_info = NoticeInfo.filter(session, product_id=prd.product_id).order_by("sort").all()
    common_info = CommonInfo.get(session, id=prd.product.common_info_id)

    context_data.update(prd=prd)
    context_data.update(notice_info=notice_info)
    context_data.update(common_info=common_info)

    return templates.TemplateResponse("account-ecoupon-detail.html", context=context_data)


def check_status(session: Session, prd: OrderProduct):
    if prd.product.api_provider == 'M12' and (prd.status == "PD" or prd.balance > 0):
        req = ReqInfo(tr_id=prd.ecoupon.tr_id, goods_id=prd.ecoupon.goods_id, pin_no=prd.ecoupon.pin_code)
        res: ResInfo = info(req)

        if res.PIN_STATUS != 'R':
            if res.PIN_STATUS == 'F':
                prd.status = 'CP'
                prd.complete_date = D().str_convert(res.USE_DATE)
                if res.GOODS_TYPE == '04' and res.ACCOUNT_BALANCE:
                    prd.balance = res.ACCOUNT_BALANCE
            elif res.PIN_STATUS == 'C':
                prd.status = 'CD'
            elif res.PIN_STATUS == 'V':
                prd.status = 'EXP'
            session.commit()
    elif prd.product.api_provider == 'DNC' and (prd.status == "PD" or prd.balance > 0):
        req = DncReqInfo(pinCode=prd.ecoupon.pin_code, orderCode=prd.ecoupon.order_code)
        try:
            res: DncResInfo = dnc_info(req)

            print(res)
        except Exception as e:
            if isinstance(e, exc.APIException):
                print(e.detail)
            else:
                print(e.args)
            pass
    elif prd.product.api_provider == 'KT' and (prd.status == "PD" or prd.balance > 0):
        req = KtReqInfo(pinCode=prd.ecoupon.pin_code, tradeId=prd.ecoupon.tr_id)
        try:
            ec_kt = EcounponKt()
            res: KtResInfo = ec_kt.info(req)

            coupon_data = res.couponInfoList[0]
            pin_status = coupon_data.pinStatusCd
            if pin_status != '01':
                if pin_status == '02':
                    prd.status = 'CP'
                    prd.complete_date = D().str_convert(coupon_data.correcDtm)
                    if coupon_data.remainAmt and int(coupon_data.remainAmt) > 0:
                        prd.balance = int(coupon_data.remainAmt)
                elif pin_status == '07' or pin_status == '03':
                    prd.status = 'CD'
                elif pin_status == '04':
                    prd.status = 'EXP'
        except Exception as e:
            if isinstance(e, exc.APIException):
                print(e.detail)
            else:
                print(e.args)
            pass
