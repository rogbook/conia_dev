from fastapi import APIRouter, Depends, Security, Request
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import OrderProduct
from app.errors import exceptions as exc
from app.models.common import Success
from app.models.auth import MemberToken
from app.utils.ecoupon_m12 import info, ReqInfo, ResInfo
from app.utils.ecoupon_kt import EcounponKt, ReqResend as KtReqResend, ResBase as KtResBase
from app.utils.jwt import token_user

router = APIRouter(prefix='/ecoupon')


@router.get("/info/{order_product_id}", response_model=ResInfo, name="E쿠폰 상태")
def info(req: Request,
         order_product_id: int,
         session: Session = Depends(db.session),
         user: MemberToken = Security(token_user, scopes=[])):
    """
    E쿠폰 상태
    """
    prd = OrderProduct.get(session=session, id=order_product_id)

    if prd is None or prd.ecoupon is None:
        raise exc.NotFoundDataEx

    req_data = ReqInfo(tr_id=prd.ecoupon.tr_id, goods_id=prd.ecoupon.goods_id, pin_no=prd.ecoupon.pin_code)
    res: ResInfo = info(req_data)

    return res


@router.get("/resend/{order_product_id}", name="E쿠폰 재발송")
def resend(req: Request,
           order_product_id: int,
           session: Session = Depends(db.session),
           user: MemberToken = Security(token_user, scopes=[])):
    """
    E쿠폰 상태
    """
    prd = OrderProduct.get(session=session, id=order_product_id)

    if prd is None or prd.ecoupon is None:
        raise exc.NotFoundDataEx

    if prd.ecoupon.provider == 'KT':
        ec_kt = EcounponKt()

        req_data = KtReqResend(tradeId=prd.ecoupon.tr_id, pinCode=prd.ecoupon.pin_code)
        res: KtResBase = ec_kt.resend(req_data)

        if res.resCode == '0000':
            return Success()
        else:
            raise exc.ProcessFailEx(msg=res.resMsg)
    else:
        raise exc.BadRequestEx(reason='지원하지 않는 공급사')
