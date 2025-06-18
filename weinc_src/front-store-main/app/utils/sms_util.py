from sqlalchemy.orm import Session
from fastapi import Request

from app.common.consts import AES_KEY, AES_IV
from app.database.schema import SmsHistory, Customer, Store
from app.utils.crypto_utils import AES256
from app.utils.common_utils import get_base_url
from app.utils.sms import SMS


def add_history(session: Session, member: Customer, msg, mid, store_code, order_id=None):
    sh = SmsHistory()
    sh.type = 'system'
    sh.mobile = member.mobile
    sh.body = msg
    sh.mid = mid
    sh.provider = ''
    sh.customer_id = member.id
    sh.store_code = store_code
    if order_id:
        sh.order_id = order_id
    session.add(sh)
    session.commit()


def make_bottom_msg(req: Request, store: Store):
    msg = f"""
▶몰 바로가기
{get_base_url(req)}{store.code}
▶카카오톡 채널 : CS상담문의
https://pf.kakao.com/_xhlKxcxj/chat
"""
    return msg


def send_sms(session: Session, member: Customer, store: Store, msg, order_id=None):
    sms = SMS()
    try:
        mobile = AES256(AES_KEY, AES_IV).decrypt(member.mobile)
        res = sms.send(mobile, msg)

        if res.get('mid'):
            add_history(session, member, msg, res.get('mid'), store.code, order_id)
    except Exception as e:
        print(e.args)
