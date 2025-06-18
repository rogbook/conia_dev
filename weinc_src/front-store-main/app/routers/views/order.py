import json
from typing import List
from math import floor
import requests
from operator import itemgetter
from datetime import datetime

from fastapi import APIRouter, Request, Depends, Form, status, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.common.config import conf
from app.common.consts import CONIA_SMS_SENDER, PG_KCP_CANCEL_ALL
from app.database.conn import db
from app.database.schema import PgInfo, ShippingInfo, ShippingCost, StoreProduct, ProductReview, Inventory, Coupon, OrderCoupon, SettingValue, Product, PgInfoSub, PgCancel, CouponTarget
from app.database.schema import Store, Order, OrderSheet, Customer, DeliveryAddress, OrderSheetProduct, Cart, WishProduct, ProductOption, OrderProduct, OrderShipping, RuralPostcode, Ecoupon
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.customer import DataCustomer, DataDeliveryAddress
from app.models.product import DataOptions, DataProduct
from app.models.coupon import DataCoupon
from app.utils.common_utils import check_store, order_numbering, make_view_context_data, get_ip, check_product_state, get_target_store_code, get_base_url, wish_and_product_check
from app.utils.jwt import token_user
from app.utils.paging import Page
from app.utils.pg_kcp import payment, ResData, ReqData, kcp_cancel, CancelData, ResCancelData
from app.utils.pg_payco import reserve, ReqReserve, ResReserve, payment as payco_payment, ReqPayment, ResPayment, PaymentDetails, cancel as payco_cancel, ReqCancel, ResCancel
from app.utils.templates import templates
from app.utils.log import analytics
from app.utils.date_utils import D
from app.utils.sms_util import send_sms, make_bottom_msg
from app.utils.ecoupon_m12 import issue, ReqIssue, ResIssue, ReqInfo, cancel as m12_cancel, ResCancel as m12ResCancel
from app.utils.ecoupon_dnc import issue as dnc_issue, ReqIssue as DncReqIssue, ResIssue as DncResIssue, cancel as dnc_cancel, ReqCancel as DncReqCancel, ResCancel as DncResCancel
from app.utils.ecoupon_kt import EcounponKt, ReqIssue as KtReqIssue, ResIssue as KtResIssue, ReqCancel as KtReqCancel, ResBase as KtResBase

router = APIRouter(prefix="/order")


