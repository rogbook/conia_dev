from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.schema import OrderProduct, SettlementRaw
from scripts.database.conn import db


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        # 타겟 주문 상품 데이터 조회
        target_orders = sess.query(OrderProduct).filter(OrderProduct.status == "CP", OrderProduct.settlement_date == None).all()

        for to in target_orders:
            raw = SettlementRaw()
            raw.target_date = func.current_date()
            raw.order_id = to.order_id
            raw.order_product_id = to.id
            raw.product_id = to.product_option.product_id
            raw.store_code = to.order.store_code
            raw.amount = to.amount
            if to.order.pg_info:
                raw.pg_type = to.order.pg_info.kind
            else:
                raw.pg_type = to.order.origin_order.pg_info.kind
            raw.supply_price = to.product_option.supply_price * to.ea
            raw.margin_price = to.amount - to.product_option.supply_price * to.ea
            sess.add(raw)

            # 타겟 주문 상품 데이터에 정산 처리일 입력
            to.update(sess, True, settlement_date=func.current_timestamp())

        sess.commit()

    db.shutdown()



