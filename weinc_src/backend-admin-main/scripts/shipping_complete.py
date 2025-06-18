from sqlalchemy.orm import Session
from app.utils.date_utils import D

from app.database.schema import OrderShipping, LogOrder
from app.models.common import LogOrderDataIn
from scripts.database.conn import db
from app.utils.common_utils import log_msg

if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        targets = sess.query(OrderShipping).filter(OrderShipping.status == 'DN', OrderShipping.number_reg_date != None, OrderShipping.number_reg_date <= D().add_day(-3)).all()

        for target in targets:
            target.status = 'DC'
            target.complete_date = D().now

            # 로깅
            log_data = LogOrderDataIn(action="배송완료", order_id=target.order_id, msg=log_msg("msg", f"자동 배송완료"), writer=f"시스템:{3}")
            LogOrder.create(sess, auto_commit=True, **log_data.dict())
        sess.commit()


    db.shutdown()



