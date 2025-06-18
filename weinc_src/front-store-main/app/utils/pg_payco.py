import json
from typing import Optional, List

import requests
from pydantic import BaseModel

from app.common.config import conf
from app.errors.exceptions import PgFailEx


class ReqReserve(BaseModel):
    sellerOrderReferenceKey: str
    orderTitle: str
    orderChannel: str
    totalPaymentAmt: str
    productAmt: str
    productPaymentAmt: str
    orderQuantity: str
    productName: str
    sellerOrderProductReferenceKey: str
    returnUrl: str
    totalTaxfreeAmt: Optional[int]
    totalTaxableAmt: Optional[int]
    totalVatAmt: Optional[int]
    taxationType: Optional[str]
    extraData: Optional[str]


class ReqPayment(BaseModel):
    reserveOrderNo: str
    sellerOrderReferenceKey: str
    paymentCertifyToken: str
    totalPaymentAmt: str
    totalTaxfreeAmt: Optional[int]
    totalTaxableAmt: Optional[int]
    totalVatAmt: Optional[int]


class CardSettleInfo(BaseModel):
    cardCompanyName: Optional[str]
    cardCompanyCode: Optional[str]
    cardNo: Optional[str]
    cardInstallmentMonthNumber: Optional[str]
    cardAdmissionNo: Optional[str]
    cardInterestFreeYn: Optional[str]
    corporateCardYn: Optional[str]
    partCancelPossibleYn: Optional[str]


class CellphoneSettleInfo(BaseModel):
    companyName: Optional[str]
    cellphoneNo: Optional[str]


class RealtimeAccountTrasferSettleInfo(BaseModel):
    bankName: Optional[str]
    bankCode: Optional[str]


class NonBankbookSettleInfo(BaseModel):
    bankName: Optional[str]
    bankCode: Optional[str]
    accountNo: Optional[str]
    paymentExpirationYmd: Optional[str]


class CouponSettleInfo(BaseModel):
    discountAmt: Optional[str]
    discountConditionAmt: Optional[str]


class PaymentDetails(BaseModel):
    paymentTradeNo: Optional[str]
    paymentMethodCode: Optional[str]
    paymentMethodName: Optional[str]
    paymentAmt: Optional[str]
    tradeYmdt: Optional[str]
    pgAdmissionNo: Optional[str]
    pgAdmissionYmdt: Optional[str]
    easyPaymentYn: Optional[str]

    cardSettleInfo: Optional[CardSettleInfo]
    cellphoneSettleInfo: Optional[CellphoneSettleInfo]
    realtimeAccountTrasferSettleInfo: Optional[RealtimeAccountTrasferSettleInfo]
    nonBankbookSettleInfo: Optional[NonBankbookSettleInfo]
    couponSettleInfo: Optional[CouponSettleInfo]


class ResPayment(BaseModel):
    sellerOrderReferenceKey: Optional[str]
    reserveOrderNo: Optional[str]
    orderNo: Optional[str]
    orderChannel: Optional[str]
    totalOrderAmt: Optional[str]
    totalPaymentAmt: Optional[str]
    orderCertifyKey: Optional[str]
    paymentCompletionYn: Optional[str]
    paymentCompleteYmdt: Optional[str]

    paymentDetails: Optional[List[PaymentDetails]]


class DataReserve(BaseModel):
    reserveOrderNo: str
    orderSheetUrl: str


class ResReserve(BaseModel):
    result: DataReserve
    code: int
    message: str


class ReqCancel(BaseModel):
    orderNo: str
    cancelTotalAmt: str
    orderCertifyKey: str


class ResCancel(BaseModel):
    orderNo: str
    cancelTradeSeq: str
    totalCancelPaymentAmt: str
    remainCancelPossibleAmt: str
    cancelYmdt: str


# 결제 예약 요청 API
def reserve(req: ReqReserve):
    c = conf()
    api_url = f"{c.PG_PAYCO_HOST}/outseller/order/reserve"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        "sellerKey": c.PG_PAYCO_SELLER_KEY,
        "sellerOrderReferenceKey": req.sellerOrderReferenceKey,
        "orderTitle": req.orderTitle,
        "returnUrl": req.returnUrl,
        "orderChannel": req.orderChannel,
        "totalPaymentAmt": req.totalPaymentAmt,
        "totalTaxfreeAmt": req.totalTaxfreeAmt,
        "totalTaxableAmt": req.totalTaxableAmt,
        "totalVatAmt": req.totalVatAmt,
        "inAppYn": "N",
        "orderMethod": "EASYPAY",
        "payMode": "PAY2",
        "orderProducts": [{
            "cpId": c.PG_PAYCO_CP_ID,
            "productId": c.PG_PAYCO_PRODUCT_ID,
            "productAmt": req.productAmt,
            "productPaymentAmt": req.productPaymentAmt,
            "orderQuantity": "1",
            "sortOrdering": "1",
            "productName": req.productName,
            "sellerOrderProductReferenceKey": req.sellerOrderProductReferenceKey,
            "taxationType": req.taxationType
        }]
    }
    if req.extraData:
        req_data.update(extraData=req.extraData)

    result = post(api_url, headers, req_data)

    if result['code'] == 0:
        return ResReserve.parse_obj(result)
    else:
        print(result['message'])
        raise PgFailEx(msg=result['message'], code=result['code'])


# 결제 요청 API
def payment(req: ReqPayment):
    c = conf()
    api_url = f"{c.PG_PAYCO_HOST}/outseller/payment/approval"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        "totalPaymentAmt": req.totalPaymentAmt,
        "totalTaxfreeAmt": req.totalTaxfreeAmt,
        "totalTaxableAmt": req.totalTaxableAmt,
        "totalVatAmt": req.totalVatAmt,
        "sellerKey": c.PG_PAYCO_SELLER_KEY,
        "reserveOrderNo": req.reserveOrderNo,
        "sellerOrderReferenceKey": req.sellerOrderReferenceKey,
        "paymentCertifyToken": req.paymentCertifyToken,
    }
    result = post(api_url, headers, req_data)

    if result['code'] == 0:
        return ResPayment.parse_obj(result['result'])
    else:
        print(result['message'])
        raise PgFailEx(msg=result['message'], code=result['code'])


# 결제 요청 API
def cancel(req: ReqCancel):
    c = conf()
    api_url = f"{c.PG_PAYCO_HOST}/outseller/order/cancel"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8'}

    req_data = {
        "sellerKey": c.PG_PAYCO_SELLER_KEY,
        "orderNo": req.orderNo,
        "cancelTotalAmt": req.cancelTotalAmt,
        "orderCertifyKey": req.orderCertifyKey,
    }
    result = post(api_url, headers, req_data)

    if result['code'] == 0:
        return ResCancel.parse_obj(result['result'])
    else:
        print(result['message'])
        raise PgFailEx(msg=result['message'], code=result['code'])


def post(api_url, headers, req_data):
    res = requests.post(api_url, headers=headers, data=json.dumps(req_data, ensure_ascii=False).encode('utf8'))
    return res.json()
