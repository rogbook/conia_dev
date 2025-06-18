import requests
import urllib3
import json
from pydantic import BaseModel, Field
from typing import Optional, List
from urllib.parse import quote

from app.common.config import conf
from app.common.consts import CONIA_SMS_SENDER
from app.errors.exceptions import APIException
from app.utils.crypto_utils import AES128


class ReqIssue(BaseModel):
    tradeId: str
    productCode: str
    receiver: str


class ReqInfo(BaseModel):
    tradeId: str
    pinCode: str


class ReqCancel(BaseModel):
    tradeId: str
    pinCode: str


class DataCoupon(BaseModel):
    brandNm: Optional[str] = Field(title="브랜드명")
    branchCd: Optional[str] = Field(title="지점코드")
    branchNm: Optional[str] = Field(title="지점명")
    cnsmPriceAmt: Optional[str] = Field(title="정상판매단가")
    correcDtm: Optional[str] = Field(title="변경일자")
    goodsCd: Optional[str] = Field(title="상품코드")
    goodsNm: Optional[str] = Field(title="상품명")
    mmsBrandThumImg: Optional[str] = Field(title="브랜이썸네일이미지")
    pinNo: str = Field(title="핀번호")
    pinStatusCd: str = Field(title="핀상태코드")
    pinStatusNm: str = Field(title="핀상태명")
    recverTelNo: Optional[str] = Field(title="수신자번호")
    sellPriceAmt: Optional[str] = Field(title="실판매단가")
    sendBasicCd: Optional[str] = Field(title="기본 발송번호")
    sendRstCd: Optional[str] = Field(title="발송결과코드")
    sendRstMsg: Optional[str] = Field(title="발송결과메세지")
    sendStatusCd: Optional[str] = Field(title="발송상태명")
    senderTelNo: Optional[str] = Field(title="발신자번호")
    validPrdEndDt: Optional[str] = Field(title="유효기간 만료일")
    validPrdStartDt: Optional[str] = Field(title="유효기간 시작일")
    goodsConfigCd: Optional[str] = Field(title="상품구성코드")
    goodsImg250: Optional[str] = Field(title="250x250 사이즈 이미지")
    goodsImg250Path: Optional[str] = Field(title="250x250 사이즈 이미지 경로")
    goodsImg500: Optional[str] = Field(title="500x500 사이즈 이미지")
    goodsImg500Path: Optional[str] = Field(title="500x500 사이즈 이미지 경로")
    orderDtm: Optional[str] = Field(title="주문일시")
    remainAmt: Optional[str] = Field(title="잔액 ( ※ 금액권일 경우 응답)")


class ResBase(BaseModel):
    resCode: str
    resMsg: str
    raw_data: Optional[str]


class ResIssue(ResBase):
    pinNo: str
    trId: Optional[str]
    ctrId: Optional[str]
    limitEndDt: Optional[str]


class ResInfo(ResBase):
    couponInfoList: List[DataCoupon]


class EcounponKt:

    def __init__(self):
        c = conf()
        self.host = c.ECOUPON_KT_HOST
        self.template_code = c.ECOUPON_KT_TEMPLATE_CODE
        self.headers = {'api_code': '',
                        'custom_auth_code': c.ECOUPON_KT_AUTH_CODE,
                        'custom_auth_token': c.ECOUPON_KT_AUTH_TOKEN,
                        'Accept': 'application/json'}

    def get(self, endpoint, api_code, data):
        url = self.host + endpoint

        headers = self.headers.copy()
        headers.update(api_code=api_code)

        res = requests.get(url=url, headers=headers, params=data)

        if res.status_code != 200:
            raise APIException(status_code=res.status_code, detail=res.text)
        else:
            return res

    def post(self, endpoint, api_code, data):
        url = self.host + endpoint

        headers = self.headers.copy()
        headers.update(api_code=api_code)

        res = requests.post(url=url, headers=headers, files=data)

        if res.status_code != 200:
            raise APIException(status_code=res.status_code, detail=res.text)
        else:
            return res

    def issue(self, req: ReqIssue) -> ResIssue:
        msg = """[윙크  WEINC]
안녕하세요.
브랜드티켓을 구매해주셔서 감사합니다.
즐거운 마음으로 사용하시고
오늘도 행복한 하루 보내세요!
감사합니다. ♥
"""
        post_data = {
            'operation_type': 'REAL',
            'gubun': 'R',
            'goods_id': req.productCode,
            'tr_id': req.tradeId,
            'title': '[윙크]브랜드티켓',
            'msg': msg,
            'template_id': self.template_code,
            'sender': CONIA_SMS_SENDER,
            'receiver': req.receiver,
        }

        res = self.post(endpoint='/coupon/send', api_code='0455', data=post_data)
        try:
            res_data: ResIssue = ResIssue.parse_obj(res.json())
            res_data.raw_data = res.text

            return res_data
        except Exception as e:
            print(f"######### {res.text}")
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)

    def info(self, req: ReqInfo) -> ResInfo:
        param_data = {
            'tr_id': req.tradeId,
            'pinNo': req.pinCode
        }

        res = self.get(endpoint='/coupon', api_code='0451', data=param_data)
        try:
            res_data: ResInfo = ResInfo.parse_obj(res.json())
            res_data.raw_data = res.text

            return res_data
        except Exception as e:
            print(f"######### {res.text}")
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)

    def cancel(self, req: ReqCancel) -> ResBase:
        post_data = {
            'tr_id': req.tradeId,
            'pinNo': req.pinCode
        }

        res = self.post(endpoint='/coupon/cancel', api_code='0452', data=post_data)
        try:
            res_data: ResBase = ResBase.parse_obj(res.json())
            res_data.raw_data = res.text

            return res_data
        except Exception as e:
            print(f"######### {res.text}")
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)


