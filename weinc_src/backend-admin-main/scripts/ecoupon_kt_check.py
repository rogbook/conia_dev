import time

from sqlalchemy.orm import Session

from app.database.schema import Product, LogProduct
from scripts.database.conn import db

from app.utils.ecoupon_kt import EcounponKt
from app.utils.common_utils import log_msg
from app.models.common import LogProductDataIn


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        kt = EcounponKt()
        res_goods = kt.goods()
        able_target = []
        for goods in res_goods.goodsList:
            able_target.append(goods.goodsCd)

        prd_list = sess.query(Product).filter(Product.type =='UP-EC', Product.api_provider == 'KT').all()

        for prd in prd_list:
            log_data = None
            if prd.status == 'Y' and prd.api_goods_id not in able_target:
                prd.status = 'N'
                log_data = LogProductDataIn(action="상태 변경", product_id=prd.id, msg=log_msg("msg", f"미승인 처리(KT API)"), writer=f"시스템:3")

            # if prd.status == 'S' and prd.api_goods_id in able_target:
            #     prd.status = 'Y'
            #     log_data = LogProductDataIn(action="상태 변경", product_id=prd.id, msg=log_msg("msg", f"품절 복원 처리(KT API)"), writer=f"시스템:3")

            if log_data:
                sess.commit()
                LogProduct.create(sess, auto_commit=True, **log_data.dict())

    db.shutdown()
