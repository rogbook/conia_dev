import time
from uuid import uuid4
from decimal import Decimal

from sqlalchemy.orm import Session
import openpyxl
import bcrypt
import pyotp

from app.common.consts import AES_KEY, AES_IV
from app.utils.crypto_utils import AES256
from app.utils.date_utils import D
from app.utils.common_utils import log_msg

from app.database.schema import Member, Product, Category, ProductCategory, Brand, ProductBrand, ProductOption, CommonInfo, Inventory, LogProduct
from app.models.common import LogProductDataIn
from scripts.database.conn import db, c

if __name__ == '__main__':

    wb = openpyxl.load_workbook("./data/12345")
    ws = wb.active

    db.startup()

    sess: Session
    with db.session as sess:
        fail_list = []
        for idx, row in enumerate(ws.rows):
            print(f"Processing row {idx}")

            if not row[0].value:
                break
            if row[0].value == '상품유형':
                continue

            if row[0].value not in ["DP", "UP-EC", "UP-OF"]:
                print(f"Product type not found | {row[0].value}")
                fail_list.append(idx)
                continue

            member = Member.get(sess, email=row[1].value)
            if not member:
                print(f"Member not found | {row[1].value}")
                fail_list.append(idx)
                continue

            cate1 = None
            if row[1].value:
                cate1 = Category.get(sess, name=row[2].value)

            cate2 = None
            if row[2].value:
                cate2 = Category.get(sess, name=row[3].value, depth1_name=row[2].value)

            cate3 = None
            if row[3].value:
                cate3 = Category.get(sess, name=row[4].value, depth1_name=row[2].value, depth2_name=row[3].value)

            cate4 = None
            if row[4].value:
                cate4 = Category.get(sess, name=row[5].value, depth1_name=row[2].value, depth2_name=row[3].value, depth3_name=row[4].value)

            brand = None
            if row[6].value:
                brand = Brand.get(sess, name=row[6].value)

            product_name = str(row[7].value).strip()
            product_ori_price = str(row[8].value).replace(',', '')
            product_supply_price = str(row[9].value).replace(',', '')
            product_price = str(row[10].value).replace(',', '')

            inventory = None
            if row[11].value:
                inventory = int(row[11].value)

            product = Product()
            product.member_id = member.id
            product.name = product_name
            product.type = row[0].value
            product.status = "N"
            product.view_yn = "N"
            product.code = f"CP{D.yyyymmdd()[2:]}{uuid4().hex[:8]}"
            # product.summary = ""
            # product.keyword = ""
            # product.contents = ""
            product.tax = "Y"
            # product.min_purchase_limit = ""
            # product.max_purchase_limit = ""
            # product.adult = ""
            # product.hscode = ""
            # product.ipcc_yn = ""
            product.cancel_yn = "Y"
            # product.confirm = ""
            # product.video = ""
            # product.memo = ""
            product.common_info_id = None
            # product.shipping_info_id = ""
            product.writer_id = 3
            if inventory:
                product.inven_use = "Y"
            else:
                product.inven_use = "N"
            # product.coupon_yn = ""
            product.option_use = "N"
            # product.barcode = ""
            # product.user_limit = ""
            # product.use_end_period = ""
            # product.use_end_date = ""
            # product.sale_start_date = ""
            # product.sale_end_date = ""
            # product.sale_start_time = ""
            # product.sale_end_time = ""
            # product.tel = ""
            # product.address = ""
            # product.address_detail = ""
            # product.lat = ""
            # product.lng = ""
            # product.subtitle = ""
            # product.view_inventory = ""
            # product.view_end_time = ""

            if row[0].value == 'UP-EC':
                product.api_provider = 'KT'
                if row[12].value:
                    product.api_goods_id = row[12].value

            sess.add(product)
            sess.commit()

            opt = ProductOption()
            opt.supply_price = Decimal(product_supply_price)
            opt.origin_price = Decimal(product_ori_price)
            opt.selling_price = Decimal(product_price)
            # opt.view_yn = ''
            opt.default_yn = 'Y'
            opt.product_id = product.id
            opt.weight = 0
            # opt.status =
            sess.add(opt)
            sess.commit()

            inven_data = {
                "count": inventory if inventory else 0,
                "safe_count": 0,
                "product_option_id": opt.id,
            }
            Inventory.create(sess, **inven_data)

            if cate1:
                mapping_data = {
                    "product_id": product.id,
                    "category_id": cate1.id,
                }
                ProductCategory.create(session=sess, auto_commit=True, **mapping_data)

            if cate2:
                mapping_data = {
                    "product_id": product.id,
                    "category_id": cate2.id,
                }
                ProductCategory.create(session=sess, auto_commit=True, **mapping_data)

            if cate3:
                mapping_data = {
                    "product_id": product.id,
                    "category_id": cate3.id,
                }
                ProductCategory.create(session=sess, auto_commit=True, **mapping_data)

            if cate4:
                mapping_data = {
                    "product_id": product.id,
                    "category_id": cate4.id,
                }
                ProductCategory.create(session=sess, auto_commit=True, **mapping_data)

            if brand:
                mapping_data = {
                    "product_id": product.id,
                    "brand_id": brand.id,
                }
                ProductBrand.create(session=sess, auto_commit=True, **mapping_data)

            log_data = LogProductDataIn(action="등록", product_id=product.id, msg=log_msg("msg", "상품 엑셀 일괄 등록"), writer=f"시스템:{product.writer_id}")
            LogProduct.create(sess, auto_commit=True, **log_data.dict())
        if fail_list:
            print(f"FAIL LIST: {fail_list}")

    db.shutdown()
