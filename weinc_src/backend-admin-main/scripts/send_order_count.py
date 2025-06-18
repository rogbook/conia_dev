from sqlalchemy.orm import Session
from sqlalchemy import or_
from dataclasses import asdict

from scripts.database.conn import SQLAlchemy
from app.common.config import conf
from app.database.schema import OrderProduct, Member
from app.utils.sms_util import send_sms_member


if __name__ == '__main__':

    c = conf()
    conf_dict = asdict(c)
    db = SQLAlchemy(**conf_dict)

    db.startup()

    session: Session
    with db.session as session:
        ops = session.query(OrderProduct).filter(or_(OrderProduct.status == 'PD', OrderProduct.status == 'DW'), OrderProduct.type == 'DP').all()
        suppliers = {}
        for op in ops:
            target = suppliers.get(op.member_id)
            if target is None:
                suppliers[op.member_id] = [op]
            else:
                suppliers[op.member_id].append(op)

        for k, v in suppliers.items():
            member = Member.get(session, id=k)

            if member.mobile:
                name = member.name
                if member.company:
                    name = member.company.name

                msg = f"""안녕하세요 [{name}]님!
코니아입니다.

배송이 필요한 주문이 [{len(v)}]건 있습니다.
상품이 준비되는데로 빠른 발송 부탁드립니다.

상품의 입고가 지연,품절 된 경우 고객에게 빠른 안내 부탁드립니다. 

문자수신 시간의 실제 주문 건수와 상이할 수 있습니다.

오늘도 기분 좋은 하루 보내세요!
감사합니다.

- CONIA -

관리자 로그인 :https://admin.coniaworld.com
문의(카카오톡) : https://pf.kakao.com/_dxixmdb
"""
                send_sms_member(session, member, msg)

    db.shutdown()
