from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from app.utils.date_utils import D
from app.utils.common_utils import generate_random_string

from app.database.schema import Coupon, CouponGroup, CouponPublishTarget, MemberStore
from scripts.database.conn import db


def publishing_coupon(session: Session, group: CouponGroup, customer_id: int):
    data = Coupon()
    data.code = generate_random_string(10)
    data.name = group.name
    data.description = group.description

    if group.expire_days:
        dutil = D()
        data.begin_date = dutil.now_str()
        data.end_date = dutil.generate235959(dutil.add_day(group.expire_days))
    elif group.begin_time and group.end_time:
        now = datetime.now()
        data.begin_date = now.replace(hour=group.begin_time.hour, minute=group.begin_time.minute, second=group.begin_time.second)
        data.end_date = now.replace(hour=group.end_time.hour, minute=group.end_time.minute, second=group.end_time.second)
    else:
        data.begin_date = group.begin_date
        data.end_date = group.end_date

    data.amount = group.amount
    data.percent = group.percent

    data.min_price = group.min_price
    data.max_price = group.max_price

    data.issuer = group.issuer
    data.coupon_group_id = group.id
    data.target = group.target
    data.type = group.type
    data.customer_id = customer_id
    data.product_id = group.product_id

    session.add(data)


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        target_group = sess.query(CouponGroup).filter(CouponGroup.status == 'Y', CouponGroup.auto == '넷마블').all()

        for group in target_group:
            publish_targets: List[CouponPublishTarget] = group.coupon_publish_target

            success_cnt = 0
            target_store = []

            for publish_target in publish_targets:
                target_store.append(publish_target.store_code)
            target_customers = sess.query(MemberStore.customer_id).filter(MemberStore.store_code.in_(target_store)).distinct().all()

            if group.publish_limit:
                published_coupon_cnt = Coupon.filter(sess, coupon_group_id=group.id).count()
                if len(target_customers) > (group.publish_limit - published_coupon_cnt):
                    print(f'GROUP ID : {group.id} / 발행 매수 초과로 발행 중단')
                    continue

            try:
                for row in target_customers:
                    publishing_coupon(sess, group, row[0])
                    success_cnt += 1
                sess.commit()
            except Exception as e:
                sess.rollback()
                print(f'GROUP ID : {group.id} / 발행 오류')
                print(f'         -> {e.args}')
            print(f'GROUP ID : {group.id} / 정상 발행 {success_cnt}건')



    db.shutdown()



