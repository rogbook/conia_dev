from sqlalchemy.orm import Session
from sqlalchemy import cast, Date, func
from app.database.conn import db
from app.database import schema as s


class Auth:
    def __init__(self):
        ...

    @staticmethod
    def get_cert_sms_count(session: Session = None, **kwargs):
        sess = next(db.session()) if not session else session

        cnt: int = 0

        if "mobile" in kwargs:
            cnt = sess.query(s.CertSms).filter(s.CertSms.type == "CERT_SMS",
                                               s.CertSms.mobile == kwargs.get("mobile"),
                                               cast(s.CertSms.reg_date, Date) == func.current_date()).count()
        elif "ip" in kwargs:
            cnt = sess.query(s.CertSms).filter(s.CertSms.type == "CERT_SMS",
                                               s.CertSms.ip == kwargs.get("ip"),
                                               cast(s.CertSms.reg_date, Date) == func.current_date()).count()
        if not session:
            sess.close()

        return cnt
