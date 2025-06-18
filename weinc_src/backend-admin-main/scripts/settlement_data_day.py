from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.schema import OrderProduct, SettlementRaw, SettlementData, Store, MemberMember, Commission, Order
from scripts.database.conn import db


class FeeModel(BaseModel):
    type: str
    value: Decimal
    payment: str = None


def get_parent_members(parent_list, child_id):
    parent_member = MemberMember.get(sess, member_id=child_id)

    if parent_member:
        parent_list.append(parent_member.pid)
        get_parent_members(parent_list, parent_member.pid)


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        # 정산 대상 데이터 조회
        raws = sess.query(SettlementRaw).filter(SettlementRaw.processed == None).all()

        for raw in raws:
            store = Store.get(sess, code=raw.store_code)
            # 판매자
            store_owner_id = store.member_id

            order = Order.get(sess, id=raw.order_id)
            order_product = OrderProduct.get(sess, id=raw.order_product_id)

            # 상품
            product = order_product.product_option.product
            # 상품 공급자
            product_owner_id = product.member_id
            # 상품 사입 여부
            product_resale = product.resale
            # 과세 여부
            tax = product.tax

            # 계층 구조 회원 목록
            fee_target_list = [store_owner_id]
            get_parent_members(fee_target_list, store_owner_id)
            fee_target_list.reverse()

            sequence = 0

            # 정산 대상
            # 1. PG 수수료
            # 2. 상품 공급자 중계인
            # 3. 상품 공급자
            # 4. 코니아
            # 5. 판매 채널 계층 구조 및 중계인

            if order.pg_info:
                pg_provider = order.pg_info.provider
                pg_kind = order.pg_info.kind
            else:
                pg_provider = order.origin_order.pg_info.provider
                pg_kind = order.origin_order.pg_info.kind

            pg_fee = Commission.get(sess, target=1, pg_provider=pg_provider, pg_kind=pg_kind)

            if not pg_fee:
                pg_fee = Commission.get(sess, target=1, pg_provider=pg_provider)

            if pg_fee.type == 'P':
                pg_amount = int(raw.amount * (pg_fee.value / Decimal(100.0)))
            else:
                pg_amount = int(pg_fee.value)

            # PG 수수료
            sequence += 1
            pg_data = SettlementData()
            pg_data.target_date = func.current_timestamp()
            pg_data.account_raw_id = raw.id
            pg_data.member_id = 1
            pg_data.type = "PG" # PG 수수료
            pg_data.sequence = sequence
            pg_data.target_amount = raw.amount
            pg_data.amount = pg_amount
            pg_data.commission_type = pg_fee.type
            pg_data.commission_value = pg_fee.value
            pg_data.pg_provider = pg_provider
            pg_data.pg_kind = pg_kind
            pg_data.tax = tax
            sess.add(pg_data)

            remain_margin = raw.amount - pg_amount

            supply_amount = raw.supply_price
            origin_supply_amount = raw.supply_price

            # 상품 공급자 중계인
            product_brokers = sess.query(Commission).filter(Commission.member_id == product_owner_id).all()
            for broker in product_brokers:
                if broker.store_code and raw.store_code != broker.store_code:
                    continue

                if broker.product_id and raw.product_id != broker.product_id:
                    continue

                sequence += 1

                if broker.type == "P":
                    if supply_amount <= 0:
                        broker_amount = 0
                    else:
                        broker_amount = int(raw.supply_price * (broker.value / Decimal(100.0)))
                else:
                    if broker.payment == 'D':
                        if supply_amount <= 0:
                            broker_amount = 0
                        elif (supply_amount - broker.value) <= 0:
                            broker_amount = int(supply_amount)
                        else:
                            broker_amount = int(broker.value)
                    else:
                        broker_amount = int(broker.value)

                broker_data = SettlementData()
                broker_data.target_date = func.current_timestamp()
                broker_data.account_raw_id = raw.id
                broker_data.member_id = broker.target
                broker_data.type = "SC" # 공급가 수수료
                broker_data.commission_type = broker.type
                broker_data.commission_value = broker.value
                broker_data.sequence = sequence
                broker_data.target_amount = raw.supply_price
                broker_data.amount = broker_amount
                broker_data.tax = tax
                broker_data.payment = broker.payment
                sess.add(broker_data)

                if broker.payment == 'D': # 이익 차감
                    supply_amount = supply_amount - broker_amount
                else:
                    remain_margin = remain_margin - broker_amount # 분리 지급

            # 상품 공급자
            if product_resale == 'Y':
                sequence += 1
                supply_data = SettlementData()
                supply_data.target_date = func.current_timestamp()
                supply_data.account_raw_id = raw.id
                supply_data.member_id = 1
                supply_data.type = "S" # 공급가
                supply_data.commission_type = 'F'
                supply_data.sequence = sequence
                supply_data.target_amount = supply_amount
                supply_data.amount = supply_amount
                supply_data.tax = tax
                sess.add(supply_data)

                supply_data = SettlementData()
                supply_data.target_date = func.current_timestamp()
                supply_data.account_raw_id = raw.id
                supply_data.member_id = product_owner_id
                supply_data.type = "S" # 공급가
                supply_data.commission_type = 'F'
                supply_data.sequence = sequence
                supply_data.target_amount = 0
                supply_data.amount = 0
                supply_data.tax = tax
                sess.add(supply_data)
            else:
                sequence += 1
                supply_data = SettlementData()
                supply_data.target_date = func.current_timestamp()
                supply_data.account_raw_id = raw.id
                supply_data.member_id = product_owner_id
                supply_data.type = "S"  # 공급가
                supply_data.commission_type = 'F'
                supply_data.sequence = sequence
                supply_data.target_amount = supply_amount
                supply_data.amount = supply_amount
                supply_data.tax = tax
                sess.add(supply_data)

            remain_margin = remain_margin - origin_supply_amount

            # 코니아 수수료
            conia_fee = Commission.filter(sess, target=1, default="N", product_id=raw.product_id).first()
            if not conia_fee:
                conia_fee = Commission.filter(sess, target=1, default="N", store_code=raw.store_code).first()
            if not conia_fee:
                conia_fee = Commission.filter(sess, target=1, default="Y", kind='prd').first()

            if conia_fee.type == "P":
                conia_amount = int(remain_margin * (conia_fee.value / Decimal(100.0)))
            else:
                if conia_fee.payment == 'D':
                    if (remain_margin - conia_fee.value) <= 0:
                        conia_amount = int(remain_margin)
                else:
                    conia_amount = int(conia_fee.value)

            # 코니아
            if conia_fee:
                sequence += 1
                conia_data = SettlementData()
                conia_data.target_date = func.current_timestamp()
                conia_data.account_raw_id = raw.id
                conia_data.member_id = 1
                conia_data.type = "MC" # 마진 수수료
                conia_data.sequence = sequence
                conia_data.target_amount = remain_margin
                conia_data.amount = conia_amount
                conia_data.commission_type = conia_fee.type
                conia_data.commission_value = conia_fee.value
                conia_data.tax = tax
                sess.add(conia_data)

            remain_margin = remain_margin - conia_amount

            # 판매 채널 계층 구조
            for i, target in enumerate(fee_target_list, start=1):
                # 판매 채널 수수료
                fee = Commission.get(sess, target=target, default="N", product_id=raw.product_id)
                if not fee:
                    fee = Commission.get(sess, target=target, default="N", store_code=raw.store_code)
                if not fee:
                    fee = Commission.get(sess, target=target, default="Y", kind='prd')

                if i == len(fee_target_list):
                    fee = FeeModel(type="P", value=Decimal(100.0))

                if fee:
                    origin_remain_margin = remain_margin
                    if fee.type == 'P':
                        seller_margin = int(remain_margin * (fee.value / Decimal(100.0)))
                    else:
                        if broker.payment == 'D':
                            if (remain_margin - seller_margin) <= 0:
                                seller_margin = int(remain_margin)
                        else:
                            seller_margin = int(fee.value)
                    broker_total_margin = 0

                    # 판매 채널 중계인
                    seller_brokers = sess.query(Commission).filter(Commission.member_id == target).all()
                    for broker in seller_brokers:
                        if broker.store_code and raw.store_code != broker.store_code:
                            continue

                        if broker.product_id and raw.product_id != broker.product_id:
                            continue

                        sequence += 1

                        if broker.type == "P":
                            if broker.payment == 'D':
                                if seller_margin <= 0:
                                    broker_amount = 0
                                else:
                                    broker_amount = int(seller_margin * (broker.value / Decimal(100.0)))
                            else:
                                broker_amount = int(seller_margin * (broker.value / Decimal(100.0))) if seller_margin > 0 else 0
                        else:
                            if broker.payment == 'D':
                                if seller_margin <= 0:
                                    broker_amount = 0
                                elif (seller_margin - broker.value) <= 0:
                                    broker_amount = int(seller_margin)
                                else:
                                    broker_amount = int(broker.value)
                            else:
                                broker_amount = int(broker.value)

                        broker_data = SettlementData()
                        broker_data.target_date = func.current_timestamp()
                        broker_data.account_raw_id = raw.id
                        broker_data.member_id = broker.target
                        broker_data.type = "MCC" # 마진 수수료 중계 수수료
                        broker_data.commission_type = broker.type
                        broker_data.commission_value = broker.value
                        broker_data.sequence = sequence
                        broker_data.target_amount = seller_margin
                        broker_data.amount = broker_amount
                        broker_data.tax = tax
                        broker_data.payment = broker.payment
                        sess.add(broker_data)

                        if broker.payment == 'D':
                            broker_total_margin = broker_total_margin + broker_amount  # 이익 차감
                        else:
                            remain_margin = remain_margin - broker_amount  # 분리 지급

                    if origin_remain_margin != remain_margin:
                        if fee.type == 'P':
                            seller_margin = int(remain_margin * (fee.value / Decimal(100.0)))
                        else:
                            if broker.payment == 'D':
                                if (remain_margin - seller_margin) <= 0:
                                    seller_margin = int(remain_margin)
                            else:
                                seller_margin = int(fee.value)

                    sequence += 1

                    # 판매 채널
                    member_data = SettlementData()
                    member_data.target_date = func.current_timestamp()
                    member_data.account_raw_id = raw.id
                    member_data.member_id = target
                    member_data.type = "MC" # 마진 수수료
                    member_data.sequence = sequence
                    member_data.target_amount = origin_remain_margin
                    member_data.amount = seller_margin - broker_total_margin
                    member_data.commission_type = fee.type
                    member_data.commission_value = fee.value
                    member_data.tax = tax
                    member_data.payment = fee.payment
                    sess.add(member_data)

                    remain_margin = remain_margin - seller_margin

            # 정산 대상 데이터에 처리일 입력
            raw.update(sess, True, processed=func.current_timestamp())
            sess.commit()


    db.shutdown()



