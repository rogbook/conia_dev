from pydantic import BaseModel, Field
from typing import Optional


class DataKtWebhook(BaseModel):
    mdcode: str = Field(title="기업코드")
    tr_id: str = Field(title="쿠폰발급 시 요청한 tr_id")
    trade_type: str = Field(title="01(핀상태변경), 02(유효기간변경)")
    trade_code: str = Field(title="핀상태 / 02: 교환, 03: 반품, 04: 관리폐기, 07: 구매취소")
    trade_date: str = Field(title="사용/사용취소 일자 ( yyyymmddhhmmss)")
    trade_amt: Optional[int] = Field(title="사용금액")
    branch_code: Optional[str] = Field(title="사용 지점코드")
    branch_name: Optional[str] = Field(title="사용 지점명")
    pin_no: Optional[str] = Field(title="쿠폰번호")
    use_start_date: Optional[str] = Field(title="유효기간 시작일")
    use_end_date: Optional[str] = Field(title="유효기간 종료일")


class ResKtWebhook(BaseModel):
    resCode: str
    resMsg: str
