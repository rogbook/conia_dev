# 일일 재고 처리
from typing import List

from app.database.schema import *
from app.utils.date_utils import D
from scripts.util.log import mongo_log
from scripts.database.conn import db

if __name__ == '__main__':
    print(f"START {D().now_str()}")
    db.startup()
    yesterday = D().yesterday_str()

    sess: Session
    with db.session as sess:
        change_count = 0
        target_prd_inven_list: List[Inventory] = sess.query(Inventory).join(ProductOption, ProductOption.id == Inventory.product_option_id).filter(Inventory.day_able_count != None, Inventory.day_able_count != 0, ProductOption.status == 'Y').all()
        print(f"CHECK LIST COUNT : {len(target_prd_inven_list)}")
        for target_prd_inven in target_prd_inven_list:
            day_able_count = target_prd_inven.day_able_count
            if target_prd_inven.use_acc_qty == 'Y':
                not_use_cnt = sess.query(OrderProduct).filter(OrderProduct.status == "PD", OrderProduct.product_option_id == target_prd_inven.product_option_id).count()
                new_count = day_able_count - not_use_cnt
            else:
                new_count = day_able_count

            if target_prd_inven.count != new_count:
                change_count += 1
                option_name = []
                po = target_prd_inven.option.__dict__
                for key, value in po.items():
                    if value and len(key) == 8 and key[:7] == "option_" and key[-1].isdigit():
                        option_name.append(value)
                product_option_name = "/".join(option_name)

                log_data = {
                    "product_name": target_prd_inven.option.product.name,
                    "product_code": target_prd_inven.option.product.code,
                    "product_id": target_prd_inven.option.product.id,
                    "opt_id": target_prd_inven.option.id,
                    "opt_name": product_option_name,
                    "before_count": target_prd_inven.count,
                    "after_count": new_count,
                    "before_status": target_prd_inven.option.product.status,
                    "after_status": '',
                    "use_acc_qty": target_prd_inven.use_acc_qty,
                }

                target_prd_inven.count = new_count

                if target_prd_inven.count > 0 and target_prd_inven.option.product.status == 'S':
                    target_prd_inven.option.product.status = 'Y'
                    log_data.update(after_status="Y")

                mongo_log("log-day-inventory", log_data)
            else:
                continue

        sess.commit()
    print(f"CHANGE COUNT : {change_count}")
    db.shutdown()
    print(f"END {D().now_str()}")