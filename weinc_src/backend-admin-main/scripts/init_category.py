import time

from sqlalchemy.orm import Session
import openpyxl

from app.database.schema import Category, Member
from scripts.database.conn import db


if __name__ == '__main__':

    wb = openpyxl.load_workbook("./data/V3_CATEGORY.xlsx")
    ws = wb.active

    db.startup()

    sess: Session
    with db.session as sess:
        sess.execute('''SET foreign_key_checks = 0''')
        sess.commit()

        sess.execute('''TRUNCATE TABLE category''')
        sess.commit()

        top_dict = dict()
        middle_dict = dict()
        small_dict = dict()
        detail_dict = dict()

        count = 0

        for row in ws.rows:
            if not row[0].value:
                break
            count += 1
            print(count)

            top = row[1].value
            middle = row[2].value
            small = row[3].value
            detail = row[4].value

            # top_data = Category.get(sess, name=top)
            top_id = top_dict.get(top)
            if not top_id:
                top_data = Category.create(session=sess, name=top, depth=1, depth1_name=top)
                top_dict[top] = top_data.id
                top_id = top_data.id

            if middle:
                # middle_data = Category.get(sess, name=middle)
                middle_id = middle_dict.get(middle)
                if not middle_id:
                    middle_data = Category.create(session=sess, name=middle, pid=top_id, depth=2, depth1_name=top, depth1_id=top_id, depth2_name=middle)
                    middle_dict[middle] = middle_data.id
                    middle_id = middle_data.id

            if small:
                # small_data = Category.get(sess, name=small)
                small_id = small_dict.get(small)
                if not small_id:
                    small_data = Category.create(session=sess, name=small, pid=middle_id, depth=3, depth1_name=top, depth1_id=top_id, depth2_name=middle, depth2_id=middle_id, depth3_name=small)
                    small_dict[small] = small_data.id
                    small_id = small_data.id

            if detail:
                # detail_data = Category.get(sess, name=detail)
                detail_id = detail_dict.get(detail)
                if not detail_id:
                    Category.create(session=sess, name=detail, pid=small_id, depth=4, depth1_name=top, depth1_id=top_id, depth2_name=middle, depth2_id=middle_id, depth3_name=small, depth3_id=small_id, depth4_name=detail)

        sess.commit()


        sess.execute('''SET foreign_key_checks = 1''')
        sess.commit()

    db.shutdown()



