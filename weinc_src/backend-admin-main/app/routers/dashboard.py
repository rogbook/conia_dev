from typing import List, Optional

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import Member, Order
from app.models.auth import MemberToken
from app.models.dashboard import DataDashboard
from app.utils.jwt import token_user
from app.utils.date_utils import D

router = APIRouter(prefix='/dashboard')


@router.get("", response_model=DataDashboard, name="대시보드 데이터")
def dashboard(session: Session = Depends(db.session),
              user: MemberToken = Security(token_user, scopes=[])):
    member_all_cnt = Member.filter(session, admin_yn='N').count()
    member_today_cnt = Member.filter(session, reg_date__gt=D.today_str()).count()
    order_all_cnt = Order.filter(session).count()
    order_today_cnt = Order.filter(session, reg_date__gt=D.today_str()).count()

    data = DataDashboard(
        member_all_cnt=member_all_cnt,
        member_today_cnt=member_today_cnt,
        order_all_cnt=order_all_cnt,
        order_today_cnt=order_today_cnt
    )

    return data
