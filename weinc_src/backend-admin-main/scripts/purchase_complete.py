from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.date_utils import D

from app.database.schema import OrderShipping, LogOrder, OrderProduct
from app.models.common import LogOrderDataIn
from scripts.database.conn import db
from app.utils.common_utils import log_msg

if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        targets = sess.query(OrderProduct).outerjoin(OrderShipping, OrderProduct.order_shipping_id == OrderShipping.id).filter(
            OrderProduct.type == 'DP',
            OrderProduct.complete_date == None,
            OrderProduct.order_shipping_id != None,
            OrderShipping.complete_date <= D().add_day(-7),
            OrderProduct.status.notin_(['RFR', 'RFN', 'RFC', 'EXR', 'EXN', 'EXC'])).all()

        for target in targets:
            target.status = 'CP'
            target.complete_date = func.current_timestamp()

            # 로깅
            log_data = LogOrderDataIn(action="구매확정", order_id=target.order_id, msg=log_msg("msg", f"자동 구매확정"), writer=f"시스템:{3}")
            LogOrder.create(sess, auto_commit=True, **log_data.dict())
        sess.commit()


    db.shutdown()



