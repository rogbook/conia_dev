import os
import json

import requests
from pydantic import BaseModel, Field
from typing import Optional

import OpenSSL
from OpenSSL import crypto
import base64

from app.errors.exceptions import PgFailEx
from app.common.consts import PG_KCP_CANCEL_PART
from app.common.config import conf


class ReqData(BaseModel):
    site_cd: str
    tran_cd: str
    enc_data: str
    enc_info: str
    cert_info: str
    ordr_mony: str


class CancelData(BaseModel):
    site_cd: str
    kcp_cert_info: str
    mod_type: str
    tno: str
    mod_mny: Optional[int]
    rem_mny: Optional[int]
    mod_desc: Optional[str]


class ResData(BaseModel):
    tno: str
    amount: int
    app_time: Optional[str] = Field(title="결제(승인) 시간")

    card_cd: Optional[str] = Field(title="발급사 코드")
    card_name: Optional[str] = Field(title="발급사 명")
    card_no: Optional[str] = Field(title="카드번호")
    app_no: Optional[str] = Field(title="승인번호")
    noinf: Optional[str] = Field(title="무이자 여부")
    noinf_type: Optional[str] = Field(title="(무이자 결제인 경우) 카드사 이벤트 무이자인 경우: CARD 상점 부담 무이자인 경우: SHOP")
    quota: Optional[str] = Field(title="할부 기간")
    partcanc_yn: Optional[str] = Field(title="부분취소 가능 유무")
    card_bin_type_01: Optional[str] = Field(title="카드구분 개인: 0 / 법인: 1")
    card_bin_type_02: Optional[str] = Field(title="카드구분 일반: 0 / 체크: 1")

    bankname: Optional[str] = Field(title="은행 명")
    bankcode: Optional[str] = Field(title="은행코드")
    cash_authno: Optional[str] = Field(title="현금영수증 승인번호")
    cash_no: Optional[str] = Field(title="현금영수증 거래번호")
    bk_mny: Optional[str] = Field(title="계좌이체 결제 금액")

    account: Optional[str] = Field(title="가상계좌 번호")
    va_date: Optional[str] = Field(title="가상계좌 입금마감일")

    van_cd: Optional[str] = Field(title="결제 사 코드")
    van_id: Optional[str] = Field(title="실물/컨텐츠 구분")
    commid: Optional[str] = Field(title="통신사 코드")
    mobile_no: Optional[str] = Field(title="휴대폰 번호")


class ResCancelData(BaseModel):
    tno: str
    canc_time: str = Field(title="취소시각")
    mod_mny: Optional[int] = Field(title="부분취소일 경우 부분취소금액")
    rem_mny: Optional[int] = Field(title="부분취소일 경우 남은 원거래 금액")
    mod_pacn_seq_no: Optional[str] = Field(title="부분취소 일련번호")
    card_mod_mny: Optional[int] = Field(title="card_mod_mny")
    coupon_mod_mny: Optional[int] = Field(title="coupon_mod_mny")


# 결제 요청 API
def payment(data: ReqData):
    # api_url = "https://spl.kcp.co.kr/gw/enc/v1/payment"
    api_url = "https://stg-spl.kcp.co.kr/gw/enc/v1/payment"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        'tran_cd': data.tran_cd,
        'site_cd': data.site_cd,
        'kcp_cert_info': data.cert_info,
        'enc_data': data.enc_data,
        'enc_info': data.enc_info,
        'ordr_mony': data.ordr_mony
    }

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False, indent="\t").encode('utf8'))
    result = res.json()

    if result['res_cd'] == "0000":
        return ResData.parse_obj(result)
    else:
        print(result['res_msg'])
        raise PgFailEx(msg=result['res_msg'], code=result['res_cd'])


# 결제 취소 API
def cancel(data: CancelData):
    c = conf()
    api_url = f"{c.PG_KCP_HOST}/gw/mod/v1/cancel"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    sign_data = f"{data.site_cd}^{data.tno}^{data.mod_type}"
    signed_data = make_sign_data(sign_data)

    req_data = {
        "site_cd": data.site_cd,
        "kcp_cert_info": data.kcp_cert_info,
        "kcp_sign_data": signed_data,
        "mod_type": data.mod_type,
        "tno": data.tno
    }
    if data.mod_type == PG_KCP_CANCEL_PART:
        req_data.update(mod_mny=data.mod_mny)
        req_data.update(rem_mny=data.rem_mny)
        req_data.update(mod_desc=data.mod_desc)

    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False, indent="\t").encode('utf8'))
    result = res.json()

    if result['res_cd'] == "0000":
        return ResCancelData.parse_obj(result)
    else:
        print(result['res_msg'])
        raise PgFailEx(msg=result['res_msg'], code=result['res_cd'])


# 서명 데이터 생성 예제
def make_sign_data(orgData):
    # 개인키 READ
    c = conf()
    file_path = os.path.join(os.getcwd(), 'certificate/', c.PG_KCP_CERT_FILE)

    if not os.path.exists(file_path):
        file_path = os.path.join(os.getcwd(), 'app/certificate/', c.PG_KCP_CERT_FILE)

    key_file = open(file_path, 'r')
    key = key_file.read()
    key_file.close()

    password = c.PG_KCP_CERT_PASSWD.encode('utf-8')
    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key, password)

    # 서명 데이터 생성
    sign = OpenSSL.crypto.sign(pkey, orgData, 'sha256')
    kcp_sign_data = base64.b64encode(sign).decode()

    return kcp_sign_data
