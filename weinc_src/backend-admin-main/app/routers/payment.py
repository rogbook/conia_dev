import json
from urllib.parse import unquote
from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request, Query
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Order, PgInfo, OrderProduct, Ecoupon
from app.errors import exceptions as exc
from app.models.webhook import DataKtWebhook

from app.utils.date_utils import D

router = APIRouter(prefix='/payment')


@router.post("/kcp-webhook", name="KCP 결제 결과 웹훅")
def kcp_webhook(req: Request,
                site_cd: str = Form(default=None, description="사이트 코드"),
                tno: str = Form(default=None, description="KCP 거래번호"),
                order_no: str = Form(default=None, description="주문번호"),
                tx_cd: str = Form(default=None, description="업무처리 구분 코드"),
                tx_tm: str = Form(default=None, description="업무처리 완료 시간"),
                ipgm_name: str = Form(default=None, description="주문자명"),
                remitter: str = Form(default=None, description="입금자명"),
                ipgm_mnyx: str = Form(default=None, description="입금 금액"),
                bank_code: str = Form(default=None, description="은행코드"),
                account: str = Form(default=None, description="가상계좌 입금계좌번호"),
                op_cd: str = Form(default=None, description="처리구분 코드"),
                noti_id: str = Form(default=None, description="노티 아이디"),
                cash_a_no: str = Form(default=None, description="현금영수증 승인번호"),
                cash_a_dt: str = Form(default=None, description="현금영수증 승인시간"),
                cash_no: str = Form(default=None, description="현금영수증 거래번호"),
                session: Session = Depends(db.session)):
    order = Order.get(session=session, id=order_no)
    if not order:
        raise exc.NotFoundDataEx

    if tx_cd == 'TX00':
        pg_info = session.query(PgInfo).filter(PgInfo.order_id == order.id, PgInfo.tid == tno).first()
        if not pg_info:
            raise exc.NotFoundDataEx

        if int(ipgm_mnyx) != int(pg_info.amount):
            raise exc.BadRequestEx(reason="금액 불일치")

        pg_info.deposit_yn = 'Y'
        pg_info.deposit_date = tx_tm
        pg_info.deposit_name = remitter
        if cash_a_no:
            pg_info.cash_authno = cash_a_no
            pg_info.cash_no = cash_no

        order.status = "PD"

        ops = session.query(OrderProduct).filter(OrderProduct.order_id == order.id).all()
        for op in ops:
            op.status = "PD"

        session.commit()
    else:
        raise exc.BadRequestEx(reason="Not match TX00")

    return "0000"


@router.get("/m12-webhook", name="M12 모바일 상품권 사용 결과 웹훅")
def m12_webhook(req: Request,
                pin_code: str = Query(default=None, description="쿠폰번호"),
                send_status: str = Query(default=None, description="기능구분 Y : 교환 / C : 교환취소"),
                use_price: str = Query(default=None, description="사용금액"),
                balance: str = Query(default=None, description="잔액"),
                ret_date: str = Query(default=None, description="처리일시"),
                ret_msg: str = Query(default=None, description="교환매장명"),
                ret_code: str = Query(default=None, description="교환매장코드"),
                tr_id: str = Query(default=None, description="거래코드"),
                goods_type: str = Query(default=None, description="권종"),
                seq_idx: str = Query(default=None, description="고유값"),
                session: Session = Depends(db.session)):
    ecoupon = Ecoupon.get(session=session, pin_code=pin_code)
    if not ecoupon:
        raise exc.NotFoundDataEx

    if ecoupon.tr_id != tr_id:
        raise exc.NotFoundDataEx

    if ret_msg:
        try:
            ret_msg = unquote(ret_msg, encoding='euc-kr')
        except:
            pass

    raw_data = {
        "pin_code": pin_code,
        "send_status": send_status,
        "use_price": use_price,
        "balance": balance,
        "ret_date": ret_date,
        "ret_msg": ret_msg,
        "ret_code": ret_code,
        "tr_id": tr_id,
        "goods_type": goods_type,
        "seq_idx": seq_idx,
    }

    if send_status == 'Y':
        if ecoupon.status == 'CP' and ecoupon.order_product.balance == 0:
            return "0001"
        ecoupon.status = 'CP'
        ecoupon.order_product.status = 'CP'
        if ret_date:
            if len(ret_date) == 8:
                ecoupon.order_product.complete_date = datetime.strptime(ret_date, "%Y%m%d")
            elif len(ret_date) == 12:
                ecoupon.order_product.complete_date = datetime.strptime(ret_date, "%Y%m%d%H%M")
            elif len(ret_date) == 14:
                ecoupon.order_product.complete_date = datetime.strptime(ret_date, "%Y%m%d%H%M%S")
        ecoupon.raw_data = f"{ecoupon.raw_data}\n{json.dumps(raw_data, ensure_ascii=False)}"

        if goods_type == '04' and balance:
            ecoupon.order_product.balance = balance
    elif send_status == 'C':
        if ecoupon.status == 'Y':
            return "0001"
        ecoupon.status = 'Y'
        ecoupon.order_product.status = 'PD'
        ecoupon.order_product.complete_date = None
        ecoupon.raw_data = f"{ecoupon.raw_data}\n{json.dumps(raw_data, ensure_ascii=False)}"

    session.commit()

    return "0000"


@router.post("/kt-webhook", name="KT 모바일 상품권 사용 결과 웹훅")
def kt_webhook(req: Request,
               mdcode: str = Form(description="기업코드"),
               tr_id: str = Form(description="쿠폰발급 시 요청한 tr_id"),
               trade_type: str = Form(description="01(핀상태변경), 02(유효기간변경)"),
               trade_code: str = Form(description="핀상태 / 02: 교환, 03: 반품, 04: 관리폐기, 07: 구매취소"),
               trade_date: str = Form(description="사용/사용취소 일자 ( yyyymmddhhmmss)"),
               trade_amt: int = Form(default=None, description="사용금액"),
               branch_code: str = Form(default=None, description="사용 지점코드"),
               branch_name: str = Form(default=None, description="사용 지점명"),
               pin_no: str = Form(default=None, description="쿠폰번호"),
               use_start_date: str = Form(default=None, description="유효기간 시작일"),
               use_end_date: str = Form(default=None, description="유효기간 종료일"),
               session: Session = Depends(db.session)):
    ecoupon = Ecoupon.get(session=session, pin_code=pin_no, tr_id=tr_id)
    if not ecoupon:
        raise exc.NotFoundDataEx

    data = DataKtWebhook(mdcode=mdcode, tr_id=tr_id, trade_type=trade_type, trade_code=trade_code, trade_date=trade_date, trade_amt=trade_amt, branch_code=branch_code, branch_name=branch_name, use_start_date=use_start_date, use_end_date=use_end_date)

    ecoupon.raw_data = f"{ecoupon.raw_data}\n{json.dumps(data.dict(), ensure_ascii=False)}"
    session.commit()

    return "0000"
