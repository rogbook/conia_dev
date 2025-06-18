# 일일 주문서 정리 스크립트

from app.database.schema import *
from app.utils.date_utils import D
from scripts.database.conn import db

if __name__ == '__main__':

    db.startup()
    yesterday = D().yesterday_str()

    sess: Session
    with db.session as sess:
        sess.query(OrderSheet).filter(OrderSheet.reg_date < yesterday).delete()
        sess.commit()

    db.shutdown()