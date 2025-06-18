from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List

from app.utils.crypto_utils import AES256
from app.common.consts import AES_KEY, AES_IV


class Store(BaseModel):
    code: str
    title: str

    class Config:
        orm_mode = True


class MemberStore(BaseModel):
    confirm: str
    store: Store
    class Config:
        orm_mode = True


class AddCustomer(BaseModel):
    """
    회원 등록 데이터 모델
    """
    email: EmailStr = Field(title="USER ID(Email)")
    password: str = Field(title="패스워드")  #
    name: Optional[str] = Field(title="이름")
    mobile: Optional[str] = Field(title="휴대전화")
    mailling: str = Field(title="마케팅 메일 수신여부")
    sms: str = Field(title="마케팅 문자 수신여부")
    referer: str = Field(title="유입경로 full_url")
    referer_domain: str = Field(title="유입경로 도메인")
    join_platform: str = Field(title="가입 플랫폼 (P, M, AOS, IOS)")

    nickname: Optional[str] = Field(title="닉네임")
    phone: Optional[str] = Field(title="전화번호")
    zipcode: Optional[str] = Field(title="우편번호")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="상세주소")
    sex: Optional[str] = Field(title="성별")
    birthday: Optional[date] = Field(title="생년월일")
    recommend: Optional[str] = Field(title="추천인코드")
    auth_yn: Optional[str] = Field(title="본인인증 여부")
    adult_auth: Optional[str] = Field(title="성인인증 여부")
    adult_auth_date: Optional[datetime] = Field(title="성인인증 일시")
    sns_naver: Optional[str] = Field(title="SNS 로그인 연동값 naver")
    sns_kakao: Optional[str] = Field(title="SNS 로그인 연동값 kakao")
    sns_google: Optional[str] = Field(title="SNS 로그인 연동값 google")
    sns_facebook: Optional[str] = Field(title="SNS 로그인 연동값 facebook")
    sns_apple: Optional[str] = Field(title="SNS 로그인 연동값 apple")
    sns_payco: Optional[str] = Field(title="SNS 로그인 연동값 payco")
    bank: Optional[str] = Field(title="환불용 계좌 은행")
    account: Optional[str] = Field(title="환불용 계좌")
    admin_yn: Optional[str] = Field(title="관리자 여부")
    grade: Optional[str] = Field(title="등급")
    refresh_token: Optional[str] = Field(title="갱신용 토큰")
    partner: Optional[str] = Field(title="파트너 회원 [N, Y, R(승인대기)]")


class DataCustomer(BaseModel):
    """
    회원 데이터 모델
    """
    id: int = Field(title="ID")
    email: EmailStr = Field(title="USER ID(Email)")
    name: Optional[str] = Field(title="이름")
    nickname: Optional[str] = Field(title="닉네임")
    mailling: str = Field(title="마케팅 메일 수신여부")
    sms: str = Field(title="마케팅 문자 수신여부")
    phone: Optional[str] = Field(title="전화번호")
    mobile: Optional[str] = Field(title="휴대전화")
    zipcode: Optional[str] = Field(title="우편번호")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="상세주소")
    sex: Optional[str] = Field(title="성별")
    birthday: Optional[date] = Field(title="생년월일")
    recommend: Optional[str] = Field(title="추천인코드")
    status: str = Field(title="상태")
    login_cnt: int = Field(title="로그인 횟수")
    review_cnt: int = Field(title="상품 리뷰 횟수")
    order_cnt: int = Field(title="주문 횟수")
    order_sum: int = Field(title="주문 금액")
    lastlogin_date: datetime = Field(title="마지막 로그인 일시")
    reg_date: datetime = Field(title="등록일시")
    mod_date: datetime = Field(title="수정일시")
    auth_yn: str = Field(title="본인인증 여부")
    adult_auth: str = Field(title="성인인증 여부")
    referer: str = Field(title="유입경로 full_url")
    referer_domain: str = Field(title="유입경로 도메인")
    join_platform: str = Field(title="가입 플랫폼 (P, M, AOS, IOS)")
    marketing_agree_date: datetime = Field(title="마케팅 수신 동의 일시")
    adult_auth_date: Optional[datetime] = Field(title="성인인증 일시")
    sns_naver: Optional[str] = Field(title="SNS 로그인 연동값 naver")
    sns_kakao: Optional[str] = Field(title="SNS 로그인 연동값 kakao")
    sns_google: Optional[str] = Field(title="SNS 로그인 연동값 google")
    sns_facebook: Optional[str] = Field(title="SNS 로그인 연동값 facebook")
    sns_apple: Optional[str] = Field(title="SNS 로그인 연동값 apple")
    sns_payco: Optional[str] = Field(title="SNS 로그인 연동값 payco")
    grade: Optional[str] = Field(title="등급")
    memo: Optional[str] = Field(title="관리자 메모")

    member_store: Optional[List[MemberStore]] = Field(title="이용 상점 목록")

    class Config:
        orm_mode = True

    @validator('mobile')
    def decrypt(cls, v):
        if v and len(v) > 24: # ListDataMember 로 들어 가면 두번 호출 되어 복호화된 데이터를 또 다시 복호화 시도 에러 발생
            v = AES256(AES_KEY, AES_IV).decrypt(v)
        return v


class ListDataCustomer(BaseModel):
    total: int = Field(title="Total Count")
    datas: List[DataCustomer]


class ModCustomer(BaseModel):
    """
    회원 수정 데이터 모델
    """
    password: Optional[str] = Field(title="패스워드")  #
    name: Optional[str] = Field(title="이름")
    nickname: Optional[str] = Field(title="닉네임")
    mailling: Optional[str] = Field(title="마케팅 메일 수신여부")
    sms: Optional[str] = Field(title="마케팅 문자 수신여부")
    phone: Optional[str] = Field(title="전화번호")
    mobile: Optional[str] = Field(title="휴대전화")
    zipcode: Optional[str] = Field(title="우편번호")
    address: Optional[str] = Field(title="주소")
    address_detail: Optional[str] = Field(title="상세주소")
    sex: Optional[str] = Field(title="성별")
    birthday: Optional[date] = Field(title="생년월일")
    recommend: Optional[str] = Field(title="추천인코드")
    status: Optional[str] = Field(title="상태")
    auth_yn: Optional[str] = Field(title="본인인증 여부")
    adult_auth: Optional[str] = Field(title="성인인증 여부")
    marketing_agree_date: Optional[datetime] = Field(title="마케팅 수신 동의 일시")
    adult_auth_date: Optional[datetime] = Field(title="성인인증 일시")
    sns_naver: Optional[str] = Field(title="SNS 로그인 연동값 naver")
    sns_kakao: Optional[str] = Field(title="SNS 로그인 연동값 kakao")
    sns_google: Optional[str] = Field(title="SNS 로그인 연동값 google")
    sns_facebook: Optional[str] = Field(title="SNS 로그인 연동값 facebook")
    sns_apple: Optional[str] = Field(title="SNS 로그인 연동값 apple")
    sns_payco: Optional[str] = Field(title="SNS 로그인 연동값 payco")
    grade: Optional[str] = Field(title="등급")
    memo: Optional[str] = Field(title="관리자 메모")


class AddDeliveryAddress(BaseModel):
    """
    배송지 등록 데이터 모델
    """
    title: str = Field(title="배송지명")
    name: str = Field(title="이름")
    address: str = Field(title="주소")
    address_detail: str = Field(title="주소 상세")
    zipcode: str = Field(title="우편번호")
    mobile: str = Field(title="휴대전화")
    phone: Optional[str] = Field(title="전화번호")
    default_yn: str = Field(title="기본 여부")
