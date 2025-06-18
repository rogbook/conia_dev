import requests
import urllib3
from pydantic import BaseModel, Field
from typing import Optional, List

from app.common.config import conf
from app.common.consts import CONIA_SMS_SENDER
from app.errors.exceptions import APIException


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


class ReqResend(BaseModel):
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


class DataGoods(BaseModel):
    b2bGoodsYn: Optional[str] = Field(title="b2b 상품 유무")
    brandCd: Optional[str] = Field(title="브랜드 코드")
    brandIconImg: Optional[str] = Field(title="브랜드 아이콘 이미지")
    brandNm: Optional[str] = Field(title="브랜드 명")
    cancelPosblYn: Optional[str] = Field(title="취소 가능 유무")
    cnsmPriceAmt: Optional[str] = Field(title="환불 금액 (소비자가격)")
    extdPosblYn: Optional[str] = Field(title="연장 가능 유무")
    goodsCd: Optional[str] = Field(title="상품 코드")
    goodsExpl: Optional[str] = Field(title="상품 교환 장소")
    goodsImg250: Optional[str] = Field(title="상품이미지 250x250")
    goodsImg250Path: Optional[str] = Field(title="상품이미지 경로 250x250")
    goodsImg500: Optional[str] = Field(title="상품이미지 500x500")
    goodsImg500Path: Optional[str] = Field(title="상품이미지 경로 500x500")
    goodsNm: Optional[str] = Field(title="상품이름")
    goodsTypeCd: Optional[str] = Field(title="상품타입 코드")
    goodsTypeDtlCd: Optional[str] = Field(title="상세 상품타입 코드")
    goodsTypeDtlNm: Optional[str] = Field(title="상세 상품타입 명")
    goodsTypeNm: Optional[str] = Field(title="상품타입 명")
    mmsBarcdCreateYn: Optional[str] = Field(title="mms 바코드 생성 유무")
    mmsBrandThumImg: Optional[str] = Field(title="mms 브랜드 이미지")
    mmsContent: Optional[str] = Field(title="mms 내용")
    mmsGoodsImg: Optional[str] = Field(title="mms 상품이미지")
    refundPosblYn: Optional[str] = Field(title="환불 가능 유무")
    searchText: Optional[str] = Field(title="검색 텍스트")
    sellDisCntCost: Optional[str] = Field(title="판매할인 금액")
    sellEndDt: Optional[str] = Field(title="판매 종료일")
    sellPriceAmt: Optional[str] = Field(title="판매금액")
    splcomCd: Optional[str] = Field(title="공급사코드")
    splcomNm: Optional[str] = Field(title="공급사 명")
    stadTermsApplyYn: Optional[str] = Field(title="연장 유무")
    useComCode: Optional[str] = Field(title="판매처 코드")
    useComName: Optional[str] = Field(title="판매처 명")
    validPrdDate: Optional[str] = Field(title="유효 일수")
    validPrdDay: Optional[str] = Field(title="유효 날짜")
    validPrdTypeCd: Optional[str] = Field(title="유효 타입 코드 (01-일수/02-일자)")


class ResBase(BaseModel):
    resCode: str
    resMsg: str
    raw_data: Optional[str]


class ResIssue(ResBase):
    pinNo: str
    trId: str
    ctrId: str
    limitEndDt: str


class ResInfo(ResBase):
    couponInfoList: List[DataCoupon]


class ResGoods(ResBase):
    listNum: Optional[int]
    goodsList: List[DataGoods]


class EcounponKt:

    def __init__(self):
        c = conf()
        self.host = c.ECOUPON_KT_HOST
        self.headers = {'api_code': '',
                        'custom_auth_code': c.ECOUPON_KT_AUTH_CODE,
                        'custom_auth_token': c.ECOUPON_KT_AUTH_TOKEN,
                        'Accept': 'application/json'}

    def get(self, endpoint, api_code, data=None):
        url = self.host + endpoint

        headers = self.headers.copy()
        headers.update(api_code=api_code)

        if data:
            res = requests.get(url=url, headers=headers, params=data)
        else:
            res = requests.get(url=url, headers=headers)

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
        post_data = {
            'operation_type': 'REAL',
            'gubun': 'R',
            'goods_id': req.productCode,
            'tr_id': req.tradeId,
            'title': '윙크 브랜드티켓',
            'msg': '본 티켓은 유효기간내 사용 가능하며 B2B 전용상품으로 취소 및 환불이 불가합니다. 티켓을 인증 후 원하시는 상품을 선택하신 후 매장에서 제품과 교환하시기 바랍니다.',
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

    def resend(self, req: ReqResend) -> ResBase:
        post_data = {
            'tr_id': req.tradeId,
            'pinNo': req.pinCode
        }

        res = self.post(endpoint='/coupon/resend', api_code='0454', data=post_data)
        try:
            res_data: ResBase = ResBase.parse_obj(res.json())
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

    def goods(self) -> ResGoods:

        res = self.get(endpoint='/goods', api_code='0101')
        try:
            res_data: ResGoods = ResGoods.parse_obj(res.json())
            res_data.raw_data = res.text

            return res_data
        except Exception as e:
            print(f"######### {res.text}")
            raise APIException(status_code=res.status_code, detail=res.text, ex=e)

