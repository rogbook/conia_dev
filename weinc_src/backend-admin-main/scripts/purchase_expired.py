import time

from sqlalchemy.orm import Session
from sqlalchemy import func
import openpyxl
import bcrypt
import pyotp

from app.common.consts import AES_KEY, AES_IV
from app.utils.crypto_utils import AES256
from app.utils.date_utils import D

from app.database.schema import OrderShipping, LogOrder, OrderProduct
from app.models.common import LogOrderDataIn
from scripts.database.conn import db
from app.utils.common_utils import log_msg

if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        targets = sess.query(OrderProduct).filter(
            OrderProduct.type.like("UP%"),
            OrderProduct.use_end_date != None,
            OrderProduct.use_end_date < func.current_timestamp(),
            OrderProduct.status == 'PD').all()

        for target in targets:
            target.status = 'EXP'

            # 로깅
            log_data = LogOrderDataIn(action="기한만료", order_id=target.order_id, msg=log_msg("msg", f"기한만료"), writer=f"시스템:{3}")
            LogOrder.create(sess, auto_commit=True, **log_data.dict())
        sess.commit()


    db.shutdown()



