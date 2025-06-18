from pydantic import BaseModel
from typing import Optional, Any, List


class DataDashboard(BaseModel):
    member_all_cnt: str
    member_today_cnt: str
    order_all_cnt: str
    order_today_cnt: str
