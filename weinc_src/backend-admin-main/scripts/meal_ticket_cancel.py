from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from scripts.database.conn import db
from app.database.schema import Store, OrderProduct, Order, PgInfoSub, PgInfo, PgCancel, LogOrder
from app.models.common import LogOrderDataIn

from app.utils.common_utils import log_msg
from app.utils.date_utils import D
from app.utils.pg_payco import cancel as payco_cancel, ReqCancel, ResCancel
from app.utils.ecoupon_m12 import info, ReqInfo, ResInfo, cancel as m12_cancel, ResCancel as m12ResCancel
from app.utils.ecoupon_dnc import cancel as dnc_cancel, ReqCancel as DncReqCancel, ResCancel as DncResCancel
from app.utils.ecoupon_kt import EcounponKt, ReqCancel as KtReqCancel, ResBase as KtResBase
from app.utils.log import L


def cancel(session: Session, order_id):
    order: Order = Order.get(session, id=order_id)
    pg_info = PgInfo.get(session, order_id=order_id)

    data = ReqCancel(orderNo=pg_info.tid,
                     cancelTotalAmt=str(int(order.final_amount)),
                     orderCertifyKey=pg_info.cancel_key)
    res: ResCancel = payco_cancel(data)
    cancel_time = res.cancelYmdt
    cancel_tno = res.cancelTradeSeq

    order.update(session, True, status="CD")
    OrderProduct.filter(session, order_id=order_id).update_q(True, status='CD')
    ops: List[OrderProduct] = session.query(OrderProduct).filter(OrderProduct.order_id == order_id).all()

    pg_info.update(session, True, cancel_type='all', cancel_date=datetime.strptime(cancel_time, "%Y%m%d%H%M%S"), cancel_mny=pg_info.amount, remain_amount=0)
    cancel_data = PgCancel()
    cancel_data.pg_info_order_id = order_id
    cancel_data.tno = cancel_tno
    cancel_data.type = "ALL"
    cancel_data.reg_date = datetime.strptime(cancel_time, "%Y%m%d%H%M%S")
    cancel_data.amount = pg_info.amount
    session.add(cancel_data)
    session.commit()

    # 로깅
    log_data = LogOrderDataIn(action="주문 전체취소", order_id=order_id, msg=log_msg("msg", f"주문 전체취소 (상점 일괄 취소 기능)"),  writer=f"시스템:{3}")
    LogOrder.create(session, auto_commit=True, **log_data.dict())


if __name__ == '__main__':
    L().info("Start")
    db.startup()

    sess: Session
    with db.session as sess:
        target_store = sess.query(Store).filter(Store.meal_opt_use == 'Y', Store.meal_opt_cancel_use == 'Y').all()
        for store in target_store:
            target_store_code = store.code

            today = D().today_str()
            target_order = sess.query(Order).filter(
                Order.store_code == target_store_code,
                Order.reg_date > f'{today} 00:00:00')

            for order in target_order:
                meal_payment = False

                if order.pg_info and order.pg_info.pg_info_sub:
                    sub_list: List[PgInfoSub] = order.pg_info.pg_info_sub
                    for sub in sub_list:
                        if sub.kind == '식권 쿠폰':
                            meal_payment = True
                            break

                if meal_payment:
                    ops: List[OrderProduct] = sess.query(OrderProduct).filter(OrderProduct.order_id == order.id).all()
                    cancel_able = True
                    if ops[0].type == 'DP' or ops[0].type == 'UP-OF':
                        for op in ops:
                            if op.status != 'PD':
                                cancel_able = False
                    if ops[0].type == 'UP-EC':
                        cancel_able = False
                    if cancel_able:
                        cancel(sess, order.id)
                    L().info(f'Canceled order {order.id}')



    db.shutdown()
    L().info(f'End')
