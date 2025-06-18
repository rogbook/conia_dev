from sqlalchemy.orm import Session
from app.utils.date_utils import D
from app.utils.aws import SES

from app.database.schema import EmailHistory
from scripts.database.conn import db

if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        targets = sess.query(EmailHistory).filter(EmailHistory.status == 'R', EmailHistory.res_date < D().now_str()).all()

        for target in targets:
            target.status = 'P'
        sess.commit()

        ses = SES()
        for target in targets:
            ses.send_email(to=target.to, subject=target.title, message=target.body)
            target.status = 'Y'

        sess.commit()


    db.shutdown()



