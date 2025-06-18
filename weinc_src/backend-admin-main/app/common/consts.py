JWT_SECRET_KEY = "8e93684faae66facb03cab63bea792a70e0200889c9d2199e18c8541a1fe477d"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

CERT_SMS_ABLE_COUNT_MOBILE = 10
CERT_SMS_ABLE_COUNT_IP = 50
# 문자인증 제한 시간
CERT_SMS_ABLE_TIME_MINUTE = 50

AES_KEY = "8e93684faae66facb03cab63bea792a7"
AES_IV = "0e0200889c9d2199e18c8541a1fe477d"

RANDOM_STRING_POOL = "ABCDEFGHJKLMNPQRSTWXYZabcdefghjkmnpqrstwxyz!@#$%^&*23456789"

# 본인인증
NICE_TOKEN = "965795a3-169f-4567-9dcf-39b906fb2202"
NICE_CLIENT_ID = "fe53ffa2-31e1-4dec-ac8d-6c3bd07f3810"
NICE_CLIENT_SECRET = "3a2dc54195aa3d66f77f26914e8651ef"
NICE_PRODUCT_ID = "2101979031"

# SMS 전송
CONIA_SMS_URL = "https://sms.coniaworld.com"
CONIA_SMS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhYmxlX2lwIjpbIjMuMzguMTI4LjQ1IiwiMTQuMzYuNDcuMTY5IiwiMTUuMTY1LjcuMTEzIl0sImFibGVfc2VuZGVyIjpbIjE1MjI5Nzk1IiwiMTY0NDczNzAiXSwiZXhwIjoyMzUzMTk0OTM5fQ.ztNh9GKSJOYu3Mh0l1hwXuCqP9xVkcvgxaanWCbiwNk"
CONIA_SMS_SENDER = "16447370"

# AWS: conia-s3
AWS_ACCESS_KEY = 'AKIATIKIS3C6NSG7EEUN'
AWS_ACCESS_SECRET = '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'
AWS_REGION = 'ap-northeast-2'

# AWS: S3 버킷
AWS_S3_BUCKET_IMG = "conia-img"
AWS_S3_BUCKET_IMG_HOST = "https://d32r23fv3xy9ae.cloudfront.net/"

# KCP 결제
PG_KCP_CANCEL_ALL = "STSC"
PG_KCP_CANCEL_PART = "STPC"

# 주문 상태
ORDER_STATUS = {
    "PW": "입금대기",
    "PD": "결제완료",
    "PU": "부분사용",
    "CD": "결제취소",
    "EXP": "기한만료",
    "DW": "상품준비중",
    "DN": "배송중",
    "DC": "배송완료",
    "DD": "출고지연",
    "CP": "구매확정",
    "RFR": "반품요청",
    "RFN": "반품진행중",
    "RFC": "반품완료",
    "EXR": "교환요청",
    "EXN": "교환진행중",
    "EXC": "교환완료",
}

MEMBER_STATUS = {
    "Y": "정상",
    "R": "승인 대기중",
    "P": "이용정지",
    "E": "이메일인증 대기중",
    "D": "탈퇴",
}

SETTLEMENT_STATUS = {
    "R": "대기",
    "C": "확정 ",
    "P": "입금완료",
    "J": "보류증 ",
}
