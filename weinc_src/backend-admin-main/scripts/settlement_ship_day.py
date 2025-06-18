from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.schema import OrderShipping, SettlementShip, Commission
from scripts.database.conn import db


class FeeModel(BaseModel):
    type: str
    value: Decimal


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        # 타겟 주문 배송 데이터 조회
        targets = sess.query(OrderShipping).filter(OrderShipping.status == "DC", OrderShipping.settlement_date == None).all()

        for target in targets:
            if not target.order.pg_info:
                target.update(sess, True, settlement_date=func.current_timestamp())
                continue

            pg_provider = target.order.pg_info.provider
            pg_kind = target.order.pg_info.kind
            target_member = target.member_id

            # PG 수수료
            pg_fee = Commission.get(sess, target=1, pg_provider=pg_provider, pg_kind=pg_kind)

            raw = SettlementShip()
            raw.target_date = func.current_date()
            raw.order_id = target.order_id
            raw.order_shipping_id = target.id
            raw.store_code = target.order.store_code
            raw.type = 'PG'
            raw.sequence = 1
            raw.target_amount = target.cost
            raw.amount = int(target.cost * (pg_fee.value / Decimal(100.0)))
            raw.member_id = 1
            raw.commission_type = pg_fee.type
            raw.commission_value = pg_fee.value
            raw.pg_provider = target.order.pg_info.provider
            raw.pg_kind = target.order.pg_info.kind
            sess.add(raw)

            remain_cost = target.cost - int(target.cost * (pg_fee.value / Decimal(100.0)))

            # 코니아 수수료
            conia_fee = Commission.get(sess, target=1, default="N", member_id=target_member, kind='ship')
            if not conia_fee:
                conia_fee = Commission.get(sess, target=1, default="Y", kind='ship')

            sequence = 1
            if conia_fee:
                conia_data = SettlementShip()
                conia_data.target_date = func.current_date()
                conia_data.order_id = target.order_id
                conia_data.order_shipping_id = target.id
                conia_data.store_code = target.order.store_code
                conia_data.type = 'C'
                conia_data.sequence = sequence + 1
                conia_data.target_amount = remain_cost
                conia_data.amount = int(remain_cost * (conia_fee.value / Decimal(100.0)))
                conia_data.member_id = 1
                conia_data.commission_type = conia_fee.type
                conia_data.commission_value = conia_fee.value
                sess.add(conia_data)

                sequence = 2
                remain_cost = remain_cost - int(remain_cost * (conia_fee.value / Decimal(100.0)))

            # 공급자
            fee = FeeModel(type="P", value=Decimal(100.0))

            member_data = SettlementShip()
            member_data.target_date = func.current_date()
            member_data.order_id = target.order_id
            member_data.order_shipping_id = target.id
            member_data.store_code = target.order.store_code
            member_data.type = 'S'
            member_data.sequence = sequence + 1
            member_data.target_amount = remain_cost
            member_data.amount = remain_cost
            member_data.member_id = target_member
            member_data.commission_type = fee.type
            member_data.commission_value = fee.value
            sess.add(member_data)

            # 타겟 주문 상품 데이터에 정산 처리일 입력
            target.update(sess, True, settlement_date=func.current_timestamp())

        sess.commit()

    db.shutdown()



