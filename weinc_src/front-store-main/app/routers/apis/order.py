import uuid
import json

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import OrderSheet, OrderSheetProduct, Cart, ProductOption, StoreProduct, Order, PgInfo, OrderProduct, OrderRe, OrderReProduct, PgCancel, Store, LogOrder, Coupon, Customer, RuralPostcode, PgInfoSub
from app.models.auth import MemberToken
from app.models.common import CreatedID, Exist, Success, LogOrderDataIn
from app.models.order import *
from app.utils.common_utils import check_product_state, log_msg
from app.utils.jwt import token_user
from app.utils.pg_kcp import kcp_cancel, CancelData, ResCancelData
from app.utils.pg_payco import cancel as payco_cancel, ReqCancel, ResCancel
from app.utils.date_utils import D
from app.utils.sms_util import send_sms, make_bottom_msg
from app.utils.ecoupon_m12 import cancel as m12_cancel, ResCancel, ReqInfo, info as m12_info, ResInfo
from app.utils.ecoupon_dnc import cancel as dnc_cancel, ReqCancel as DncReqCancel, ResCancel as DncResCancel
from app.utils.ecoupon_kt import EcounponKt, ReqCancel as KtReqCancel, ResBase as KtResBase
from app.errors import exceptions as exc
from app.common.consts import PG_KCP_CANCEL_ALL
from app.common.config import conf

router = APIRouter(prefix='/order')


