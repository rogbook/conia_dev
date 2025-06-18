import os
from datetime import date, datetime, timedelta
from typing import List, Optional

import openpyxl
from fastapi import APIRouter, Depends, Security, Query, Form, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.conn import db
from app.database.schema import RevenueOffline, OrderProduct, Order
from app.errors import exceptions as exc
from app.models.auth import MemberToken
from app.models.common import Success
from app.models.revenue import DataMonth, DataRevenue, ListOfflineRevenue
from app.utils.date_utils import D
from app.utils.jwt import token_user

router = APIRouter(prefix='/revenue')


@router.post("/offline", response_model=Success, name="오프라인 매출 등록 Excel")
async def add_offline(code: str = Form(default=None, description="코드"),
                      excel_file: UploadFile = File(description="엑셀 파일"),
                      session: Session = Depends(db.session),
                      user: MemberToken = Security(token_user, scopes=["write:revenue_offline"])):
    allowed_extensions = {'xlsx'}
    if not ('.' in excel_file.filename and excel_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        raise exc.NotAllowedFileEx

    file_path = os.path.join(os.getcwd(), 'app/upload/', f'RevenueOffline-{D.now_str_trim()}.xlsx')

    with open(file_path, 'wb') as buffer:
        buffer.write(await excel_file.read())

    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    try:
        for row in ws.rows:
            row_a = row[0].value
            if not row_a:
                break

            if not str(row[0].value).isdigit():
                continue

            if row[11].value == '승인거절':
                continue

            # if not str(row[0].value).isdigit():
            #     raise exc.BadRequestEx(reason='매출일 오류')

            if not is_number(str(row[13].value)):
                raise exc.BadRequestEx(reason='금액 오류')

            data = RevenueOffline()
            data.code = code
            data.amount = row[13].value
            data.sales_date = row[5].value
            data.member_id = user.id
            session.add(data)

        try:
            session.commit()
        except Exception as e:
            raise exc.BadRequestEx(reason='데이터베이스 입력 오류')

    finally:
        try:
            wb.close()
            os.remove(file_path)
        except:
            pass

    return Success()


@router.get("/offline", response_model=ListOfflineRevenue, name="오프라인 매출 목록")
def list_offline(code: Optional[str] = Query(default=None, description="코드"),
                 s_sales_date: Optional[date] = Query(default=None, description="매출일 시작"),
                 e_sales_date: Optional[date] = Query(default=None, description="매출일 종료"),
                 s_reg_date: Optional[date] = Query(default=None, description="등록일 시작"),
                 e_reg_date: Optional[date] = Query(default=None, description="등록일 종료"),
                 offset: int = 0, limit: int = 20,
                 session: Session = Depends(db.session),
                 user: MemberToken = Security(token_user, scopes=["read:revenue_offline"])):
    qry = session.query(RevenueOffline)
    sum_qry = session.query(func.sum(RevenueOffline.amount))

    if code:
        qry = qry.filter(RevenueOffline.code == code)
        sum_qry = sum_qry.filter(RevenueOffline.code == code)

    if s_sales_date and e_sales_date:
        qry = qry.filter(RevenueOffline.sales_date.between(s_sales_date, D().make235959(e_sales_date)))
        sum_qry = sum_qry.filter(RevenueOffline.sales_date.between(s_sales_date, D().make235959(e_sales_date)))
    elif s_sales_date:
        qry = qry.filter(RevenueOffline.sales_date > s_sales_date)
        sum_qry = sum_qry.filter(RevenueOffline.sales_date > s_sales_date)
    elif e_sales_date:
        qry = qry.filter(RevenueOffline.sales_date < D().make235959(e_sales_date))
        sum_qry = sum_qry.filter(RevenueOffline.sales_date < D().make235959(e_sales_date))

    if s_reg_date and e_reg_date:
        qry = qry.filter(RevenueOffline.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
        sum_qry = sum_qry.filter(RevenueOffline.reg_date.between(s_reg_date, D().make235959(e_reg_date)))
    elif s_reg_date:
        qry = qry.filter(RevenueOffline.reg_date > s_reg_date)
        sum_qry = sum_qry.filter(RevenueOffline.reg_date > s_reg_date)
    elif e_reg_date:
        qry = qry.filter(RevenueOffline.reg_date < D().make235959(e_reg_date))
        sum_qry = sum_qry.filter(RevenueOffline.reg_date < D().make235959(e_reg_date))

    total = qry.count()
    total_sum = sum_qry.scalar()
    datas = qry.offset(offset).limit(limit).all()

    return ListOfflineRevenue(total=total, total_sum=total_sum, data=datas)


@router.put("/offline/{target_id}", response_model=Success, name="오프라인 매출 상태 수정")
def mod_offline(target_id: int,
                status: str,
                session: Session = Depends(db.session),
                user: MemberToken = Security(token_user, scopes=["write:revenue_offline"])):
    data: RevenueOffline = RevenueOffline.get(session=session, id=target_id)
    if not data:
        raise exc.NotFoundDataEx

    data.update_optional(session=session, auto_commit=True, status=status, member_id=user.id)

    return Success()


@router.get("/month", response_model=DataMonth, name="월별 매출")
async def list_month(year: int = Query(description="년"),
                     month: int = Query(description="월"),
                     session: Session = Depends(db.session),
                     user: MemberToken = Security(token_user, scopes=["read:revenue_month"])):
    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=31)

    offline_qry = session.query(func.date(RevenueOffline.sales_date).label('date'), func.sum(RevenueOffline.amount).label('total_sales'))
    offline_qry = offline_qry.filter(RevenueOffline.sales_date >= start_date)
    offline_qry = offline_qry.filter(RevenueOffline.sales_date < end_date)
    offline_qry = offline_qry.group_by(func.date(RevenueOffline.sales_date))
    offline_data = offline_qry.all()
    offline_list = [DataRevenue.from_orm(row) for row in offline_data]

    online_qry = session.query(func.date(Order.reg_date).label('date'), func.sum(OrderProduct.amount).label('total_sales')).join(Order, OrderProduct.order_id == Order.id)
    online_qry = online_qry.filter(OrderProduct.status.notin_(["PW", "CD"]))
    online_qry = online_qry.filter(Order.reg_date >= start_date)
    online_qry = online_qry.filter(Order.reg_date < end_date)
    online_qry = online_qry.group_by(func.date(Order.reg_date))
    online_data = online_qry.all()
    online_list = [DataRevenue.from_orm(row) for row in online_data]

    return DataMonth(online=online_list, offline=offline_list)


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False
