from sqlalchemy.orm import Session
from fastapi import Request

from app.common.consts import AES_KEY, AES_IV
from app.common.config import conf
from app.database.schema import SmsHistory, Customer, Store, Member
from app.utils.crypto_utils import AES256
from app.utils.sms import SMS


def add_history_customer(session: Session, member: Customer, msg, mid, store_code):
    sh = SmsHistory()
    sh.type = 'system'
    sh.mobile = member.mobile
    sh.body = msg
    sh.mid = mid
    sh.provider = ''
    sh.customer_id = member.id
    sh.store_code = store_code
    session.add(sh)
    session.commit()


def add_history_member(session: Session, member: Member, msg, mid):
    sh = SmsHistory()
    sh.type = 'system'
    sh.mobile = member.mobile
    sh.body = msg
    sh.mid = mid
    sh.provider = ''
    sh.member_id = member.id
    session.add(sh)
    session.commit()


def make_bottom_msg(req: Request, store: Store):
    c = conf()
    msg = f"""
▶몰 바로가기
{c.STORE_HOST}/{store.code}
▶카카오톡 채널 : CS상담문의
https://pf.kakao.com/_xhlKxcxj/chat
"""
    return msg


def send_sms_customer(session: Session, member: Customer, store: Store, msg):
    sms = SMS()
    try:
        mobile = AES256(AES_KEY, AES_IV).decrypt(member.mobile)
        res = sms.send(mobile, msg)

        if res.get('mid'):
            add_history_customer(session, member, msg, res.get('mid'), store.code)
    except Exception as e:
        print(e.args)


def send_sms_member(session: Session, member: Member, msg):
    sms = SMS()
    try:
        mobile = AES256(AES_KEY, AES_IV).decrypt(member.mobile)
        res = sms.send(mobile, msg)

        if res.get('mid'):
            add_history_member(session, member, msg, res.get('mid'))
    except Exception as e:
        print(e.args)