@router.post("/sheet", response_model=CreatedID, name="주문서 등록")
def add_order_sheet(indata: AddOrderSheet,
                    session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    order_sheet_id: str = str(uuid.uuid4())

    new_data = OrderSheet()
    new_data.id = order_sheet_id
    new_data.customer_id = member.id
    new_data.store_code = indata.store_code
    if indata.type == "cart":
        new_data.step_type = "cart"
    else:
        new_data.step_type = "direct"

    session.add(new_data)
    session.flush()

    store = Store.get(session, code=indata.store_code)
    original_store = store
    dupl_target = None
    if store.dupl_store:
        dupl_target = Store.get(session, code=store.dupl_store)

    if dupl_target:
        store = dupl_target

    products = {}

    if indata.type == "cart":
        for cart_id in indata.carts:
            cart: Cart = Cart.get(session, id=cart_id)

            prd = products.get(cart.product_option.product.id)

            if cart.product_option.product.inven_use == "Y":
                inven_cnt = cart.product_option.inventory.count
                inven_safe_cnt = cart.product_option.inventory.safe_count
                remain_cnt = inven_cnt - inven_safe_cnt
                if cart.count > remain_cnt:
                    raise exc.BadRequestEx(reason="재고 수량이 부족합니다.")

            if prd:
                prd["count"] = prd["count"] + cart.count
            else:
                product_data = cart.product_option.product
                products[product_data.id] = {
                    "max_cnt": int(product_data.max_purchase_limit) if product_data.max_purchase_limit else 0,
                    "min_cnt": int(product_data.min_purchase_limit) if product_data.min_purchase_limit else 0,
                    "user_max_cnt": int(product_data.user_limit) if product_data.user_limit else 0,
                    "user_limit_reset": product_data.user_limit_reset,
                    "count": cart.count,
                }

        product_list = list(products.items())
        for k, v in product_list:
            if 0 < v["max_cnt"] < v["count"]:
                raise exc.BadRequestEx(reason="최대 구매수량을 초과하였습니다.")
            if v["min_cnt"] > 0 and v["min_cnt"] > v["count"]:
                raise exc.BadRequestEx(reason="최소 구매수량을 확인해주세요.")
            if v["user_max_cnt"] > 0:
                reset_target_date = None
                if v["user_limit_reset"]:
                    user_limit_reset = json.loads(v["user_limit_reset"])
                    if user_limit_reset["type"] == 'month':
                        reset_target_date = D().get_last_day(int(user_limit_reset["value"]))
                    elif user_limit_reset["type"] == 'week':
                        reset_target_date = D().get_last_week(int(user_limit_reset["value"]))

                # 주문 상태는 고려하지 않음
                if reset_target_date:
                    order_cnt = session.query(OrderProduct).join(Order, OrderProduct.order_id == Order.id).filter(OrderProduct.product_id == k, Order.customer_id == member.id, Order.reg_date > reset_target_date).group_by(Order.id).count()
                else:
                    order_cnt = session.query(OrderProduct).join(Order, OrderProduct.order_id == Order.id).filter(OrderProduct.product_id == k, Order.customer_id == member.id).group_by(Order.id).count()
                if order_cnt >= v["user_max_cnt"]:
                    raise exc.BadRequestEx(reason="1인당 구매횟수를 초과하였습니다.")

        for cart_id in indata.carts:
            cart: Cart = Cart.get(session, id=cart_id)

            if not check_product_state(session, cart.product_option.product_id, cart.product_option_id, indata.store_code):
                raise exc.NotFoundDataEx

            variation = StoreProduct.get(session, store_code=store.code, product_id=cart.product_option.product_id).variation
            amount = cart.product_option.selling_price
            if variation != 0:
                amount = cart.product_option.selling_price + variation

            if cart.product_option.product.type == 'DP':
                new_data_product = OrderSheetProduct()
                new_data_product.id = str(uuid.uuid4())
                new_data_product.order_sheet_id = order_sheet_id
                new_data_product.product_option_id = cart.product_option_id
                new_data_product.amount = amount * cart.count
                new_data_product.ea = cart.count

                session.add(new_data_product)
            else:
                for i in range(cart.count):
                    new_data_product = OrderSheetProduct()
                    new_data_product.id = str(uuid.uuid4())
                    new_data_product.order_sheet_id = order_sheet_id
                    new_data_product.product_option_id = cart.product_option_id
                    new_data_product.amount = amount
                    new_data_product.ea = 1

                    session.add(new_data_product)
    else:
        for item in indata.products:
            op: ProductOption = ProductOption.get(session, id=item.product_option_id)

            if op.product.inven_use == "Y":
                inven_cnt = op.inventory.count
                inven_safe_cnt = op.inventory.safe_count
                remain_cnt = inven_cnt - inven_safe_cnt
                if item.count > remain_cnt:
                    raise exc.BadRequestEx(reason="재고 수량이 부족합니다.")

            prd = products.get(op.product.id)
            if prd:
                prd["count"] = prd["count"] + item.count
            else:
                product_data = op.product
                products[product_data.id] = {
                    "max_cnt": int(product_data.max_purchase_limit) if product_data.max_purchase_limit else 0,
                    "min_cnt": int(product_data.min_purchase_limit) if product_data.min_purchase_limit else 0,
                    "user_max_cnt": int(product_data.user_limit) if product_data.user_limit else 0,
                    "user_limit_reset": product_data.user_limit_reset,
                    "count": item.count,
                }
        product_list = list(products.items())
        for k, v in product_list:
            if 0 < v["max_cnt"] < v["count"]:
                raise exc.BadRequestEx(reason="최대 구매수량을 초과하였습니다.")
            if v["min_cnt"] > 0 and v["min_cnt"] > v["count"]:
                raise exc.BadRequestEx(reason="최소 구매수량을 확인해주세요.")
            if v["user_max_cnt"] > 0:
                reset_target_date = None
                if v["user_limit_reset"]:
                    user_limit_reset = json.loads(v["user_limit_reset"])
                    if user_limit_reset["type"] == 'month':
                        reset_target_date = D().get_last_day(int(user_limit_reset["value"]))
                    elif user_limit_reset["type"] == 'week':
                        reset_target_date = D().get_last_week(int(user_limit_reset["value"]))

                # 주문 상태는 고려하지 않음
                if reset_target_date:
                    order_cnt = session.query(OrderProduct).join(Order, OrderProduct.order_id == Order.id).filter(OrderProduct.product_id == k, Order.customer_id == member.id, Order.reg_date > reset_target_date).group_by(Order.id).count()
                else:
                    order_cnt = session.query(OrderProduct).join(Order, OrderProduct.order_id == Order.id).filter(OrderProduct.product_id == k, Order.customer_id == member.id).group_by(Order.id).count()
                if order_cnt >= v["user_max_cnt"]:
                    raise exc.BadRequestEx(reason="1인당 구매횟수를 초과하였습니다.")

        for item in indata.products:
            op: ProductOption = ProductOption.get(session, id=item.product_option_id)

            if not check_product_state(session, op.product_id, op.id, indata.store_code):
                raise exc.NotFoundDataEx

            variation = StoreProduct.get(session, store_code=store.code, product_id=op.product_id).variation
            amount = op.selling_price
            if variation != 0:
                amount = op.selling_price + variation

            if op.product.type == 'DP':
                new_data_product = OrderSheetProduct()
                new_data_product.id = str(uuid.uuid4())
                new_data_product.order_sheet_id = order_sheet_id
                new_data_product.product_option_id = item.product_option_id
                new_data_product.amount = amount * item.count
                new_data_product.ea = item.count

                session.add(new_data_product)
            else:
                for i in range(item.count):
                    new_data_product = OrderSheetProduct()
                    new_data_product.id = str(uuid.uuid4())
                    new_data_product.order_sheet_id = order_sheet_id
                    new_data_product.product_option_id = item.product_option_id
                    new_data_product.amount = amount
                    new_data_product.ea = 1

                    session.add(new_data_product)

    session.commit()

    return CreatedID(id=order_sheet_id)


@router.put("/sheet/{sheet_id}", response_model=Success, name="주문서 쿠폰 적용")
def sheet_coupon(sheet_id: str,
                 indata: OrderSheetCoupon,
                 session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    sheet = OrderSheet.get(session, customer_id=member.id, id=sheet_id)
    if not sheet:
        raise exc.NotFoundDataEx

    sp = OrderSheetProduct.get(session, order_sheet_id=sheet_id, id=indata.sheet_product_id)
    if not sp:
        raise exc.NotFoundDataEx

    if indata.coupon_id:
        already: List[OrderSheetProduct] = session.query(OrderSheetProduct).filter(OrderSheetProduct.coupon_id == indata.coupon_id).all()
        for row in already:
            row.coupon_id = None
        session.commit()

        coupon = Coupon.get(session, customer_id=member.id, id=indata.coupon_id, use_yn='N')
        if not coupon:
            raise exc.NotFoundDataEx
        if coupon.target == 'one':
            if coupon.product_id != sp.product_option.product_id:
                raise exc.NotFoundDataEx
        sp.coupon_id = coupon.id
    else:
        sp.coupon_id = None

    session.commit()

    return Success()


@router.post("/request_re", response_model=Success, name="교환,반품 신청")
def request_re(indata: ReqOrderRe,
               session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    order: Order = Order.get(session, customer_id=member.id, id=indata.order_id)

    if not order:
        raise exc.NotFoundDataEx

    opl: List[OrderProduct] = OrderProduct.filter(session, order_id=indata.order_id).all()
    sel_opl: List[OrderProduct] = []

    prd_opt_id_list = indata.order_products.split(",")

    for sel_prd_id in prd_opt_id_list:
        for op in opl:
            if op.id == int(sel_prd_id):
                sel_opl.append(op)

    if len(sel_opl) == 0:
        raise exc.ViewNotFoundEx

    pg_info = PgInfo.get(session, order_id=indata.order_id)

    re = OrderRe()
    re.order_id = indata.order_id
    re.type = indata.request_type
    re.contents = indata.request_reason
    re.status = "R"
    re.pay_type = pg_info.kind
    re.log = "신청"
    session.add(re)
    session.commit()

    for row in sel_opl:
        orp = OrderReProduct()
        orp.order_re_id = re.id
        orp.order_product_id = row.id
        session.add(orp)

        if indata.request_type == "return":
            row.update(session, True, status="RFR")
        elif indata.request_type == "exchange":
            row.update(session, True, status="EXR")
    session.commit()

    return Success()


@router.get("/sheet/{sheet_id}", response_model=Exist, name="주문서 여부")
def check_sheet(sheet_id: str,
                session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data = OrderSheet.get(session, customer_id=member.id, id=sheet_id)

    return Exist(exist=True if data else False)


@router.get("/rural/{post_code}", response_model=Exist, name="도서산간 여부")
def rural_check(post_code: int,
                session: Session = Depends(db.session), member: MemberToken = Depends(token_user)):
    data = RuralPostcode.get(session, post_code=post_code)

    return Exist(exist=True if data else False)


@router.post("/cancel/{order_id}", response_model=Success, name="주문 취소")
def cancel(order_id: str,
           req: Request,
           session: Session = Depends(db.session),
           member: MemberToken = Depends(token_user)):
    order: Order = Order.get(session, customer_id=member.id, id=order_id)

    if not order:
        raise exc.NotFoundDataEx

    if order.status == 'PD':
        cancel_disable = None
        pg_info = session.query(PgInfo).filter(PgInfo.order_id == order_id).first()
        if pg_info:
            if order.pg_info and order.pg_info.app_time[:8] != D().yyyymmdd() and order.pg_info.pg_info_sub:
                sub_list: List[PgInfoSub] = order.pg_info.pg_info_sub
                for sub in sub_list:
                    if sub.kind == '식권 쿠폰':
                        cancel_disable = '식권 쿠폰 사용 결제 입니다.'
                        break
        if cancel_disable:
            raise exc.BadRequestEx(reason='취소 불가(식권쿠폰 사용결제)')

        ops: List[OrderProduct] = session.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()
        for op in ops:
            if op.ecoupon and op.ecoupon.provider == 'M12':
                m12_req = ReqInfo(tr_id=op.ecoupon.tr_id, goods_id=op.ecoupon.goods_id, pin_no=op.ecoupon.pin_code)
                m12_res: ResInfo = m12_info(m12_req)
                if m12_res.PIN_STATUS != 'R':
                    raise exc.BadRequestEx(reason='E쿠폰 사용시 취소 불가')

        pg_info = PgInfo.get(session, order_id=order_id)

        if pg_info.amount > 0:

            cancel_time = ""
            cancel_tno = ""

            c = conf()

            if pg_info.provider == "KCP":
                data = CancelData(site_cd=c.PG_KCP_SITE_CODE,
                                  kcp_cert_info=c.PG_KCP_CERT_INFO,
                                  mod_type=PG_KCP_CANCEL_ALL,
                                  tno=pg_info.tid)

                res: ResCancelData = kcp_cancel(data)
                cancel_time = res.canc_time
                cancel_tno = res.tno
            elif pg_info.provider == "PAYCO":
                data = ReqCancel(orderNo=pg_info.tid,
                                 cancelTotalAmt=str(int(order.final_amount)),
                                 orderCertifyKey=pg_info.cancel_key)
                res: ResCancel = payco_cancel(data)
                cancel_time = res.cancelYmdt
                cancel_tno = res.cancelTradeSeq

            order.update(session, True, status="CD")
            OrderProduct.filter(session, order_id=order_id).update_q(True, status='CD')
            ops: List[OrderProduct] = session.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()
            for op in ops:
                if op.ecoupon:
                    if op.ecoupon.provider == 'M12':
                        m12_req = ReqInfo(tr_id=op.ecoupon.tr_id, goods_id=op.ecoupon.goods_id, pin_no=op.ecoupon.pin_code)
                        m12_res: ResCancel = m12_cancel(m12_req)
                        if m12_res.STATUS_CODE == '0000':
                            op.ecoupon.status = 'D'
                        else:
                            op.ecoupon.status = 'DE'
                    elif op.ecoupon.provider == 'DNC':
                        dnc_req = DncReqCancel(tradeId=op.ecoupon.tr_id, pinCode=op.ecoupon.pin_code, orderCode=op.ecoupon.order_code, requestedAt=D().now_str())
                        try:
                            res: DncResCancel = dnc_cancel(dnc_req)
                            if res.pinCode:
                                op.ecoupon.status = 'D'
                            else:
                                op.ecoupon.status = 'DE'
                        except:
                            op.ecoupon.status = 'DE'
                    elif op.ecoupon.provider == 'KT':
                        kt_req = KtReqCancel(tradeId=op.ecoupon.tr_id, pinCode=op.ecoupon.pin_code)
                        try:
                            ec_kt = EcounponKt()
                            res: KtResBase = ec_kt.cancel(kt_req)
                            if res.resCode == '0000':
                                op.ecoupon.status = 'D'
                            else:
                                op.ecoupon.status = 'DE'
                        except:
                            op.ecoupon.status = 'DE'


            pg_info.update(session, True, cancel_type='all', cancel_date=datetime.strptime(cancel_time, "%Y%m%d%H%M%S"), cancel_mny=pg_info.amount, remain_amount=0)
            cancel_data = PgCancel()
            cancel_data.pg_info_order_id = order_id
            cancel_data.tno = cancel_tno
            cancel_data.type = "ALL"
            cancel_data.reg_date = datetime.strptime(cancel_time, "%Y%m%d%H%M%S")
            cancel_data.amount = pg_info.amount
            session.add(cancel_data)
            session.commit()

            customer = Customer.get(session, id=member.id)
            store = Store.get(session, code=order.store_code)
            msg = f"""안녕하세요 [{customer.name}]님!
[{store.title}]입니다. 요청하신 주문 취소가 처리되었습니다.

■취소 금액 : {int(pg_info.amount):,}원
최종 환불까지는 결제했던 방법에 따라 영업일 기준 2~3일 정도 소요됩니다. 
카드 별 처리가 상이한 점 참고해주세요.

오늘도 기분 좋은 하루 보내세요!
{make_bottom_msg(req, store)}
"""
            send_sms(session, customer, store, msg, order_id)

            # 로깅
            log_data = LogOrderDataIn(action="주문 전체취소", order_id=order_id, msg=log_msg("msg", f"주문 전체취소"), writer=f"주문자 본인")
            LogOrder.create(session, auto_commit=True, **log_data.dict())
        else:
            order.update(session, True, status="CD")
            OrderProduct.filter(session, order_id=order_id).update_q(True, status='CD')

    elif order.status == "PW":
        order.update(session, True, status="CD")
        OrderProduct.filter(session, order_id=order_id).update_q(True, status='CD')
    else:
        raise exc.BadRequestEx(reason="주문 취소가 불가능한 상태입니다.")

    return Success()


@router.post("/complete/{order_product_id}", response_model=Success, name="구매 확정")
def complete(order_product_id: str,
             session: Session = Depends(db.session),
             member: MemberToken = Depends(token_user)):
    op: OrderProduct = OrderProduct.get(session, id=order_product_id)
    order: Order = Order.get(session, customer_id=member.id, id=op.order_id)

    if not op:
        raise exc.NotFoundDataEx

    if not order:
        raise exc.NotFoundDataEx

    op.status = "CP"
    op.complete_date = func.current_timestamp()
    session.commit()

    # 로깅
    log_data = LogOrderDataIn(action="구매확정", order_id=order.id, msg=log_msg("msg", f"구매확정"), writer=f"주문자 본인")
    LogOrder.create(session, auto_commit=True, **log_data.dict())

    ops = session.query(OrderProduct).filter(OrderProduct.order_id == order.id, OrderProduct.status != "CP").all()
    if len(ops) == 0:
        order.update(session, auto_commit=True, status="CP")
    else:
        ...

    return Success()


@router.post("/confirm/{order_id}", response_model=Success, name="직원 확인")
def confirm(order_id: str,
            indata: Confirm,
            session: Session = Depends(db.session),
            member: MemberToken = Depends(token_user)):
    order: Order = session.query(Order).filter(Order.id == order_id, Order.customer_id == member.id, Order.status.in_(["PD", "PU"])).first()

    if not order:
        raise exc.NotFoundDataEx

    prd_list: List[OrderProduct] = order.products

    confirm_pass = prd_list[0].member.confirm_pass

    if confirm_pass != indata.code:
        raise exc.BadRequestEx

    for row in prd_list:
        if row.status == 'PD':
            if row.use_end_date and row.use_end_date < D().now:
                raise exc.BadRequestEx(reason="사용 기간이 지난 상품 입니다.")

            row.status = "CP"
            row.use_date = D().now
            row.complete_date = func.current_timestamp()
    order.status = "CP"

    session.commit()

    return Success()


@router.post("/confirm_row/{order_prd_id}", response_model=Success, name="직원 확인 개별")
def confirm_row(order_prd_id: str,
                indata: Confirm,
                session: Session = Depends(db.session),
                member: MemberToken = Depends(token_user)):
    order_prd: OrderProduct = (session.query(OrderProduct)
                               .join(Order, Order.id == OrderProduct.order_id)
                               .filter(OrderProduct.id == order_prd_id, OrderProduct.status == "PD", Order.customer_id == member.id).first())

    if not order_prd:
        raise exc.NotFoundDataEx

    confirm_pass = order_prd.member.confirm_pass

    if confirm_pass != indata.code:
        raise exc.BadRequestEx(reason="인증 코드가 올바르지 않습니다.")

    if order_prd.use_end_date and order_prd.use_end_date < D().now:
        raise exc.BadRequestEx(reason="사용 기간이 지난 상품 입니다.")

    order_prd.status = "CP"
    order_prd.use_date = D().now
    order_prd.complete_date = func.current_timestamp()
    session.commit()

    order: Order = Order.get(session, id=order_prd.order_id)
    prd_list: List[OrderProduct] = order.products
    part_used = False
    for prd in prd_list:
        if prd.status != "CP":
            part_used = True

    if part_used:
        order.status = "PU"
    else:
        order.status = "CP"

    session.commit()

    return Success()
