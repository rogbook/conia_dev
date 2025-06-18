import os
from uuid import uuid4

from sqlalchemy.orm import Session

from app.common.consts import SETTLEMENT_STATUS, AWS_S3_BUCKET_IMG, AWS_S3_BUCKET_IMG_HOST
from app.utils.aws import S3
from app.utils.date_utils import D

from app.database.schema import Member, SettlementData, SettlementExcel, MemberClass
from app.models.settlement import ListData
from scripts.database.conn import db


def get_option_name(product_option):
    option_name = []
    po = product_option.__dict__
    for key, value in po.items():
        if value and len(key) == 8 and key[:7] == "option_" and key[-1].isdigit():
            option_name.append(value)
    return "/".join(option_name)


if __name__ == '__main__':

    db.startup()

    session: Session
    with db.session as session:
        target_list = session.query(SettlementExcel).filter(SettlementExcel.status == 'R').all()

        for target_row in target_list:
            target_row.status = 'P'
            session.commit()

            qry = session.query(SettlementData)

            if target_row.target_status:
                qry = qry.filter(SettlementData.status == target_row.target_status)

            if target_row.member_id:
                qry = qry.filter(SettlementData.member_id == target_row.member_id)

            if target_row.target_kind:
                qry = qry.filter(SettlementData.type == target_row.target_kind)
            else:
                qry = qry.filter(SettlementData.type != 'PG')

            if target_row.s_reg_date and target_row.e_reg_date:
                qry = qry.filter(SettlementData.reg_date.between(target_row.s_reg_date, D().make235959(target_row.e_reg_date)))
            elif target_row.s_reg_date:
                qry = qry.filter(SettlementData.reg_date > target_row.s_reg_date)
            elif target_row.e_reg_date:
                qry = qry.filter(SettlementData.reg_date < D().make235959(target_row.e_reg_date))

            datas = qry.all()

            if target_row.request_member == 1 or target_row.request_member == 2:
                is_cm = True
            else:
                is_cm = session.query(MemberClass).filter(MemberClass.class_code == 'CM', MemberClass.member_id == target_row.request_member).first()

            st_data = ListData(total=len(datas), datas=datas)

            if not st_data.total:
                target_row.status = 'E'
                session.commit()
                continue

            member = None
            if target_row.member_id:
                member = Member.get(session, id=target_row.member_id)

            import openpyxl

            file_name = f'{member.name}({member.company.name})-정산내역-{target_row.s_reg_date}_{target_row.e_reg_date}-{D.yyyymmdd()}-{uuid4().hex[:4]}.xlsx'
            file_path = os.path.join(os.getcwd(), 'files/', file_name)
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(['조회기간', f"{target_row.s_reg_date}_{target_row.e_reg_date}"])
            if member:
                sheet.append(['이름', member.name])
                sheet.append(['이메일', member.email])
                sheet.append(['업체명', member.company.name])

            sheet.append([''])
            sheet.append([''])

            pa_header = ["결제일", "구매확정일", "주문번호", "판매상정명(코드)", "상품명", "옵션", "수량", "핀번호(e쿠폰상품)", "공급가", "정산금액", "과세여부", "공급가액", "세액", "정산상태"]
            if is_cm:
                mc_header = ["결제일", "구매확정일", "주문번호", "판매상정명(코드)", "상품명", "옵션", "수량", "판매단가", "결제금액", "공급가", "정산금액", "정산상태"]
            else:
                mc_header = ["결제일", "구매확정일", "주문번호", "판매상정명(코드)", "상품명", "옵션", "수량", "판매단가", "결제금액", "정산금액", "정산상태"]

            if target_row.member_type and target_row.member_type == 'PA':
                sheet.append(pa_header)
                for row in st_data.datas:
                    sheet.append([row.account_raw.order_id[:8],
                                  row.account_raw.order_product.complete_date,
                                  row.account_raw.order_id,
                                  f"{row.account_raw.store.title}({row.account_raw.store_code})",
                                  row.account_raw.product.name,
                                  get_option_name(row.account_raw.order_product.product_option),
                                  row.account_raw.order_product.ea,
                                  row.account_raw.order_product.ecoupon.pin_code if row.account_raw.order_product.ecoupon else '',
                                  row.account_raw.supply_price,
                                  row.amount,
                                  row.tax,
                                  round(float(row.amount) / 1.1) if row.tax == 'Y' else int(row.amount),
                                  int(row.amount) - round(float(row.amount) / 1.1) if row.tax == 'Y' else 0,
                                  SETTLEMENT_STATUS.get(row.status)])

                    histories = session.query(SettlementData).filter(SettlementData.account_raw_id == row.account_raw_id).all()

            elif target_row.member_type and target_row.member_type == 'MC':
                sheet.append(mc_header)
                for row in st_data.datas:
                    if is_cm:
                        sheet.append([row.account_raw.order_id[:8],
                                      row.account_raw.order_product.complete_date,
                                      row.account_raw.order_id,
                                      f"{row.account_raw.store.title}({row.account_raw.store_code})",
                                      row.account_raw.product.name,
                                      get_option_name(row.account_raw.order_product.product_option),
                                      row.account_raw.order_product.ea,
                                      row.account_raw.order_product.product_option.selling_price,
                                      row.account_raw.amount,
                                      row.account_raw.supply_price,
                                      row.amount,
                                      SETTLEMENT_STATUS.get(row.status)])
                    else:
                        sheet.append([row.account_raw.order_id[:8],
                                      row.account_raw.order_product.complete_date,
                                      row.account_raw.order_id,
                                      f"{row.account_raw.store.title}({row.account_raw.store_code})",
                                      row.account_raw.product.name,
                                      get_option_name(row.account_raw.order_product.product_option),
                                      row.account_raw.order_product.ea,
                                      row.account_raw.order_product.product_option.selling_price,
                                      row.account_raw.amount,
                                      row.amount,
                                      SETTLEMENT_STATUS.get(row.status)])
            sheet.append([''])
            # if target_row.member_type and target_row.member_type == 'PA':
            #     sheet.append(['합계'])
            # elif target_row.member_type and target_row.member_type == 'MC':
            #     sheet.append(['합계'])
            wb.save(file_path)

            with open(file_path, 'rb') as file:
                s3 = S3()
                s3.s3.upload_fileobj(file, AWS_S3_BUCKET_IMG, f"settlement/excel/{file_name}")
                url: str = f"{AWS_S3_BUCKET_IMG_HOST}settlement/excel/{file_name}"
                target_row.file = url
                target_row.status = 'Y'
                session.commit()

            try:
                wb.close()
                os.remove(file_path)
            except:
                pass



    db.shutdown()
