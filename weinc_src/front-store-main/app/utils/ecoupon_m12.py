import requests
import json
from pydantic import BaseModel
from typing import Optional
from urllib.parse import quote

from app.common.config import conf
from app.utils.crypto_utils import AES128


class ResBase(BaseModel):
    STATUS_CODE: str
    RESULT_CODE: Optional[str]
    RESULT_REASON: Optional[str]
    TR_ID: Optional[str]
    PIN_NO: Optional[str]
    raw_data: Optional[str]


class ReqIssue(BaseModel):
    tr_id: str
    goods_id: str
    send_no: str
    recv_no: str
    period: Optional[str]


class ReqInfo(BaseModel):
    tr_id: str
    goods_id: str
    pin_no: str


class ReqExtend(BaseModel):
    tr_id: str
    goods_id: str
    pin_no: str
    period: str


class ResIssue(ResBase):
    PERIOD_DATE: Optional[str]
    DUTY_CODE: Optional[str]


class ResInfo(ResBase):
    GOODS_NAME: Optional[str]
    GOODS_TYPE: Optional[str]
    PIN_STATUS: Optional[str]
    ISSUE_DATE: Optional[str]
    PERIOD_DATE: Optional[str]
    ACCOUNT_BALANCE: Optional[str]
    USE_DATE: Optional[str]
    USE_STORE: Optional[str]
    CANCEL_DATE: Optional[str]


class ResCancel(ResBase):
    ISSUE_DATE: Optional[str]
    CANCEL_DATE: Optional[str]


class ResExtend(ResBase):
    ISSUE_DATE: Optional[str]
    PERIOD_DATE: Optional[str]


def issue(req: ReqIssue):
    c = conf()
    api_url = f"{c.ECOUPON_M12_HOST}/basic_coupon/couponIssue.php"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    aes = AES128(c.ECOUPON_M12_KEY.encode(), c.ECOUPON_M12_IV.encode())

    send_enc = aes.encrypt(req.send_no)
    send_no = quote(send_enc)

    recv_enc = aes.encrypt(req.recv_no)
    recv_no = quote(recv_enc)

    req_data = {
        'sid': c.ECOUPON_M12_SID,
        'tr_id': req.tr_id,
        'goods_id': req.goods_id,
        'send_no': send_no,
        'recv_no': recv_no,
        'real_send': "N",
    }
    if req.period:
        req_data.update(period=req.period)

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        res_data = ResIssue(STATUS_CODE='9999', RESULT_CODE=f'{res.status_code}', RESULT_REASON='FAIL', TR_ID=req.tr_id)
    else:
        result = res.json()
        res_data = ResIssue.parse_obj(result)
        res_data.raw_data = res.text
    return res_data


def info(req: ReqInfo):
    c = conf()
    api_url = f"{c.ECOUPON_M12_HOST}/basic_coupon/couponInfo.php"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        'sid': c.ECOUPON_M12_SID,
        'tr_id': req.tr_id,
        'goods_id': req.goods_id,
        'pin_no': req.pin_no,
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        res_data = ResIssue(STATUS_CODE='9999', RESULT_CODE=f'{res.status_code}', RESULT_REASON='FAIL', TR_ID=req.tr_id)
    else:
        result = res.json()
        res_data = ResInfo.parse_obj(result)
        res_data.raw_data = res.text

    return res_data


def cancel(req: ReqInfo):
    c = conf()
    api_url = f"{c.ECOUPON_M12_HOST}/basic_coupon/couponCancel.php"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        'sid': c.ECOUPON_M12_SID,
        'tr_id': req.tr_id,
        'goods_id': req.goods_id,
        'pin_no': req.pin_no,
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        res_data = ResIssue(STATUS_CODE='9999', RESULT_CODE=f'{res.status_code}', RESULT_REASON='FAIL', TR_ID=req.tr_id)
    else:
        result = res.json()
        res_data = ResCancel.parse_obj(result)
        res_data.raw_data = res.text

    return res_data


def extend(req: ReqExtend):
    c = conf()
    api_url = f"{c.ECOUPON_M12_HOST}/basic_coupon/couponExtend.php"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        'sid': c.ECOUPON_M12_SID,
        'tr_id': req.tr_id,
        'goods_id': req.goods_id,
        'pin_no': req.pin_no,
        'period': req.period,
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))

    if res.status_code != 200:
        res_data = ResIssue(STATUS_CODE='9999', RESULT_CODE=f'{res.status_code}', RESULT_REASON='FAIL', TR_ID=req.tr_id)
    else:
        result = res.json()
        res_data = ResCancel.parse_obj(result)
        res_data.raw_data = res.text

    return res_data
