import time

from sqlalchemy.orm import Session
import openpyxl

from app.database.schema import Brand
from scripts.database.conn import db


if __name__ == '__main__':

    wb = openpyxl.load_workbook("./data/V3_BRAND.xlsx")
    ws = wb.active

    db.startup()

    sess: Session
    with db.session as sess:
        sess.execute('''SET foreign_key_checks = 0''')
        sess.commit()

        sess.execute('''TRUNCATE TABLE brand''')
        sess.commit()

        for row in ws.rows:
            if not row[0].value:
                break

            name: str = row[0].value
            desc = row[1].value
            print(f"{name} / {desc}")
            if Brand.get(sess, name=name.strip()):
                continue
            created_data = Brand.create(session=sess, name=name.strip() ,description=desc)
        sess.commit()

        sess.execute('''SET foreign_key_checks = 1''')
        sess.commit()

    db.shutdown()