@router.get("/cart")
def cart(req: Request, store_code: str,
         store: Store = Depends(check_store),
         session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    cart_list: List[Cart] = Cart.filter(session=session, customer_id=user.id, store_code=store_code, type="D").all()
    cart_u_list: List[Cart] = Cart.filter(session=session, customer_id=user.id, store_code=store_code, type="U").all()

    shipping = {}

    for cart_item in cart_list:
        product = cart_item.product_option.product
        prd = prd_cart_item(session, cart_item, target_store_code)

        if product.shipping_info.calc_type == "개별":
            ship_key = f"{product.shipping_info.id}_{product.id}"
        else:
            ship_key = product.shipping_info.id

        shipping_data = shipping.get(ship_key)

        if shipping_data:
            shipping_data["products"].append(prd)
        else:
            cost_list: List[ShippingCost] = cart_item.product_option.product.shipping_info.costs
            cost_list_res = []
            for row in cost_list:
                cost_list_res.append({
                    "type": row.type,
                    "category": row.category,
                    "cost": row.cost,
                    "section_start": row.section_start,
                    "section_end": row.section_end,
                    "section_repeat": row.section_repeat,
                })

            shipping[ship_key] = dict(info=cart_item.product_option.product.shipping_info,
                                      shipping_title=cart_item.product_option.product.shipping_info.member.company.name,
                                      cost=json.dumps(cost_list_res),
                                      products=[prd])

    for row in shipping.values():
        shipping_products = row.get("products")

        product_group = {}
        for prd in shipping_products:
            prd_grp_row = product_group.get(prd["product"].id)
            if prd_grp_row:
                prd_grp_row["options"].append(prd)
            else:
                product_group[prd["product"].id] = dict(product=prd["product"], options=[prd])

        prd_grp_list = list(product_group.values())
        row["prd_grp"] = prd_grp_list

    context_data.update(shipping=shipping.values())
    context_data.update(d_count=len(cart_list))
    context_data.update(u_count=len(cart_u_list))

    return templates.TemplateResponse("shop-cart.html", context=context_data)


@router.get("/cart-u")
def cart_u(req: Request, store_code: str,
           store: Store = Depends(check_store),
           session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    target_store_code = get_target_store_code(context_data)

    cart_list: List[Cart] = Cart.filter(session=session, customer_id=user.id, store_code=store_code, type="D").all()
    cart_u_list: List[Cart] = Cart.filter(session=session, customer_id=user.id, store_code=store_code, type="U").all()
    prd_grp_list = []
    u_title = ""

    product_group = {}
    for cart_item in cart_u_list:
        prd = prd_cart_item(session, cart_item, target_store_code)

        prd_grp_row = product_group.get(prd["product"].id)
        if prd_grp_row:
            prd_grp_row["options"].append(prd)
        else:
            product_group[prd["product"].id] = dict(product=prd["product"], options=[prd])

        prd_grp_list = list(product_group.values())

        product = cart_item.product_option.product
        u_title = product.member.company.name

    context_data.update(d_count=len(cart_list))
    context_data.update(u_list=prd_grp_list)
    context_data.update(u_title=u_title)
    context_data.update(u_count=len(cart_u_list))

    return templates.TemplateResponse("shop-cart-u.html", context=context_data)


@router.get("/history")
def history(req: Request, store_code: str,
            store: Store = Depends(check_store),
            prd_type: str = Query(default=None),
            page: int = Query(default=1, gt=0),
            page_size: int = Query(default=10),
            session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    # qry = session.query(Order).filter(Order.store_code == store_code, Order.member_id == user.id, Order.status != "D").order_by(Order.reg_date.desc())
    qry = session.query(OrderProduct).join(Order, Order.id == OrderProduct.order_id) \
        .filter(Order.store_code == store_code, Order.customer_id == user.id, Order.status != "D").order_by(Order.reg_date.desc())

    if prd_type:
        qry = qry.filter(OrderProduct.type == prd_type)

    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    # orders = qry.all()
    order_products = qry.all()

    paginate = Page(order_products, page, page_size, total)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(paginate=paginate)
    # context_data.update(orders=orders)
    context_data.update(order_products=order_products)

    sweet_tracker_api_key = SettingValue.get(session, type="sweet_tracker_api_key")
    context_data.update(sweet_tracker_api_key=sweet_tracker_api_key.value)

    context_data.update(legacy_data=None)
    customer = Customer.get(session, id=user.id)
    if customer.legacy_id and customer.legacy_shop == store.code:
        context_data.update(legacy_data={
            "id": customer.legacy_id,
            "pw": customer.legacy_pw,
        })

    return templates.TemplateResponse("account-orders.html", context=context_data)


@router.get("/ticket")
def ticket(req: Request, store_code: str,
           store: Store = Depends(check_store),
           page: int = Query(default=1, gt=0),
           page_size: int = Query(default=10),
           session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    qry = session.query(OrderProduct).join(Order, Order.id == OrderProduct.order_id) \
        .filter(Order.store_code == store_code, Order.customer_id == user.id, Order.status != "D", Order.status != "CD", OrderProduct.type.like("UP-OF"), OrderProduct.status == "PD").order_by(Order.reg_date.desc())

    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    order_products = qry.all()

    paginate = Page(order_products, page, page_size, total)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(paginate=paginate)
    context_data.update(order_products=order_products)

    context_data.update(legacy_data=None)
    customer = Customer.get(session, id=user.id)
    if customer.legacy_id and customer.legacy_shop == store.code:
        context_data.update(legacy_data={
            "id": customer.legacy_id,
            "pw": customer.legacy_pw,
        })

    return templates.TemplateResponse("account-tickets.html", context=context_data)


@router.get("/ticket-used")
def ticket_used(req: Request, store_code: str,
                store: Store = Depends(check_store),
                page: int = Query(default=1, gt=0),
                page_size: int = Query(default=10),
                session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    qry = session.query(OrderProduct).join(Order, Order.id == OrderProduct.order_id) \
        .filter(Order.store_code == store_code, Order.customer_id == user.id, Order.status != "D", Order.status != "CD", OrderProduct.type.like("UP-OF"), OrderProduct.status != "PD").order_by(Order.reg_date.desc())

    total = qry.count()
    qry = qry.offset(page_size * (page - 1)).limit(page_size)
    order_products = qry.all()

    paginate = Page(order_products, page, page_size, total)

    for prd in order_products:
        review = ProductReview.filter(session, order_product_id=prd.id, product_id=prd.product_id, customer_id=user.id, status="Y").first()
        if review:
            prd.review_id = review.id

    context_data = make_view_context_data(session, req, store, user)

    context_data.update(paginate=paginate)
    context_data.update(order_products=order_products)
    context_data.update(legacy_data=None)
    customer = Customer.get(session, id=user.id)
    if customer.legacy_id and customer.legacy_shop == store.code:
        context_data.update(legacy_data={
            "id": customer.legacy_id,
            "pw": customer.legacy_pw,
        })

    return templates.TemplateResponse("account-tickets-used.html", context=context_data)


@router.get("/wishlist")
def wishlist(req: Request, store_code: str,
             store: Store = Depends(check_store),
             session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)
    target_store_code = get_target_store_code(context_data)

    qry = session.query(Product, StoreProduct) \
        .join(StoreProduct, StoreProduct.product_id == Product.id) \
        .join(ProductOption, ProductOption.product_id == Product.id) \
        .join(WishProduct, WishProduct.product_id == Product.id) \
        .filter(StoreProduct.store_code == target_store_code
                , WishProduct.customer_id == user.id
                , WishProduct.store_code == store.code
                , Product.status != 'N'
                , Product.view_yn == 'Y'
                , StoreProduct.view_yn == 'Y'
                , ProductOption.status == 'Y'
                , ProductOption.default_yn == 'Y') \
        .group_by(Product.id)

    datas = qry.all()

    w, products = wish_and_product_check(session, datas, None, store_code)
    # wish_products: List[WishProduct] = WishProduct.filter(session, customer_id=user.id, store_code=store.code).all()
    #
    # for row in wish_products:
    #     row.product.def_option = session.query(ProductOption).filter(ProductOption.product_id == row.product_id, ProductOption.default_yn == 'Y').first()

    context_data.update(wish_products=products)

    return templates.TemplateResponse("account-wishlist.html", context=context_data)


@router.post("/request")
def request(req: Request,
            store: Store = Depends(check_store),
            ordr_idxx: str = Form(),
            good_mny: str = Form(),
            site_cd: str = Form(default=None),
            enc_info: str = Form(default=None),
            enc_data: str = Form(default=None),
            ret_pay_method: str = Form(default=None),
            tran_cd: str = Form(default=None),
            use_pay_method: str = Form(default=None),
            sheet_id: str = Form(),
            address_id: str = Form(default=None),
            memo: str = Form(default=None),
            client_type: str = Form(default=None),
            user_name: str = Form(default=None),
            user_phone: str = Form(default=None),
            user_email: str = Form(default=None),
            active_coupon: str = Form(default=None),
            payType: str = Form(default=None),
            reserveOrderNo: str = Form(default=None),
            paymentCertifyToken: str = Form(default=None),
            mainPgCode: str = Form(default=None),
            comm_tax_mny: int = Form(default=0),
            comm_vat_mny: int = Form(default=0),
            comm_free_mny: int = Form(default=0),
            session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    amount = good_mny.replace(",", "")

    customer = Customer.get(session, id=user.id)
    member = DataCustomer.from_orm(customer)
    address_data = None
    rural_area = False
    if address_id and address_id != "None":
        address_data = DataDeliveryAddress.from_orm(DeliveryAddress.get(session, id=address_id))
        rural_data = RuralPostcode.get(session, post_code=address_data.zipcode)
        if rural_data:
            rural_area = True

    sheet_data: OrderSheet = OrderSheet.get(session, id=sheet_id)
    if not sheet_data:
        raise exc.BadRequestEx(reason="만료된 주문서 입니다.")
    sheet_products: List[OrderSheetProduct] = sheet_data.products

    total_cnt = len(sheet_products)
    total_ea = 0
    origin_amount = 0
    prd_amount = 0
    shipping = {}
    product_grp = {}
    product_count_data = {}
    option_grp = {}

    # 주문 상품 분류
    prd_titles = []
    for sp in sheet_products:
        if not check_product_state(session, sp.product_option.product_id, sp.product_option_id, store.code):
            raise exc.BadRequestEx(reason='주문할 수 없는 상품 입니다.')

        if sp.product_option.product.inven_use == 'Y':
            option_grp_data = option_grp.get(sp.product_option_id)
            if option_grp_data:
                option_grp_data["count"] = option_grp_data["count"] + sp.ea
            else:
                option_grp[sp.product_option_id] = {
                    'count': sp.ea,
                    'inven_count': sp.product_option.inventory.count,
                    'inven_safe_count': sp.product_option.inventory.safe_count,
                }

        total_ea += sp.ea
        prd_amount += sp.amount
        origin_amount += sp.product_option.origin_price
        prd_titles.append(sp.product_option.product.name)

        prd_count = product_count_data.get(sp.product_option.product.id)
        if prd_count:
            prd_count["count"] = prd_count["count"] + sp.ea
        else:
            product_data = sp.product_option.product
            product_count_data[product_data.id] = {
                "max_cnt": int(product_data.max_purchase_limit) if product_data.max_purchase_limit else 0,
                "min_cnt": int(product_data.min_purchase_limit) if product_data.min_purchase_limit else 0,
                "user_max_cnt": int(product_data.user_limit) if product_data.user_limit else 0,
                "user_limit_reset": product_data.user_limit_reset,
                "count": sp.ea,
            }

        prd = dict(
            id=sp.id,
            product=sp.product_option.product,
            option=sp.product_option,
            amount=sp.amount,
            count=sp.ea,
            weight=sp.ea * sp.product_option.weight if sp.product_option.weight else 0,
        )

        option = dict(
            id=sp.id,
            option=sp.product_option,
            amount=sp.amount,
            count=sp.ea,
            weight=sp.ea * sp.product_option.weight if sp.product_option.weight else 0,
        )

        prd_grp_row = product_grp.get(sp.product_option.product_id)
        if prd_grp_row:
            prd_grp_row["options"].append(option)
            prd_grp_row["amount"] = prd_grp_row["amount"] + option.get('amount')
        else:
            product_grp[sp.product_option.product_id] = dict(product=sp.product_option.product, options=[option], amount=option.get('amount'))

        if sp.product_option.product.type == "DP":
            if sp.product_option.product.shipping_info.calc_type == "개별":
                ship_key = f"{sp.product_option.product.shipping_info.id}_{sp.product_option.product.id}"
            else:
                ship_key = sp.product_option.product.shipping_info.id

            shipping_data = shipping.get(ship_key)
            if shipping_data:
                shipping_data["products"].append(prd)
            else:
                shipping[ship_key] = dict(info=sp.product_option.product.shipping_info,
                                          shipping_title=sp.product_option.product.shipping_info.member.company.name,
                                          cost=0,
                                          products=[prd])

    # 구매 수량 검증
    product_count_list = list(product_count_data.items())
    for k, v in product_count_list:
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

    # 재고 검증
    option_grp_list = list(option_grp.items())
    for k, v in option_grp_list:
        remain_cnt = v["inven_count"] - v["inven_safe_count"]
        if v["count"] > remain_cnt:
            raise exc.BadRequestEx(reason="재고 수량이 부족합니다.")

    # 쿠폰 검증
    coupons = None
    if active_coupon and active_coupon != 'None':
        coupons = json.loads(active_coupon)
        if coupons:
            for coupon in coupons:
                coupon_data = Coupon.get(session, id=coupon['id'], use_yn='N')
                if not coupon_data:
                    raise exc.BadRequestEx

    # 가격 검증
    total_shipping_amount = get_shipping_amount(shipping, rural_area)
    total_product_amount, total_discount = get_option_amount(sheet_products, coupons)

    total_amount = total_product_amount + total_shipping_amount
    if int(total_amount) != int(good_mny):
        raise exc.BadRequestEx

    payco_res = None
    kcp_res = None
    if total_amount > 0:
        # 결제 승인 처리
        if payType and payType == 'payco':
            pg_provider = 'PAYCO'
            req_data = ReqPayment(
                reserveOrderNo=reserveOrderNo,
                sellerOrderReferenceKey=ordr_idxx,
                paymentCertifyToken=paymentCertifyToken,
                totalPaymentAmt=good_mny,
                totalTaxfreeAmt=comm_free_mny,
                totalTaxableAmt=comm_tax_mny,
                totalVatAmt=comm_vat_mny,
            )
            payco_res: ResPayment = payco_payment(req_data)
            pg_tno = payco_res.orderNo
            pg_time = payco_res.paymentCompleteYmdt
        else:
            c = conf()
            pg_provider = 'KCP'
            req_data = ReqData(site_cd=site_cd,
                               tran_cd=tran_cd,
                               enc_data=enc_data,
                               enc_info=enc_info,
                               cert_info=c.PG_KCP_CERT_INFO,
                               ordr_mony=amount)
            kcp_res: ResData = payment(req_data)
            pg_tno = kcp_res.tno
            pg_time = kcp_res.app_time
    else:
        pg_provider = 'CONIA'
        pg_tno = '0'
        pg_time = D().now_str_trim()

    pay_kind = convert_pay_kind(ret_pay_method, use_pay_method, mainPgCode)

    # 주문 데이터 생성
    order_data = Order()
    order_data.id = ordr_idxx
    order_data.customer_id = user.id
    order_data.store_code = store.code

    order_data.origin_amount = origin_amount
    order_data.raw_amount = prd_amount
    order_data.final_amount = amount
    order_data.tex_free_amount = comm_free_mny
    # order_data.tax_rate =
    order_data.discount = total_discount
    order_data.coupon_discount = total_discount
    if pay_kind == "vbank":
        order_data.status = "PW"
    else:
        order_data.status = "PD"

    order_data.user_name = member.name
    order_data.user_phone = member.phone
    order_data.user_mobile = member.mobile
    order_data.user_email = member.email

    order_data.recipient_name = address_data.name if address_data else ''
    order_data.recipient_phone = address_data.phone if address_data else ''
    order_data.recipient_mobile = address_data.mobile if address_data else ''
    order_data.zipcode = address_data.zipcode if address_data else ''
    order_data.address = address_data.address if address_data else ''
    order_data.address_detail = address_data.address_detail if address_data else ''
    order_data.shipping_msg = memo if memo and memo != 'None' else ''

    order_data.shipping_cost = total_shipping_amount
    order_data.shipping_cost_post = 0
    order_data.shipping_condition = ""

    order_data.step_type = sheet_data.step_type
    order_data.client_type = client_type
    order_data.referer = ""
    order_data.referer_url = ""
    order_data.total_ea = total_ea
    order_data.total_kind = total_cnt
    # order_data.ipcc_code = ""
    order_data.ip = get_ip(req)

    session.add(order_data)
    session.commit()

    # 결제 데이터 생성
    pg_info = PgInfo()
    pg_info.order_id = ordr_idxx
    pg_info.kind = pay_kind
    pg_info.amount = amount
    pg_info.remain_amount = amount

    pg_info.app_time = pg_time
    pg_info.tid = pg_tno
    pg_info.provider = pg_provider

    if payco_res:
        pg_info.cancel_key = payco_res.orderCertifyKey
        pg_info.raw_data = payco_res.json()
    elif kcp_res:
        pg_info.raw_data = kcp_res.json()

    if pay_kind == 'card':
        if kcp_res:
            pg_info.card_name = kcp_res.card_name
            pg_info.card_no = kcp_res.card_no
            pg_info.card_app_num = kcp_res.app_no
            pg_info.card_quota = kcp_res.quota
            pg_info.card_partcanc_yn = kcp_res.partcanc_yn
            pg_info.card_bin_type_01 = kcp_res.card_bin_type_01
            pg_info.card_bin_type_02 = kcp_res.card_bin_type_02
        elif payco_res:
            for payment_data in payco_res.paymentDetails:
                if payment_data.cardSettleInfo is not None:
                    pg_info.card_name = payment_data.cardSettleInfo.cardCompanyName
                    pg_info.card_no = payment_data.cardSettleInfo.cardNo
                    pg_info.card_app_num = payment_data.cardSettleInfo.cardAdmissionNo
                    pg_info.card_quota = payment_data.cardSettleInfo.cardInstallmentMonthNumber
                    pg_info.card_partcanc_yn = payment_data.cardSettleInfo.partCancelPossibleYn
                    pg_info.card_bin_type_01 = payment_data.cardSettleInfo.corporateCardYn
                    pg_info.card_bin_type_02 = ''
                    break
    elif pay_kind == 'bank':
        if kcp_res:
            pg_info.bankname = kcp_res.bankname
            if kcp_res.cash_authno:
                pg_info.cash_authno = kcp_res.cash_authno
        elif payco_res:
            for payment_data in payco_res.paymentDetails:
                if payment_data.realtimeAccountTrasferSettleInfo is not None:
                    pg_info.bankname = payment_data.realtimeAccountTrasferSettleInfo.bankName
                    break
    elif pay_kind == 'vbank':
        if kcp_res:
            pg_info.bankname = kcp_res.bankname
            pg_info.virtual_account = kcp_res.account
            pg_info.virtual_date = kcp_res.va_date
            if kcp_res.cash_authno:
                pg_info.cash_authno = kcp_res.cash_authno
        elif payco_res:
            for payment_data in payco_res.paymentDetails:
                if payment_data.nonBankbookSettleInfo is not None:
                    pg_info.bankname = payment_data.nonBankbookSettleInfo.bankName
                    pg_info.virtual_account = payment_data.nonBankbookSettleInfo.accountNo
                    pg_info.virtual_date = payment_data.nonBankbookSettleInfo.paymentExpirationYmd

    session.add(pg_info)
    session.commit()

    meal_coupon_use = False
    if payco_res:
        # 페이코 결제 방법 저장
        meal_coupon_use = save_pg_info_sub(session, payco_res.paymentDetails, pg_info.id)

    if shipping:
        for row in shipping.values():
            os = save_order_shipping(session, row, ordr_idxx)
            save_order_product(session, row, ordr_idxx, os, store, user, req, coupons, pay_kind)
            session.commit()
    else:
        for product in sheet_products:
            op = OrderProduct()
            if pay_kind == "vbank":
                op.status = "PW"
            else:
                op.status = "PD"

            target_prd = product.product_option.product

            op.order_id = ordr_idxx
            op.product_option_id = product.product_option_id
            op.product_code = target_prd.code
            op.product_id = target_prd.id
            op.ea = product.ea
            op.product_name = target_prd.name
            op.product_thumbnail = target_prd.photos[0].uri
            op.amount = product.amount
            op.origin_price = product.product_option.origin_price * product.ea
            op.seller_title = target_prd.member.company.name if target_prd.member.company else target_prd.member.name

            # 식권 결제 사용 시간 제한 기능
            force_use_end = None
            if meal_coupon_use and store.meal_opt_use == 'Y' and store.meal_opt_limit_use == 'Y' and store.meal_opt_limit_time != '[]':
                limit_time_table = json.loads(store.meal_opt_limit_time)
                now = datetime.now().time()
                time_range = get_current_time_range(now, limit_time_table)
                if time_range:
                    force_use_end = datetime.combine(datetime.now(), datetime.strptime(time_range['end_time'], "%H:%M").time())

            if force_use_end:
                op.use_end_date = force_use_end  # 사용 만료일
            else:
                if target_prd.use_end_period:
                    op.use_end_date = D().add_day_last_hour(target_prd.use_end_period)  # 사용 만료일
                if target_prd.use_end_date:
                    op.use_end_date = target_prd.use_end_date  # 사용 만료일

            op.code = ""
            op.user_name = user_name
            op.user_phone = user_phone
            op.user_email = user_email
            op.type = target_prd.type

            coupon = order_product_coupon(coupons, op, product.id)

            op.member_id = target_prd.member.id
            op.product_description = ''
            session.add(op)
            session.flush()

            if coupon:
                # 쿠폰 사용 처리
                use_coupon(session, ordr_idxx, op, coupon)

            # E쿠폰 발급 처리
            if op.type == "UP-EC" and op.status == "PD":
                if target_prd.api_provider == "M12":
                    tr_id = f"{ordr_idxx[8:]}_{op.id}"
                    try:
                        m12_req = ReqIssue(tr_id=tr_id, goods_id=target_prd.api_goods_id, send_no=CONIA_SMS_SENDER, recv_no=member.mobile)
                    except Exception as e:
                        session.commit()
                        # 쿠폰 발급 실패시 전체 롤백
                        cancel_order(session, order_data, pg_info)
                        analytics_data = {
                            "type": "e-coupon issue fail",
                            "file": "app/routers/views/order.py",
                            "func": "request",
                            "code": "API 호출 실패(M12)",
                            "data": str(e.args),
                        }
                        analytics("store-log", analytics_data)
                        raise exc.PgFailEx(msg="E쿠폰 발급 오류")
                    if op.use_end_date:
                        m12_req.period = D().convert_yyyymmdd(op.use_end_date)

                    m12_res: ResIssue = issue(m12_req)
                    if m12_res.STATUS_CODE == "0000":
                        ecoupon_data = Ecoupon()
                        ecoupon_data.provider = "M12"
                        ecoupon_data.goods_id = target_prd.api_goods_id
                        ecoupon_data.tr_id = tr_id
                        ecoupon_data.pin_code = m12_res.PIN_NO
                        ecoupon_data.period_date = op.use_end_date
                        ecoupon_data.kind = ""
                        ecoupon_data.duty_code = m12_res.DUTY_CODE
                        ecoupon_data.raw_data = m12_res.raw_data
                        ecoupon_data.order_id = ordr_idxx
                        ecoupon_data.order_product_id = op.id
                        ecoupon_data.customer_id = user.id
                        session.add(ecoupon_data)
                    else:
                        session.commit()
                        # 쿠폰 발급 실패시 전체 롤백
                        cancel_order(session, order_data, pg_info)
                        try:
                            analytics_data = {
                                "type": "e-coupon issue fail",
                                "file": "app/routers/views/order.py",
                                "func": "request",
                                "code": m12_res.RESULT_CODE,
                                "data": m12_res.raw_data,
                            }
                            analytics("store-log", analytics_data)
                        except:
                            pass
                        raise exc.PgFailEx(msg="E쿠폰 발급 오류")
                elif target_prd.api_provider == "DNC":
                    tr_id = f"{ordr_idxx[8:]}_{op.id}"
                    try:
                        dnc_req = DncReqIssue(tradeId=tr_id, productCode=target_prd.api_goods_id, quantity=1, requestedAt=D().now_str())
                        dnc_res: DncResIssue = dnc_issue(dnc_req)

                        if len(dnc_res.coupons) > 0:
                            ecoupon_data = Ecoupon()
                            ecoupon_data.provider = "DNC"
                            ecoupon_data.goods_id = target_prd.api_goods_id
                            ecoupon_data.tr_id = tr_id
                            ecoupon_data.pin_code = dnc_res.coupons[0].pinCode
                            ecoupon_data.period_date = op.use_end_date
                            ecoupon_data.kind = ""
                            ecoupon_data.duty_code = ""
                            ecoupon_data.order_code = dnc_res.coupons[0].orderCode
                            ecoupon_data.raw_data = dnc_res.raw_data
                            ecoupon_data.order_id = ordr_idxx
                            ecoupon_data.order_product_id = op.id
                            ecoupon_data.customer_id = user.id
                            session.add(ecoupon_data)
                        else:
                            raise exc.APIException(status_code=500, detail=dnc_res.raw_data)
                    except Exception as e:
                        session.commit()
                        # 쿠폰 발급 실패시 전체 롤백
                        cancel_order(session, order_data, pg_info)
                        analytics_data = {
                            "type": "e-coupon issue fail",
                            "file": "app/routers/views/order.py",
                            "func": "request",
                            "code": "API 호출 실패 (DNC)",
                            "data": str(e.args),
                        }
                        analytics("store-log", analytics_data)
                        raise exc.PgFailEx(msg="E쿠폰 발급 오류")
                elif target_prd.api_provider == "KT":
                    tr_id = f"{ordr_idxx[8:]}_{op.id}"
                    try:
                        kt_req = KtReqIssue(tradeId=tr_id, productCode=target_prd.api_goods_id, receiver=user_phone)
                        ec_kt = EcounponKt()
                        kt_res: KtResIssue = ec_kt.issue(kt_req)

                        ecoupon_data = Ecoupon()
                        ecoupon_data.provider = "KT"
                        ecoupon_data.goods_id = target_prd.api_goods_id
                        ecoupon_data.tr_id = tr_id
                        ecoupon_data.pin_code = kt_res.pinNo
                        ecoupon_data.period_date = op.use_end_date
                        ecoupon_data.kind = ""
                        ecoupon_data.duty_code = ""
                        ecoupon_data.order_code = ""
                        ecoupon_data.raw_data = kt_res.raw_data
                        ecoupon_data.order_id = ordr_idxx
                        ecoupon_data.order_product_id = op.id
                        ecoupon_data.customer_id = user.id
                        session.add(ecoupon_data)

                        op.status = "CP"
                        op.complete_date = D().now_str()
                    except Exception as e:
                        session.commit()
                        # 쿠폰 발급 실패시 전체 롤백
                        cancel_order(session, order_data, pg_info)
                        analytics_data = {
                            "type": "e-coupon issue fail",
                            "file": "app/routers/views/order.py",
                            "func": "request",
                            "code": "API 호출 실패 (KT)",
                            "data": str(e.args),
                        }
                        analytics("store-log", analytics_data)
                        raise exc.PgFailEx(msg="E쿠폰 발급 오류")
            analytics_data = {
                "store_code": store.code,
                "product_id": target_prd.id,
                "customer_id": user.id if user else None,
                "ip": get_ip(req)
            }
            analytics("order-product", analytics_data)

            # 장바구니 해당 상품 삭제
            session.query(Cart).filter(Cart.customer_id == user.id, Cart.product_option_id == product.product_option.id).delete()

    session.commit()

    # 품절 확인
    for sp in sheet_products:
        inven: Inventory = Inventory.get(session, product_option_id=sp.product_option_id)
        if inven.count < 1:
            # 재고 사용시 품절 확인
            product = sp.product_option.product
            if product.inven_use == "Y" and product.status == 'Y':
                p_options = session.query(ProductOption).filter(ProductOption.product_id == product.id, ProductOption.status == 'Y').all()
                opt_cnt = len(p_options)
                sold_out_cnt = 0
                for row in p_options:
                    if row.inventory.count <= row.inventory.safe_count:
                        sold_out_cnt += 1
                if opt_cnt == sold_out_cnt:
                    product.update(session, True, status='S')

    # 주문서 삭제
    session.query(OrderSheet).filter(OrderSheet.id == sheet_id).delete()
    session.commit()

    # 주문 완료 문자 전송
    if len(prd_titles) > 1:
        prd_title = f"{prd_titles[0]} 외 {len(prd_titles) - 1}건"
    else:
        prd_title = prd_titles[0]

    msg = f"""안녕하세요 [{member.name}]님!
[{store.title}]에서 주문하신 상품 결제가 완료되었습니다.

■주문일: {D().today_str()}
■주문번호: {ordr_idxx}
■상품명: {prd_title}
■주문금액: {int(total_amount):,}원

오늘도 기분 좋은 하루 보내세요!

{make_bottom_msg(req, store)}
"""
    send_sms(session, customer, store, msg, ordr_idxx)

    return RedirectResponse(f'/{store.code}/order/complete/{ordr_idxx}', status_code=status.HTTP_303_SEE_OTHER)


@router.post("/trade_reg")
def trade_reg(req: Request,
              store: Store = Depends(check_store),
              pay_type: str = Form(),
              ordr_idxx: str = Form(),
              good_name: str = Form(),
              good_mny: str = Form(),
              buyr_name: str = Form(),
              buyr_tel2: str = Form(default=None),
              buyr_mail: str = Form(),
              pay_method: str = Form(),
              site_cd: str = Form(),
              site_name: str = Form(),
              sheet_id: str = Form(),
              address_id: str = Form(default=None),
              memo: str = Form(default=None),
              client_type: str = Form(default=None),
              user_name: str = Form(default=None),
              user_phone: str = Form(default=None),
              user_email: str = Form(default=None),
              active_coupon: str = Form(default=None),
              tax_flag: str = Form(default=None),
              comm_tax_mny: int = Form(default=0),
              comm_vat_mny: int = Form(default=0),
              comm_free_mny: int = Form(default=0),
              session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    context_data = make_view_context_data(session, req, store, user)

    c = conf()

    return_url = f"{get_base_url(req)}{store.code}/order/mobile"
    cancel_url = f"{get_base_url(req)}{store.code}/order/sheet/{sheet_id}"
    req_data = {
        'site_cd': site_cd,
        'site_name': site_name,
        'kcp_cert_info': c.PG_KCP_CERT_INFO,
        'ordr_idxx': ordr_idxx,
        'good_mny': good_mny,
        'good_name': good_name,
        'buyr_name': buyr_name,
        'buyr_tel2': buyr_tel2,
        'buyr_mail': buyr_mail,
        'pay_method': pay_method,
        'Ret_URL': return_url,
        'escw_used': 'N',
        'user_agent': '',
        'sheet_id': sheet_id,
        'address_id': address_id,
        'memo': memo,
        'client_type': client_type,
        'user_name': user_name,
        'user_phone': user_phone,
        'user_email': user_email,
        'active_coupon': active_coupon,
        'tax_flag': tax_flag,
        'comm_tax_mny': comm_tax_mny,
        'comm_vat_mny': comm_vat_mny,
        'comm_free_mny': comm_free_mny,
    }

    if pay_type == 'payco':
        sheet_data: OrderSheet = OrderSheet.get(session, id=sheet_id)
        if sheet_data is None:
            raise exc.BadRequestEx(reason="주문서 오류")

        sheet_products: List[OrderSheetProduct] = sheet_data.products

        return_url = f"{get_base_url(req)}{store.code}/order/payco"

        taxation_type = 'TAXATION'
        if tax_flag == 'TG02':
            taxation_type = 'DUTYFREE'
        elif tax_flag == 'TG03':
            taxation_type = 'COMBINE'

        req_reserve_data = ReqReserve(
            sellerOrderReferenceKey=ordr_idxx,
            orderTitle=good_name,
            orderChannel=req.state.device,
            totalPaymentAmt=good_mny,
            totalTaxfreeAmt=comm_free_mny,
            totalTaxableAmt=comm_tax_mny,
            totalVatAmt=comm_vat_mny,
            productAmt=good_mny,
            productPaymentAmt=good_mny,
            orderQuantity="1",
            productName=good_name,
            sellerOrderProductReferenceKey=sheet_products[0].product_option.product_id,
            returnUrl=return_url,
            taxationType=taxation_type,
            # extraData=json.dumps({"cancelMobileUrl": cancel_url})
        )

        payco_res: ResReserve = reserve(req_reserve_data)
        # context_data.update(payco_res=payco_res)
        # context_data.update(req_data=req_data)
        # return templates.TemplateResponse("payco_trade_reg.html", context=context_data)
        return payco_res
    else:
        if pay_method == "100000000000":  # 신용카드
            pay_code = "CARD"
            action_result = "card"
            van_code = ""
        elif pay_method == "010000000000":  # 계좌이체
            pay_code = "BANK"
            action_result = "acnt"
            van_code = ""
        elif pay_method == "001000000000":  # 가상계좌
            pay_code = "VCNT"
            action_result = "vcnt"
            van_code = ""
        elif pay_method == "000100000000":  # 포인트
            pay_code = "TPNT"
            action_result = "tpnt"  # ??
            van_code = "SCWB"
        elif pay_method == "000010000000":  # 휴대폰
            pay_code = "MOBX"
            action_result = "mobx"
            van_code = ""
        else:
            raise exc.BadRequestEx

        post_data = {
            'pay_code': pay_code,
            'actionResult': action_result,
            'van_code': van_code
        }
        # 거래등록 API
        c = conf()
        target_url = f'{c.PG_KCP_HOST}/std/tradeReg/register'
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

        # 거래등록 API REQ DATA
        res = requests.post(target_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False, indent="\t").encode('utf8'))

        context_data.update(res_data=json.loads(res.text))
        context_data.update(post_data=post_data)

    context_data.update(req_data=req_data)

    return templates.TemplateResponse("payment_trade_reg.html", context=context_data)


@router.post("/mobile")
def mobile(req: Request,
           store: Store = Depends(check_store),
           site_cd: str = Form(default=None),
           site_name: str = Form(default=None),
           ordr_idxx: str = Form(default=None),
           good_mny: str = Form(default=None),
           good_name: str = Form(default=None),
           buyr_name: str = Form(default=None),
           buyr_tel2: str = Form(default=None),
           buyr_mail: str = Form(default=None),
           Ret_URL: str = Form(default=None),
           pay_code: str = Form(default=None),
           ActionResult: str = Form(default=None),
           van_code: str = Form(default=None),
           approvalKey: str = Form(default=None),
           traceNo: str = Form(default=None),
           PayUrl: str = Form(default=None),
           enc_info: str = Form(default=None),
           enc_data: str = Form(default=None),
           res_cd: str = Form(default=None),
           res_msg: str = Form(default=None),
           req_tx: str = Form(default=None),
           tran_cd: str = Form(default=None),
           use_pay_method: str = Form(default=None),
           param_opt_1: str = Form(default=None),
           sheet_id: str = Form(default=None),
           address_id: str = Form(default=None),
           memo: str = Form(default=None),
           client_type: str = Form(default=None),
           user_name: str = Form(default=None),
           user_phone: str = Form(default=None),
           user_email: str = Form(default=None),
           active_coupon: str = Form(default=None),
           comm_tax_mny: int = Form(default=0),
           comm_vat_mny: int = Form(default=0),
           comm_free_mny: int = Form(default=0),
           session: Session = Depends(db.session)):
    if res_cd == '0000':
        post_data = {}
        # enc_info 값이 없을 경우 POST DATA 처리 후 order_mobile 이동
        if not enc_info:
            extra_data = {
                "sheet_id": sheet_id,
                "address_id": address_id,
                "memo": memo,
                "client_type": client_type,
                "user_name": user_name,
                "user_phone": user_phone,
                "user_email": user_email,
                "active_coupon": active_coupon,
                "comm_tax_mny": comm_tax_mny,
                "comm_vat_mny": comm_vat_mny,
                "comm_free_mny": comm_free_mny,
            }
            post_data = {
                'approvalKey': approvalKey,
                'traceNo': traceNo,
                'PayUrl': PayUrl,
                'pay_code': pay_code,
                'actionResult': ActionResult,
                'Ret_URL': Ret_URL,
                'van_code': van_code,
                'site_cd': site_cd,
                'site_name': site_name,
                'buyr_name': buyr_name,
                'buyr_tel2': buyr_tel2,
                'buyr_mail': buyr_mail,
                'ordr_idxx': ordr_idxx,
                'good_name': good_name,
                'good_mny': good_mny,
                'param_opt_1': json.dumps(extra_data, ensure_ascii=False),
            }
        else:
            extra_data = json.loads(param_opt_1)
            post_data = {
                'req_tx': req_tx,  # 요청 종류
                'res_cd': res_cd,  # 응답 코드
                'site_cd': site_cd,  # 사이트코드
                'tran_cd': tran_cd,  # 트랜잭션 코드
                'ordr_idxx': ordr_idxx,  # 쇼핑몰 주문번호
                'good_name': good_name,  # 상품명
                'good_mny': good_mny,  # 결제 금액
                'buyr_name': buyr_name,  # 주문자명
                'buyr_tel2': buyr_tel2,  # 주문자 핸드폰 번호
                'buyr_mail': buyr_mail,  # 주문자 E-mail 주소
                'use_pay_method': use_pay_method,  # 결제 방법
                'enc_info': enc_info,  # 암호화 정보
                'enc_data': enc_data,  # 암호화 데이터
                'sheet_id': extra_data["sheet_id"],
                'address_id': extra_data["address_id"],
                'memo': extra_data["memo"],
                'client_type': extra_data["client_type"],
                'user_name': extra_data["user_name"],
                'user_phone': extra_data["user_phone"],
                'user_email': extra_data["user_email"],
                'active_coupon': extra_data["active_coupon"],
                'comm_tax_mny': extra_data["comm_tax_mny"],
                'comm_vat_mny': extra_data["comm_vat_mny"],
                'comm_free_mny': extra_data["comm_free_mny"],
            }
    else:
        post_data = {
            'res_cd': res_cd,  # 응답 코드
            'res_msg': res_msg,  # 응답 메세지
            'good_mny': ''
        }

    context_data = make_view_context_data(session, req, store, None)
    context_data.update(post_data=post_data)

    return templates.TemplateResponse("kcp_order_mobile.html", context=context_data)


@router.get("/payco")
def payco(req: Request,
          store: Store = Depends(check_store),
          session: Session = Depends(db.session)):
    context_data = make_view_context_data(session, req, store, None)
    return templates.TemplateResponse("payco_trade_confirm.html", context=context_data)


@router.get("/sheet/{sheet_id}")
def sheet(req: Request, store_code: str, sheet_id: str,
          store: Store = Depends(check_store),
          session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    customer = Customer.get(session, id=user.id)
    if customer.auth_yn == 'N':
        response = RedirectResponse(f'/{store_code}/auth/verify?referer={req.url}')
        return response

    sheet_data = OrderSheet.get(session=session, id=sheet_id, customer_id=user.id)

    if not sheet_data:
        raise exc.ViewNotFoundEx

    sheet_products: List[OrderSheetProduct] = OrderSheetProduct.filter(session=session, order_sheet_id=sheet_id).all()

    products = []
    shipping = {}
    product_grp = {}
    total_prd_price = 0
    total_shipping = 0
    tax_type = "T"  # 과세 : T / 비과세 : F / 복합 : TF
    tax_type_list = []
    disable_pg_provider = {}

    for sp in sheet_products:
        if not check_product_state(session, sp.product_option.product_id, sp.product_option_id, store_code):
            raise exc.NotFoundDataEx
        sheet_product = sp.product_option.product

        if sheet_product.pg_provider:
            disable_target_list = sheet_product.pg_provider.split("|")
            for row in disable_target_list:
                if disable_pg_provider.get(row):
                    disable_pg_provider[row].append(sheet_product.name)
                else:
                    disable_pg_provider[row] = [sheet_product.name]

        option = dict(
            sp_id=sp.id,
            opt_id=sp.product_option.id,
            option=sp.product_option,
            amount=sp.amount,
            count=sp.ea,
            weight=sp.ea * sp.product_option.weight if sp.product_option.weight else 0,
        )

        prd_grp_row = product_grp.get(sp.product_option.product_id)
        if prd_grp_row:
            prd_grp_row["options"].append(option)
        else:
            product_grp[sp.product_option.product_id] = dict(id=sp.product_option.product_id, product=sheet_product, options=[option])

        prd = dict(
            sp_id=sp.id,
            product=sheet_product,
            option=sp.product_option,
            amount=sp.amount,
            count=sp.ea,
            weight=sp.ea * sp.product_option.weight if sp.product_option.weight else 0,
        )
        products.append(prd)
        tax_type_list.append(sheet_product.tax)

        if sheet_product.shipping_info:
            if sheet_product.shipping_info.calc_type == "개별":
                ship_key = f"{sheet_product.shipping_info.id}_{sheet_product.id}"
            else:
                ship_key = sheet_product.shipping_info.id

            shipping_data = shipping.get(ship_key)

            if shipping_data:
                shipping_data["products"].append(prd)
            else:
                # 도서산간 추가 배송비
                add_cost = 0
                if sheet_product.shipping_info.costs:
                    for cost_data in sheet_product.shipping_info.costs:
                        if cost_data.category == 'add':
                            add_cost = cost_data.cost
                            break

                shipping[ship_key] = dict(info=sheet_product.shipping_info,
                                          shipping_title=sheet_product.shipping_info.member.company.name,
                                          cost=0,
                                          add_cost=add_cost,
                                          prd_grp=[],
                                          products=[prd])

        total_prd_price += sp.amount

    for row in shipping.values():
        shipping_info = row.get("info")
        shipping_products = row.get("products")

        product_group = {}
        for prd in shipping_products:
            option = dict(
                sp_id=prd["sp_id"],
                option=prd["option"],
                amount=prd["amount"],
                count=prd["count"],
                weight=prd["count"] * prd["option"].weight if prd["option"].weight else 0,
            )

            prd_grp_row = product_group.get(prd["product"].id)
            if prd_grp_row:
                prd_grp_row["options"].append(option)
                prd_grp_row["amount"] = prd_grp_row["amount"] + prd["amount"]
                prd_grp_row["count"] = prd_grp_row["count"] + prd["count"]
                prd_grp_row["weight"] = prd_grp_row["weight"] + prd["count"] * prd["option"].weight if prd["option"].weight else 0
            else:
                product_group[prd["product"].id] = dict(product=prd["product"],
                                                        options=[option],
                                                        amount=prd["amount"],
                                                        count=prd["count"],
                                                        weight=prd["count"] * prd["option"].weight if prd["option"].weight else 0)

        prd_grp_list = list(product_group.values())
        for prd_grp_row in prd_grp_list:
            prd_total_amount = 0
            for opt in prd_grp_row["options"]:
                prd_total_amount += opt["amount"]
            prd_grp_row.update(prd_total_amount=prd_total_amount)
        row.update(prd_grp=prd_grp_list)

        if shipping_info.pay_type == "선불":
            if shipping_info.calc_type == "묶음":
                total_cost = 0
                total_ea = 0
                total_weight = 0
                for prd in shipping_products:
                    total_cost += prd.get("amount")
                    total_ea += prd.get("count")
                    total_weight += prd.get("weight")

                if shipping_info.costs:
                    cost_type = shipping_info.costs[0].type
                    if cost_type == "free":
                        continue
                    elif cost_type == "fix":
                        total_shipping += shipping_info.costs[0].cost
                        row.update(cost=shipping_info.costs[0].cost)
                    elif cost_type == "cost":
                        total_shipping += calc_shipping(shipping_info, total_cost)
                        row.update(cost=calc_shipping(shipping_info, total_cost))
                    elif cost_type == "ea":
                        total_shipping += calc_shipping(shipping_info, total_ea)
                        row.update(cost=calc_shipping(shipping_info, total_ea))
                    elif cost_type == "weight":
                        total_shipping += calc_shipping(shipping_info, total_weight)
                        row.update(cost=calc_shipping(shipping_info, total_weight))

            elif shipping_info.calc_type == "개별":
                for prd in prd_grp_list:
                    if shipping_info.costs:
                        cost_type = shipping_info.costs[0].type
                        if cost_type == "free":
                            continue
                        elif cost_type == "fix":
                            total_shipping += shipping_info.costs[0].cost
                            row.update(cost=row.get("cost") + shipping_info.costs[0].cost)
                        elif cost_type == "cost":
                            total_shipping += calc_shipping(shipping_info, prd.get("amount"))
                            row.update(cost=row.get("cost") + calc_shipping(shipping_info, prd.get("amount")))
                        elif cost_type == "ea":
                            total_shipping += calc_shipping(shipping_info, prd.get("count"))
                            row.update(cost=row.get("cost") + calc_shipping(shipping_info, prd.get("count")))
                        elif cost_type == "weight":
                            total_shipping += calc_shipping(shipping_info, prd.get("weight"))
                            row.update(cost=row.get("cost") + calc_shipping(shipping_info, prd.get("weight")))

    total_amount = total_prd_price + total_shipping

    member = Customer.get(session, id=user.id)
    member = DataCustomer.from_orm(member)

    address: List[DeliveryAddress] = DeliveryAddress.filter(session=session, customer_id=member.id).all()

    convert_address: List[DataDeliveryAddress] = []

    address_default = None
    for row in address:
        convert_address.append(DataDeliveryAddress.from_orm(row))
        if row.default_yn == 'Y':
            address_default = DataDeliveryAddress.from_orm(row)

    # 사용 가능 쿠폰 분류

    coupons: List[Coupon] = session.query(Coupon).filter(Coupon.customer_id == user.id,
                                                         Coupon.use_yn == "N",
                                                         Coupon.begin_date <= D().now,
                                                         Coupon.end_date >= D().now).all()
    able_coupon = []
    for row in coupons:
        coupon_data = DataCoupon.from_orm(row)
        if row.target == 'all':
            able_coupon.append(coupon_data)
            continue
        for prd_row in list(product_grp.values()):
            if row.product_id == prd_row.get("product").id:
                able_coupon.append(coupon_data)
                continue
            if row.coupon_group.coupon_target:
                cp_target_list = coupon_data.coupon_group.coupon_target
                next_flag = True
                for cp_target in cp_target_list:
                    if cp_target.member_id:
                        if str(prd_row.get("product").member_id) == cp_target.member_id:
                            able_coupon.append(coupon_data)
                            next_flag = False
                            break
                    elif cp_target.product_id:
                        if str(prd_row.get("product").id) == cp_target.product_id:
                            able_coupon.append(coupon_data)
                            next_flag = False
                            break
                if not next_flag:
                    break
    if able_coupon:
        for data_coupon in able_coupon:
            if data_coupon.target != 'all':
                if data_coupon.coupon_group.coupon_target:
                    for target in data_coupon.coupon_group.coupon_target:
                        if target.member_id:
                            pa_prd_list: List[Product] = Product.filter(session, status='Y', member_id=target.member_id).all()
                            for pa_prd in pa_prd_list:
                                data_coupon.able_prd_list.append(str(pa_prd.id))
                        else:
                            data_coupon.able_prd_list.append(str(target.product_id))
                    data_coupon.able_prd_str = ','.join(data_coupon.able_prd_list)
                elif data_coupon.product_id:
                    data_coupon.able_prd_str = data_coupon.product_id

    prd_grp_list = list(product_grp.values())
    prd_grp_list.sort(key=itemgetter('id'))
    for prd_grp_row in prd_grp_list:
        prd_total_amount = 0
        prd_grp_row["options"].sort(key=itemgetter('opt_id'))
        for opt in prd_grp_row["options"]:
            prd_total_amount += opt["amount"]
        prd_grp_row.update(prd_total_amount=prd_total_amount)

    tax_count = tax_type_list.count('Y')
    tax_free_count = tax_type_list.count('N')
    if tax_count > 0 and tax_free_count > 0:
        tax_type = "TF"
    elif tax_count > 0 and tax_free_count == 0:
        tax_type = "T"
    elif tax_free_count > 0 and tax_count == 0:
        if total_shipping > 0:
            tax_type = "TF"
        else:
            tax_type = "F"

    context_data = make_view_context_data(session, req, store, user)

    disable_pg_provider_list = []
    disable_pg_provider_prd = {}
    if store.prd_pg_opt_use == 'Y' or (context_data.get('dupl_store') and context_data.get('dupl_store').prd_pg_opt_use == 'Y'):
        for k, v in disable_pg_provider.items():
            disable_pg_provider_list.append(k)
            disable_pg_provider_prd[k] = set(v)

    c = conf()
    context_data.update(address=address,
                        address_default=address_default,
                        order_num=order_numbering(),
                        site_code=c.PG_KCP_SITE_CODE,
                        kcp_host=c.PG_KCP_PC_HOST,
                        products=products,
                        product_grp=prd_grp_list,
                        store=store,
                        member=member,
                        able_coupon=able_coupon,
                        shippings=shipping.values(),
                        total_prd_price=total_prd_price,
                        total_amount=total_amount,
                        total_shipping=total_shipping,
                        tax_type=tax_type,
                        disable_pg_provider_list=disable_pg_provider_list,
                        disable_pg_provider_prd=disable_pg_provider_prd)

    return templates.TemplateResponse("checkout-payment.html", context=context_data)


@router.get("/complete/{order_id}")
def complete(req: Request, order_id: int,
             store: Store = Depends(check_store),
             session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    order_data = session.query(Order).filter(Order.id == order_id, Order.customer_id == user.id, or_(Order.status == "PD", Order.status == "PW")).first()
    pg_info = session.query(PgInfo).filter(PgInfo.order_id == order_id).first()

    if not order_data:
        raise exc.ViewNotFoundEx

    osl: List[OrderShipping] = OrderShipping.filter(session, order_id=order_id).all()
    opl: List[OrderProduct] = OrderProduct.filter(session, order_id=order_id).all()

    data = {}
    for row in osl:
        data[row.id] = dict(
            title=row.member.company.name,
            products=[],
        )
    if osl:
        for row in opl:
            data[row.order_shipping_id].get('products').append(row)
    else:
        data[opl[0].id] = dict(
            title=opl[0].member.company.name,
            products=opl,
        )

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(order_id=order_id)
    context_data.update(datas=data.values())
    context_data.update(order=order_data)
    context_data.update(pg_info=make_pg_info(pg_info))

    return templates.TemplateResponse("checkout-complete.html", context=context_data)


@router.get("/history/{order_id}")
def order_detail(req: Request, store_code: str, order_id: int,
                 store: Store = Depends(check_store),
                 session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    order = session.query(Order).filter(Order.id == order_id, Order.customer_id == user.id, Order.status != "D").first()
    pg_info = session.query(PgInfo).filter(PgInfo.order_id == order_id).first()

    if not order:
        raise exc.ViewNotFoundEx

    context_data = make_view_context_data(session, req, store, user)

    now = D().now
    able_count = 0
    cancel_able = True
    product_cancel_able = True
    products: List[OrderProduct] = order.products
    for prd in products:
        review = ProductReview.filter(session, order_product_id=prd.id, product_id=prd.product_id, customer_id=user.id, status="Y").first()
        if review:
            prd.review_id = review.id
        if prd.use_end_date and prd.use_end_date < now:
            cancel_able = False
            continue
        else:
            able_count += 1
        if prd.status != "PD":
            cancel_able = False
        if prd.product.cancel_yn == 'N':
            product_cancel_able = False

    context_data.update(order=order)

    cancel_disable = None
    if pg_info:
        context_data.update(pg_info=make_pg_info(pg_info))

        if order.pg_info and order.pg_info.app_time[:8] != D().yyyymmdd() and order.pg_info.pg_info_sub:
            sub_list: List[PgInfoSub] = order.pg_info.pg_info_sub
            for sub in sub_list:
                if sub.kind == '식권 쿠폰':
                    cancel_disable = '식권 쿠폰 사용 결제 입니다.'
                    break

    tracker_api_key = SettingValue.get(session, type="sweet_tracker_api_key")
    context_data.update(sweet_tracker_api_key=tracker_api_key.value)
    context_data.update(now=now)
    context_data.update(able_count=able_count)
    context_data.update(cancel_able=cancel_able)
    context_data.update(cancel_disable=cancel_disable)
    context_data.update(product_cancel_able=product_cancel_able)

    return templates.TemplateResponse("order-tracking.html", context=context_data)


@router.get("/re_step1/{order_id}")
def re(req: Request, order_id: int,
       store: Store = Depends(check_store),
       session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    order_data = Order.get(session=session, id=order_id, customer_id=user.id)

    if not order_data:
        raise exc.ViewNotFoundEx

    opl: List[OrderProduct] = session.query(OrderProduct).filter(OrderProduct.order_id == order_id, or_(OrderProduct.status == "DN", OrderProduct.status == "DC")).all()

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(order_id=order_id)
    context_data.update(order_products=opl)

    return templates.TemplateResponse("account-return-exchange-select.html", context=context_data)


@router.post("/re_step2/{order_id}")
def re(req: Request, order_id: int,
       prd_ids: str = Form(title="타겟 상품 아이디 리스트"),
       store: Store = Depends(check_store),
       session: Session = Depends(db.session), user: MemberToken = Depends(token_user)):
    order_data = Order.get(session=session, id=order_id, customer_id=user.id)

    if not order_data:
        raise exc.ViewNotFoundEx

    opl: List[OrderProduct] = OrderProduct.filter(session, order_id=order_id).all()
    sel_opl: List[OrderProduct] = []

    prd_id_list = prd_ids.split(",")

    for sel_prd_id in prd_id_list:
        for op in opl:
            if op.id == int(sel_prd_id):
                sel_opl.append(op)

    if len(sel_opl) == 0:
        raise exc.ViewNotFoundEx

    ids = []
    for row in sel_opl:
        ids.append(str(row.id))
    join_str = ",".join(ids)

    context_data = make_view_context_data(session, req, store, user)
    context_data.update(order_id=order_id)
    context_data.update(order_products=sel_opl)
    context_data.update(order_product_ids=join_str)

    return templates.TemplateResponse("account-return-exchange-reason.html", context=context_data)


def calc_shipping(sp: ShippingInfo, value):
    cost_sections: List[ShippingCost] = sp.costs

    for section in cost_sections:
        if section.section_repeat:
            target_value = value - section.section_start
            if target_value == 0:
                return section.cost * 2
            else:
                return section.cost * (2 + floor(target_value / section.section_repeat))
        else:
            section_end = section.section_end
            if section_end is None:
                section_end = 999999999

            if section.section_start <= value < section_end:
                return section.cost


def get_shipping_amount(shipping, rural_area):
    total_shipping = 0
    if shipping:
        for row in shipping.values():
            shipping_info = row.get("info")
            shipping_products = row.get("products")

            # 도서산간 추가 배송비
            if rural_area:
                if shipping_info.costs:
                    for cost_data in shipping_info.costs:
                        if cost_data.category == 'add':
                            total_shipping += cost_data.cost
                            row.update(add_cost=cost_data.cost)
                            break

            product_group = {}
            for prd in shipping_products:
                prd_grp_row = product_group.get(prd["product"].id)
                if prd_grp_row:
                    prd_grp_row["amount"] = prd_grp_row["amount"] + prd["amount"]
                    prd_grp_row["count"] = prd_grp_row["count"] + prd["count"]
                    prd_grp_row["weight"] = prd_grp_row["weight"] + prd["count"] * prd["option"].weight if prd["option"].weight else 0
                else:
                    product_group[prd["product"].id] = dict(amount=prd["amount"],
                                                            count=prd["count"],
                                                            weight=prd["count"] * prd["option"].weight if prd["option"].weight else 0)
            prd_grp_list = list(product_group.values())

            if shipping_info.pay_type == "선불":
                if shipping_info.calc_type == "묶음":
                    total_cost = 0
                    total_ea = 0
                    total_weight = 0
                    for prd in shipping_products:
                        total_cost += prd.get("amount")
                        total_ea += prd.get("count")
                        total_weight += prd.get("weight")

                    if shipping_info.costs:
                        cost_type = shipping_info.costs[0].type
                        if cost_type == "free":
                            pass
                        elif cost_type == "fix":
                            total_shipping += shipping_info.costs[0].cost
                            row.update(cost=shipping_info.costs[0].cost)
                        elif cost_type == "cost":
                            total_shipping += calc_shipping(shipping_info, total_cost)
                            row.update(cost=calc_shipping(shipping_info, total_cost))
                        elif cost_type == "ea":
                            total_shipping += calc_shipping(shipping_info, total_ea)
                            row.update(cost=calc_shipping(shipping_info, total_ea))
                        elif cost_type == "weight":
                            total_shipping += calc_shipping(shipping_info, total_weight)
                            row.update(cost=calc_shipping(shipping_info, total_weight))

                elif shipping_info.calc_type == "개별":
                    for prd in prd_grp_list:
                        if shipping_info.costs:
                            cost_type = shipping_info.costs[0].type
                            if cost_type == "free":
                                continue
                            elif cost_type == "fix":
                                total_shipping += shipping_info.costs[0].cost
                                row.update(cost=row.get("cost") + shipping_info.costs[0].cost)
                            elif cost_type == "cost":
                                total_shipping += calc_shipping(shipping_info, prd.get("amount"))
                                row.update(cost=row.get("cost") + calc_shipping(shipping_info, prd.get("amount")))
                            elif cost_type == "ea":
                                total_shipping += calc_shipping(shipping_info, prd.get("count"))
                                row.update(cost=row.get("cost") + calc_shipping(shipping_info, prd.get("count")))
                            elif cost_type == "weight":
                                total_shipping += calc_shipping(shipping_info, prd.get("weight"))
                                row.update(cost=row.get("cost") + calc_shipping(shipping_info, prd.get("weight")))
    return total_shipping


def get_product_amount(product, coupons=None):
    total_amount = 0
    total_discount = 0
    for prd in list(product.values()):
        active_coupon = None
        if coupons:
            for row in coupons:
                if int(row['active_target']) == prd.get('product').id:
                    active_coupon = row
        if active_coupon:
            discount = int(int(prd.get('amount')) * (int(active_coupon["percent"]) / 100))
            total_amount += (int(prd.get('amount')) - discount)
            total_discount += discount
            active_coupon["discount"] = discount
        else:
            total_amount += prd.get('amount')
    return total_amount, total_discount


def get_option_amount(sheet_products: List[OrderSheetProduct], coupons=None):
    total_amount = 0
    total_discount = 0
    for prd in sheet_products:
        active_coupon = None
        if coupons:
            for row in coupons:
                if row['sp_id'] == prd.id:
                    active_coupon = row
        if active_coupon:
            discount = 0
            if active_coupon["percent"] and active_coupon["percent"] != 'None':
                discount = int(int(prd.amount) * (int(active_coupon["percent"]) / 100))
            elif active_coupon["amount"] and active_coupon["amount"] != 'None':
                if isinstance(active_coupon["amount"], str) and '.' in active_coupon["amount"]:
                    discount = int(float(active_coupon["amount"]))
                else:
                    discount = int(active_coupon["amount"])
            total_amount += (int(prd.amount) - discount)
            total_discount += discount
            active_coupon["discount"] = discount
        else:
            total_amount += prd.amount
    return total_amount, total_discount


def prd_cart_item(session, cart_item, target_store_code):
    product = DataProduct.from_orm(cart_item.product_option.product)
    po = DataOptions.from_orm(cart_item.product_option)
    sp = StoreProduct.get(session, store_code=target_store_code, product_id=product.id)
    if sp is None:
        product.status = "P"

    if sp and sp.variation != 0:
        po.selling_price += sp.variation

    is_sold_out = False
    if product.status == 'S':
        is_sold_out = True

    if product.inven_use == "Y":
        if po.inventory.count <= po.inventory.safe_count:
            is_sold_out = True

    now = D().now
    now_time = now.time()

    if po.status == "D":
        product.status = "P"

    if product.sale_start_date and (product.sale_start_date > now):
        product.status = 'PT'

    if product.sale_end_date and (product.sale_end_date < now):
        product.status = 'PT'

    if product.sale_start_time and (product.sale_start_time > now_time):
        product.status = 'PT'

    if product.sale_end_time and (product.sale_end_time < now_time):
        product.status = 'PT'

    if product.use_end_date and (product.use_end_date < now):
        product.status = 'PT'

    prd = dict(
        cart_id=cart_item.id,
        product=product,
        checked=cart_item.checked,
        count=cart_item.count,
        option=po,
        is_sold_out=is_sold_out,
        status=product.status,
        cart_type=cart_item.type,
    )

    return prd


def make_pg_info(pg_info):
    if pg_info:
        payment_type = ""
        if pg_info.kind == "card":
            payment_type = "신용카드"
        elif pg_info.kind == "bank":
            payment_type = "계좌이체"
        elif pg_info.kind == "vbank":
            payment_type = "가상계좌"
        elif pg_info.kind == "point":
            if pg_info.provider == 'PAYCO':
                payment_type = "PAYCO 포인트"
            else:
                payment_type = "포인트"
        elif pg_info.kind == "mobile":
            payment_type = "휴대폰"

        card_info = ""
        if pg_info.card_name:
            if pg_info.card_quota == "00":
                quota = " 일시불"
            else:
                quota = f" {pg_info.card_quota}개월"

            card_no_str = ''
            if pg_info.card_no:
                card_no_str = f" ({pg_info.card_no[:4]}-****-****-****)"

            card_info = f"{pg_info.card_name}{card_no_str}{quota}"

        vbank_info = {}
        if pg_info.kind == "vbank":
            vbank_info["bankname"] = pg_info.bankname
            vbank_info["virtual_account"] = pg_info.virtual_account
            vbank_info["virtual_date"] = pg_info.virtual_date

        return dict(
            payment_type=payment_type,
            card_info=card_info,
            vbank_info=vbank_info,
            kind=pg_info.kind,
            amount=pg_info.amount,
        )
    else:
        return None


def save_order_shipping(session, row, ordr_idxx):
    os = OrderShipping()
    os.status = 'R'
    os.cost = row.get('cost') + row.get('add_cost') if row.get('add_cost') else row.get('cost')
    os.shipping_type = row.get('info').type
    os.pay_type = row.get('info').pay_type
    os.order_id = ordr_idxx
    os.member_id = row.get('info').member_id
    os.shipping_info_id = row.get('info').id
    session.add(os)
    session.commit()

    return os


def save_order_product(session, row, ordr_idxx, os, store, user, req, coupons, pay_kind):
    for prd in row.get('products'):
        op = OrderProduct()
        if pay_kind == "vbank":
            op.status = "PW"
        else:
            op.status = "PD"
        op.order_id = ordr_idxx
        op.product_option_id = prd.get('option').id
        op.product_code = prd.get('product').code
        op.product_id = prd.get('product').id
        op.ea = prd.get('count')
        op.product_name = prd.get('product').name
        op.product_thumbnail = prd.get('product').photos[0].uri
        op.amount = prd.get('amount')
        op.origin_price = prd.get('option').origin_price * prd.get('count')
        op.seller_title = prd.get('product').member.company.name if prd.get('product').member.company.name else prd.get('product').member.name

        op.member_id = prd.get('product').member.id
        op.product_description = ''
        op.order_shipping_id = os.id
        op.type = prd.get('product').type

        coupon = order_product_coupon(coupons, op, prd['id'])
        session.add(op)
        session.flush()

        if coupon:
            # 쿠폰 사용 처리
            use_coupon(session, ordr_idxx, op, coupon)

        analytics_data = {
            "store_code": store.code,
            "product_id": prd.get('product').id,
            "customer_id": user.id if user else None,
            "ip": get_ip(req)
        }
        analytics("order-product", analytics_data)

        # 장바구니 해당 상품 삭제
        session.query(Cart).filter(Cart.customer_id == user.id, Cart.product_option_id == prd.get('option').id).delete()


def order_product_coupon(coupons, op: OrderProduct, sp_id: str):
    if coupons:
        for coupon in coupons:
            if coupon['sp_id'] == sp_id:
                op.discount = coupon['discount']
                return coupon


def use_coupon(session: Session, ordr_idxx, op: OrderProduct, coupon):
    cp = Coupon.get(session, id=coupon['id'])
    cp.update(session, False, use_yn='Y', use_date=D().now)
    oc = OrderCoupon()
    oc.coupon_id = cp.id
    oc.order_id = ordr_idxx
    oc.discount = coupon["discount"]
    oc.order_product_id = op.id
    session.add(oc)


def convert_pay_kind(ret_pay_method=None, use_pay_method=None, mainPgCode=None):
    pay_kind = "etc"

    if ret_pay_method and ret_pay_method.find("0") == -1:
        pay_kind = ret_pay_method
    elif use_pay_method:
        if use_pay_method == "100000000000":  # 신용카드
            pay_kind = "card"
        elif use_pay_method == "010000000000":  # 계좌이체
            pay_kind = "bank"
        elif use_pay_method == "001000000000":  # 가상계좌
            pay_kind = "vbank"
        elif use_pay_method == "000100000000":  # 포인트
            pay_kind = "point"  # ??
        elif use_pay_method == "000010000000":  # 휴대폰
            pay_kind = "mobile"
    elif mainPgCode:
        if mainPgCode == "31" or mainPgCode == "01" or mainPgCode == "51":  # 신용카드
            pay_kind = "card"
        elif mainPgCode == "04" or mainPgCode == "35":  # 계좌이체
            pay_kind = "bank"
        elif mainPgCode == "02":  # 무통장
            pay_kind = "vbank"
        elif mainPgCode == "70" or mainPgCode == "75" or mainPgCode == "76" or mainPgCode == "77" or mainPgCode == "78":  # 쿠폰
            pay_kind = "voucher"
        elif mainPgCode == "98":  # 포인트
            pay_kind = "point"
        elif mainPgCode == "60" or mainPgCode == "05":  # 휴대폰
            pay_kind = "mobile"

    return pay_kind


def save_pg_info_sub(session: Session, payment_details: List[PaymentDetails], pg_info_id):
    meal_coupon_use = False
    for pay_data in payment_details:
        pg_info_sub = PgInfoSub()
        pg_info_sub.pg_info_id = pg_info_id
        pg_info_sub.kind = pay_data.paymentMethodName
        pg_info_sub.tno = pay_data.paymentTradeNo
        pg_info_sub.amount = pay_data.paymentAmt
        session.add(pg_info_sub)
        if pay_data.paymentMethodName == "식권 쿠폰":
            meal_coupon_use = True
    session.commit()
    return meal_coupon_use


def cancel_order(session: Session, order: Order, pg_info: PgInfo):
    order.status = "CD"

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
    OrderProduct.filter(session, order_id=order.id).update_q(True, status='CD')

    ops: List[OrderProduct] = session.query(OrderProduct).filter(OrderProduct.order_id == order.id).all()
    for op in ops:
        if op.ecoupon:
            if op.ecoupon.provider == 'M12':
                req = ReqInfo(tr_id=op.ecoupon.tr_id, goods_id=op.ecoupon.goods_id, pin_no=op.ecoupon.pin_code)
                res: m12ResCancel = m12_cancel(req)
                if res.STATUS_CODE == '0000':
                    op.ecoupon.status = 'D'
                else:
                    op.ecoupon.status = 'DE'
            elif op.ecoupon.provider == 'DNC':
                dnc_req = DncReqCancel(tradeId=op.ecoupon.tr_id, pinCode=op.ecoupon.pin_code, orderCode='', requestedAt=D().now_str())
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
    cancel_data.pg_info_order_id = order.id
    cancel_data.tno = cancel_tno
    cancel_data.type = "ALL"
    cancel_data.reg_date = datetime.strptime(cancel_time, "%Y%m%d%H%M%S")
    cancel_data.amount = pg_info.amount
    session.add(cancel_data)
    session.commit()


def get_current_time_range(now, time_table):
    for time_range in time_table:
        start_time = datetime.strptime(time_range["start_time"], "%H:%M").time()
        end_time = datetime.strptime(time_range["end_time"], "%H:%M").time()

        # 시간 범위 내에 현재 시간이 있는지 확인
        if start_time <= now < end_time:
            return time_range

    return None
