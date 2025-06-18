import time

from sqlalchemy.orm import Session
import openpyxl

from app.database.schema import NoticeInfoTemplate
from scripts.database.conn import db


if __name__ == '__main__':

    wb = openpyxl.load_workbook("./data/V3_NOTICE_INFO.xlsx")
    ws = wb.active

    db.startup()

    sess: Session
    with db.session as sess:
        sess.execute('''SET foreign_key_checks = 0''')
        sess.commit()

        sess.execute('''TRUNCATE TABLE notice_info_template''')
        sess.commit()

        for row in ws.rows:
            if not row[0].value:
                break

            category = row[0].value
            item = row[1].value
            num: str = row[2].value
            print(f"{category} / {item}")
            created_data = NoticeInfoTemplate.create(session=sess, category=category ,item=item, num=num)
        sess.commit()

        sess.execute('''SET foreign_key_checks = 1''')
        sess.commit()

    db.shutdown()



