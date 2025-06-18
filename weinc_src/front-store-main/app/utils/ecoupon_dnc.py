import requests
import json
from pydantic import BaseModel
from typing import Optional, List
from urllib.parse import quote

from app.common.config import conf
from app.errors.exceptions import APIException
from app.utils.crypto_utils import AES128


class ReqIssue(BaseModel):
    tradeId: str
    productCode: str
    quantity: int
    requestedAt: str


class ReqInfo(BaseModel):
    pinCode: str
    orderCode: str


class ReqCancel(BaseModel):
    tradeId: str
    pinCode: str
    orderCode: str
    requestedAt: str


class DataCoupon(BaseModel):
    pinCode: str
    orderCode: str
    startAt: str
    expireAt: str


class ResBase(BaseModel):
    raw_data: Optional[str]


class ResIssue(ResBase):
    tradeId: str
    quantity: int

    coupons: List[DataCoupon]


class ResCancel(ResBase):
    tradeId: str
    pinCode: str


class ResInfo(ResBase):
    pinCode: str
    productName: str
    productAmount: str
    startAt: str
    expireAt: str
    exchangeProvider: str
    exchangePlace: Optional[str]
    exchangeDate: Optional[str]
    status: str
    balance: Optional[str]


def issue(req: ReqIssue):
    c = conf()
    api_url = f"{c.ECOUPON_DNC_HOST}/conialab/orders/issue"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'x-api-key': c.ECOUPON_DNC_KEY}

    req_data = {
        'campaignCode': c.ECOUPON_DNC_CAMPAIGN_CODE,
        'tradeId': req.tradeId,
        'productCode': req.productCode,
        'quantity': req.quantity,
        'requestedAt': req.requestedAt,
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        raise APIException(status_code=res.status_code, detail=res.text)
    else:
        result = res.json()
        try:
            res_data = ResIssue.parse_obj(result)
            res_data.raw_data = res.text
        except Exception as e:
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)

    return res_data


def info(req: ReqInfo) -> ResInfo:
    c = conf()
    api_url = f"{c.ECOUPON_DNC_HOST}/conialab/coupons/info"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'x-api-key': c.ECOUPON_DNC_KEY}

    req_data = {
        'campaignCode': c.ECOUPON_DNC_CAMPAIGN_CODE,
        'pinCode': req.pinCode,
        'orderCode': req.orderCode
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        raise APIException(status_code=res.status_code, detail=res.text)
    else:
        result = res.json()
        try:
            res_data = ResInfo.parse_obj(result)
            res_data.raw_data = res.text
        except Exception as e:
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)

    return res_data


def cancel(req: ReqCancel) -> ResCancel:
    c = conf()
    api_url = f"{c.ECOUPON_DNC_HOST}/conialab/coupons/cancel"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'x-api-key': c.ECOUPON_DNC_KEY}

    req_data = {
        'campaignCode': c.ECOUPON_DNC_CAMPAIGN_CODE,
        'tradeId': req.tradeId,
        'orderCode': req.orderCode,
        'requestedAt': req.requestedAt,
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        raise APIException(status_code=res.status_code, detail=res.text)
    else:
        result = res.json()
        try:
            res_data = ResCancel.parse_obj(result)
            res_data.raw_data = res.text
        except Exception as e:
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)

    return res_data

