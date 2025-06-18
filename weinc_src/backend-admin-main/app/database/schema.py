from sqlalchemy import Column, DECIMAL, Date, DateTime, Time, ForeignKey, String, Text, text, Index, Table
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import Session, relationship

from app.database.conn import Base, db
from app.errors.exceptions import NotChangeDataEx


metadata = Base.metadata


class BaseMixin:
    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.name != "reg_date"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        if not session:
            sess.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply filter
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt':
                cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte':
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt':
                cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte':
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in':
                cond.append((col.in_(val)))
            elif len(key) == 2 and key[1] == 'ne':
                cond.append((col != val))
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    def update(self, session: Session, auto_commit=False, **kwargs):
        for col in self.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(self, col_name, kwargs.get(col_name))

        if auto_commit:
            session.commit()

        return self

    def update_optional(self, session: Session, auto_commit=False, auto_error=False, **kwargs):
        change_data = []
        for col in self.all_columns():
            col_name = col.name
            if col_name in kwargs:
                if kwargs.get(col_name) is not None:
                    before = getattr(self, col_name)
                    if before != kwargs.get(col_name):
                        if kwargs.get(col_name) == "_null_":
                            setattr(self, col_name, None)
                            change_data.append({
                                col_name: {
                                    "before": before,
                                    "after": "",
                                }
                            })
                        else:
                            setattr(self, col_name, kwargs.get(col_name))
                            change_data.append({
                                col_name: {
                                    "before": before,
                                    "after": kwargs.get(col_name),
                                }
                            })
        if auto_error and len(change_data) == 0:
            raise NotChangeDataEx

        if auto_commit:
            session.commit()

        return change_data

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def paging(self, offset: int, limit: int):
        if offset:
            self._q = self._q.offset(offset)
        if limit:
            self._q = self._q.limit(limit)

        return self

    def update_q(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        ret = None

        self._session.flush()
        if qs > 0:
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def all(self):
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


class Badge(Base, BaseMixin):
    __tablename__ = 'badge'
    __table_args__ = {'comment': '뱃지'}

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(8), nullable=False)
    color = Column(String(8))
    img = Column(String(512))
    shape = Column(String(50))
    reg_date = Column(DateTime, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class Brand(Base, BaseMixin):
    __tablename__ = 'brand'
    __table_args__ = {'comment': '브랜드'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='브랜드 이름')
    description = Column(Text, comment='브랜드 설명')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    photo = Column(String(512))
    pid = Column(ForeignKey('brand.id'), index=True)
    status = Column(String(2), nullable=False, server_default=text("'Y'"))

    parent = relationship('Brand', remote_side=[id])


class Category(Base, BaseMixin):
    __tablename__ = 'category'
    __table_args__ = {'comment': '상품 분류'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='이름')
    description = Column(String(255), comment='설명')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    photo = Column(String(512))
    pid = Column(ForeignKey('category.id'), index=True)
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    depth = Column(INTEGER(10))
    depth1_name = Column(String(45))
    depth2_name = Column(String(45))
    depth3_name = Column(String(45))
    depth4_name = Column(String(45))
    depth1_id = Column(INTEGER(10))
    depth2_id = Column(INTEGER(10))
    depth3_id = Column(INTEGER(10))
    depth4_id = Column(INTEGER(10))

    parent = relationship('Category', remote_side=[id])


class Cert(Base, BaseMixin):
    __tablename__ = 'cert'
    __table_args__ = {'comment': '본인인증 내역'}

    id = Column(INTEGER(10), primary_key=True)
    req_token_version_id = Column(String(128), comment='요청 구분값')
    responseno = Column(String(32))
    authtype = Column(String(4))
    name = Column(String(24))
    utf8_name = Column(String(64))
    birthdate = Column(String(128))
    gender = Column(String(1))
    nationalinfo = Column(String(1))
    mobileco = Column(String(1))
    mobileno = Column(String(128))
    ci = Column(String(88))
    di = Column(String(64))
    user_id = Column(INTEGER(11), comment='요청 회원 ID')
    reg_date = Column(DateTime, server_default=text("current_timestamp()"), comment='인증 요청 시간')
    mod_date = Column(DateTime)
    status = Column(String(2), nullable=False, server_default=text("'R'"), comment='상태')
    ip = Column(String(64), comment='요청 아이피')
    key = Column(String(16), comment='암호화 key')
    iv = Column(String(16), comment='암호화 iv')


class CertSms(Base, BaseMixin):
    __tablename__ = 'cert_sms'
    __table_args__ = {'comment': '문자 인증'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(16), nullable=False)
    mobile = Column(String(16), nullable=False)
    code = Column(String(6), nullable=False)
    status = Column(String(2), nullable=False, server_default=text("'R'"))
    ip = Column(String(50), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class Class(Base, BaseMixin):
    __tablename__ = 'class'
    __table_args__ = {'comment': '회원 등급'}

    code = Column(String(8), primary_key=True, comment='코드')
    name = Column(String(45), nullable=False, comment='이름')
    description = Column(String(256), comment='설명')


class CommonInfo(Base, BaseMixin):
    __tablename__ = 'common_info'
    __table_args__ = {'comment': '공통 정보'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), comment='이름')
    contents = Column(Text, comment='내용')
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    member_id = Column(ForeignKey('member.id'), index=True)

    member = relationship('Member')


class CouponGroup(Base, BaseMixin):
    __tablename__ = 'coupon_group'

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='이름')
    description = Column(String(255), nullable=False, comment='설명')
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    expire_days = Column(INTEGER(11), comment='사용 기한 (일 단위)')
    begin_date = Column(DateTime, comment='시작일')
    end_date = Column(DateTime, comment='만료일')
    begin_time = Column(Time, comment='사용 시작 시간')
    end_time = Column(Time, comment='사용 만료 시간')
    amount = Column(DECIMAL(10, 2), comment='금액할인')
    percent = Column(INTEGER(11), comment='퍼센트할인')
    min_price = Column(DECIMAL(10, 2), comment='최소주문금액')
    max_price = Column(DECIMAL(10, 2), comment='최대 할인 금액')
    issuer = Column(INTEGER(10), nullable=False, comment='발행자')
    auto = Column(String(45), comment='자동 발행 플래그 (join, birth)')
    publish_limit = Column(INTEGER(11), comment='발행 수 제한')
    publish_begin_date = Column(DateTime, comment='발행 시작일')
    publish_end_date = Column(DateTime, comment='발행 종료일')
    target = Column(Text, nullable=False, comment='발행 대상')
    type = Column(String(16), nullable=False, comment='product, shipping')
    image = Column(String(512))
    product_id = Column(ForeignKey('product.id'), index=True)

    product = relationship('Product')
    coupon_target = relationship('CouponTarget')
    coupon_publish_target = relationship('CouponPublishTarget')


class Customer(Base, BaseMixin):
    __tablename__ = 'customer'
    __table_args__ = {'comment': '회원'}

    id = Column(INTEGER(10), primary_key=True)
    email = Column(String(45), nullable=False, unique=True, comment='이메일')
    password = Column(String(256), comment='패스워드')
    name = Column(String(32), comment='이름')
    nickname = Column(String(32), comment='닉네임')
    mailling = Column(String(1), server_default=text("'N'"), comment='마케팅 메일 수신여부')
    sms = Column(String(1), server_default=text("'N'"), comment='마케팅 문자 수신여부')
    phone = Column(String(128), comment='전화번호')
    mobile = Column(String(128), comment='휴대전화번호')
    zipcode = Column(String(10), comment='우편번호')
    address = Column(String(256), comment='주소')
    address_detail = Column(String(128), comment='상세주소')
    sex = Column(String(1), comment='성별')
    birthday = Column(Date, comment='생년월일')
    recommend = Column(String(45), comment='추천인코드')
    status = Column(String(2), server_default=text("'Y'"), comment='상태')
    login_cnt = Column(INTEGER(11), server_default=text("0"), comment='로그인횟수')
    review_cnt = Column(INTEGER(11), server_default=text("0"), comment='상품리뷰횟수')
    order_cnt = Column(INTEGER(11), server_default=text("0"), comment='주문횟수')
    order_sum = Column(INTEGER(11), server_default=text("0"), comment='주문금액')
    lastlogin_date = Column(DateTime, server_default=text("current_timestamp()"), comment='마지막 로그인 일시')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    auth_yn = Column(String(1), server_default=text("'N'"), comment='본인인증 여부')
    adult_auth = Column(String(1), server_default=text("'N'"), comment='성인인증 여부')
    referer = Column(String(512), comment='유입경로 full_url')
    referer_domain = Column(String(256), comment='유입경로 도메인')
    join_platform = Column(String(3), comment='가입 플랫폼 (P, M, AOS, IOS)')
    marketing_agree_date = Column(DateTime, server_default=text("current_timestamp()"), comment='마케팅 수신 동의 일시')
    adult_auth_date = Column(DateTime, comment='성인인증 일시')
    sns_naver = Column(String(100))
    sns_kakao = Column(String(100))
    sns_google = Column(String(100))
    sns_facebook = Column(String(100))
    sns_apple = Column(String(100))
    sns_payco = Column(String(100))
    grade = Column(String(45), comment='등급')
    refresh_token = Column(String(512))

    member_store = relationship('MemberStore', back_populates='customer')


class FavoriteProductProperty(Base, BaseMixin):
    __tablename__ = 'favorite_product_property'
    __table_args__ = {'comment': '상품 속성'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='이름')
    type = Column(String(16), comment='타입')

    propertys = relationship('FavoriteProductPropertyDetail', back_populates="property")


class Member(Base, BaseMixin):
    __tablename__ = 'member'
    __table_args__ = {'comment': '회원'}

    id = Column(INTEGER(10), primary_key=True)
    email = Column(String(45), nullable=False, unique=True, comment='이메일')
    password = Column(String(256), comment='패스워드')
    name = Column(String(32), comment='이름')
    nickname = Column(String(32), comment='닉네임')
    mailling = Column(String(1), server_default=text("'N'"), comment='마케팅 메일 수신여부')
    sms = Column(String(1), server_default=text("'N'"), comment='마케팅 문자 수신여부')
    phone = Column(String(128), comment='전화번호')
    mobile = Column(String(128), comment='휴대전화번호')
    zipcode = Column(String(10), comment='우편번호')
    address = Column(String(256), comment='주소')
    address_detail = Column(String(128), comment='상세주소')
    sex = Column(String(1), comment='성별')
    birthday = Column(Date, comment='생년월일')
    recommend = Column(String(45), comment='추천인코드')
    status = Column(String(2), server_default=text("'Y'"), comment='상태')
    login_cnt = Column(INTEGER(11), server_default=text("0"), comment='로그인횟수')
    review_cnt = Column(INTEGER(11), server_default=text("0"), comment='상품리뷰횟수')
    order_cnt = Column(INTEGER(11), server_default=text("0"), comment='주문횟수')
    order_sum = Column(INTEGER(11), server_default=text("0"), comment='주문금액')
    lastlogin_date = Column(DateTime, server_default=text("current_timestamp()"), comment='마지막 로그인 일시')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    auth_yn = Column(String(1), server_default=text("'N'"), comment='본인인증 여부')
    adult_auth = Column(String(1), server_default=text("'N'"), comment='성인인증 여부')
    referer = Column(String(512), comment='유입경로 full_url')
    referer_domain = Column(String(256), comment='유입경로 도메인')
    join_platform = Column(String(3), comment='가입 플랫폼 (P, M, AOS, IOS)')
    marketing_agree_date = Column(DateTime, server_default=text("current_timestamp()"), comment='마케팅 수신 동의 일시')
    adult_auth_date = Column(DateTime, comment='성인인증 일시')
    sns_naver = Column(String(100))
    sns_kakao = Column(String(100))
    sns_google = Column(String(100))
    sns_facebook = Column(String(100))
    sns_apple = Column(String(100))
    sns_payco = Column(String(100))
    bank = Column(String(16), comment='환불용 계좌 은행')
    account = Column(String(45), comment='환불용 계좌')
    admin_yn = Column(String(1), nullable=False, server_default=text("'N'"), comment='관리자 여부')
    otp = Column(String(40))
    grade = Column(String(45), comment='등급')
    refresh_token = Column(String(512))
    partner = Column(String(2), server_default=text("'N'"), comment='파트너 회원 [N, Y, R(승인대기)]')
    memo = Column(String(255), comment='관리자 메모')
    confirm_pass = Column(String(16), comment='직원 확인용 패스워드')
    shop_yn = Column(String(2), server_default=text("'N'"), comment='매장 여부')

    company = relationship('MemberCompany', back_populates="member", uselist=False)
    shop = relationship('Shop', back_populates="member", uselist=False)
    store = relationship('Store', back_populates="member")
    classes = relationship('MemberClass', back_populates="member")
    log = relationship('LogMember', back_populates="member")


class Menu(Base, BaseMixin):
    __tablename__ = 'menu'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)
    depth = Column(INTEGER(11), nullable=False)
    menu_id = Column(ForeignKey('menu.id', ondelete='CASCADE'), index=True)

    menu = relationship('Menu', remote_side=[id])


class NoticeInfoTemplate(Base, BaseMixin):
    __tablename__ = 'notice_info_template'
    __table_args__ = {'comment': '상품정보제공고시 템플릿'}

    id = Column(INTEGER(10), primary_key=True)
    category = Column(String(45), nullable=False)
    item = Column(String(255), nullable=False)
    num = Column(INTEGER(10))


class OptionValue(Base, BaseMixin):
    __tablename__ = 'option_value'
    __table_args__ = {'comment': '옵션값 모음'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(32), comment='타입')
    name = Column(String(64), comment='이름')
    value = Column(String(128), comment='값')
    sort = Column(INTEGER(11), server_default=text("99"), comment='순서')


class Permission(Base, BaseMixin):
    __tablename__ = 'permission'
    __table_args__ = {'comment': '권한'}

    code = Column(String(128), primary_key=True, comment='코드')
    name = Column(String(45), nullable=False, comment='이름')
    description = Column(String(255), nullable=False, comment='설명')
    type = Column(String(2), nullable=False, comment='권한 타입\\nMember = B, Admin = A')
    category = Column(String(45))
    group = Column(String(45))


class SettingValue(Base, BaseMixin):
    __tablename__ = 'setting_value'
    __table_args__ = {'comment': '설정 값'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(32), comment='타입')
    name = Column(String(64), comment='이름')
    value = Column(Text, comment='값')
    description = Column(String(512), comment='설명')


class SettlementRaw(Base, BaseMixin):
    __tablename__ = 'settlement_raw'

    id = Column(INTEGER(10), primary_key=True)
    target_date = Column(Date, nullable=False)
    order_id = Column(BIGINT(20), nullable=False)
    order_product_id = Column(ForeignKey('order_product.id'), nullable=False, index=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    pg_type = Column(String(45), nullable=False)
    supply_price = Column(DECIMAL(10, 2), nullable=False, server_default=text("0.00"), comment='공급가')
    margin_price = Column(DECIMAL(10, 2), nullable=False, server_default=text("0.00"), comment='마진가')
    processed = Column(DateTime)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)

    order_product = relationship('OrderProduct')
    product = relationship('Product')
    store = relationship('Store')


class ShippingInfo(Base, BaseMixin):
    __tablename__ = 'shipping_info'
    __table_args__ = {'comment': '배송 정보'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='이름')
    type = Column(String(10), nullable=False, comment='배송방법 (택배,퀵서비스,화물배송,매장수령)')
    pay_type = Column(String(10), nullable=False, comment='지불방법 (선불,착불)')
    calc_type = Column(String(10), nullable=False, comment='계산타입 [묶음계산-묶음배송/개별계산-개별배송 /무료계산-묶음배송]')
    return_cost = Column(INTEGER(11), server_default=text("0"), comment='반품비')
    change_cost = Column(INTEGER(11), server_default=text("0"), comment='교환비')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    member_id = Column(ForeignKey('member.id'), index=True)

    member = relationship('Member')
    shipping_costs = relationship('ShippingCost')


class Catalog(Base, BaseMixin):
    __tablename__ = 'catalog'
    __table_args__ = {'comment': '카탈로그'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), comment='이름')
    description = Column(String(255), comment='설명')
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    open = Column(String(2), nullable=False, server_default=text("'N'"), comment='열람 범위')
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    member = relationship('Member')


class ClassPermission(Base, BaseMixin):
    __tablename__ = 'class_permission'
    __table_args__ = (
        Index('u_class_permission_class_code', 'class_code', 'permission_code', unique=True),
        {'comment': '회원등급-권한 연결'}
    )

    id = Column(INTEGER(11), primary_key=True)
    class_code = Column(ForeignKey('class.code'), nullable=False, index=True)
    permission_code = Column(ForeignKey('permission.code'), nullable=False, index=True)
    target = Column(String(16), nullable=False, server_default=text("'*'"))

    class_ = relationship('Class')
    permission = relationship('Permission')


class Coupon(Base, BaseMixin):
    __tablename__ = 'coupon'
    __table_args__ = {'comment': '쿠폰'}

    id = Column(BIGINT(20), primary_key=True)
    code = Column(String(45), nullable=False, comment='코드')
    name = Column(String(45), nullable=False, comment='이름')
    description = Column(String(255), nullable=False, comment='설명')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"), comment='등록일')
    use_date = Column(DateTime, comment='사용일')
    begin_date = Column(DateTime, comment='시작일')
    end_date = Column(DateTime, comment='만료일')
    use_yn = Column(String(1), server_default=text("'N'"), comment='사용 여부')
    amount = Column(DECIMAL(10, 2), comment='금액할인')
    percent = Column(INTEGER(11), comment='퍼센트할인')
    min_price = Column(DECIMAL(10, 2), comment='최소주문금액')
    max_price = Column(DECIMAL(10, 2), comment='최대 할인 금액')
    issuer = Column(ForeignKey('member.id'), nullable=False, index=True, comment='발행자')
    coupon_group_id = Column(ForeignKey('coupon_group.id'), nullable=False, index=True)
    target = Column(Text, nullable=False, comment='발행 대상')
    type = Column(String(16), nullable=False, comment='product, shipping')
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('product.id'), index=True)

    coupon_group = relationship('CouponGroup')
    customer = relationship('Customer')
    member = relationship('Member')
    product = relationship('Product')


class FavoriteProductPropertyDetail(Base, BaseMixin):
    __tablename__ = 'favorite_product_property_detail'
    __table_args__ = {'comment': '상품 속성 상세'}

    id = Column(INTEGER(10), primary_key=True)
    value = Column(String(128), nullable=False, comment='속성값')
    price = Column(DECIMAL(10, 2), nullable=False, comment='가격')
    code = Column(String(45), nullable=False)
    favorite_product_property_id = Column(ForeignKey('favorite_product_property.id'), nullable=False, index=True)

    property = relationship('FavoriteProductProperty', back_populates="propertys")


class LogMember(Base, BaseMixin):
    __tablename__ = 'log_member'
    __table_args__ = {'comment': '상품 로그'}

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    action = Column(String(16), nullable=False)
    msg = Column(Text, nullable=False)
    writer = Column(String(64), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    del_column = Column('del', String(1), nullable=False, server_default=text("'N'"))

    member = relationship('Member', back_populates="log")


class MemberClass(Base, BaseMixin):
    __tablename__ = 'member_class'
    __table_args__ = {'comment': '회원-등급 연결'}

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    class_code = Column(ForeignKey('class.code'), nullable=False, index=True)
    grade = Column(String(45), comment='등급')

    class_ = relationship('Class')
    member = relationship('Member', back_populates="classes")


class MemberCompany(Base, BaseMixin):
    __tablename__ = 'member_company'
    __table_args__ = {'comment': '회원 사업자 정보'}

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(45), comment='이름')
    ceo = Column(String(45), comment='대표자명')
    reg_no = Column(String(45), comment='사업자등록번호')
    biz_type = Column(String(45), comment='업태')
    biz_item = Column(String(45), comment='업종')
    zipcode = Column(String(10), comment='우편번호')
    address = Column(String(256), comment='주소')
    address_detail = Column(String(128), comment='주소상세')
    phone = Column(String(32), comment='대표자 전화번호')
    mobile = Column(String(32), comment='대표자 휴대전화')
    corp_type = Column(String(3), nullable=False, comment='사업자 종류 (개인(P),법인(B),개인사업자(PB),개인사업자간이과세(PBS))')
    corp_number = Column(String(45), comment='법인번호(주민번호)')
    tax_email = Column(String(128), comment='계산서 이메일')
    bank = Column(String(16), comment='은행')
    account = Column(String(45), comment='계좌번호')
    bank_user = Column(String(45), comment='예금주')
    photo_reg = Column(String(512), comment='사업자등록증 사진')
    photo_bank = Column(String(512), comment='통장 사본 사진')
    status = Column(String(2), nullable=False, server_default=text("'R'"), comment='사업자 승인 여부')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    manager_name = Column(String(32), comment='담당자명')
    manager_phone = Column(String(32), comment='담당자 전화번호')
    manager_mobile = Column(String(32), comment='담당자 휴대전화')
    manager_email = Column(String(128), comment='담당자 이메일')
    settlement_name = Column(String(32), comment='정산 담당자명')
    settlement_phone = Column(String(32), comment='정산 담당자 전화번호')
    settlement_mobile = Column(String(32), comment='정산 담당자 휴대전화')
    settlement_email = Column(String(128), comment='정산 담당자 이메일')
    cs_name = Column(String(32), comment='CS 담당자명')
    cs_phone = Column(String(32), comment='CS 담당자 전화번호')
    cs_mobile = Column(String(32), comment='CS 담당자 휴대전화')
    cs_email = Column(String(128), comment='CS 담당자 이메일')
    network_reg_no = Column(String(24), comment='통신판매업 신고번호')

    member = relationship('Member', back_populates="company")


class MemberMember(Base, BaseMixin):
    __tablename__ = 'member_member'
    __table_args__ = (
        Index('u_member_member_link', 'member_id', 'pid', unique=True),
        {'comment': '회원-회원 연결'}
    )

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    pid = Column(ForeignKey('member.id'), nullable=False, index=True, comment='상위 회원')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    member = relationship('Member', primaryjoin='MemberMember.member_id == Member.id')
    member1 = relationship('Member', primaryjoin='MemberMember.pid == Member.id')


class MemberPermission(Base, BaseMixin):
    __tablename__ = 'member_permission'
    __table_args__ = (
        Index('u_member_permission_member_code', 'member_id', 'permission_code', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    permission_code = Column(ForeignKey('permission.code'), nullable=False, index=True)
    target = Column(String(16), nullable=False, server_default=text("'*'"))
    exclude = Column(String(1), server_default=text("'N'"), comment='제외 플래그')

    member = relationship('Member')
    permission = relationship('Permission')


class SettlementData(Base, BaseMixin):
    __tablename__ = 'settlement_data'

    id = Column(BIGINT(20), primary_key=True)
    target_date = Column(Date, nullable=False)
    account_raw_id = Column(ForeignKey('settlement_raw.id'), nullable=False, index=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    type = Column(String(2), nullable=False, comment='S(공급가), C(수수료)')
    sequence = Column(INTEGER(11), nullable=False, comment='정산 순번')
    target_amount = Column(DECIMAL(10, 2), nullable=False, comment='정산 대상 금액')
    amount = Column(DECIMAL(10, 2), nullable=False, comment='정산 금액')
    commission_type = Column(String(2))
    commission_value = Column(DECIMAL(10, 2))
    payment_date = Column(DateTime, comment='정산 지급일')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    pg_provider = Column(String(16))
    pg_kind = Column(String(16))
    status = Column(String(2), server_default=text("'R'"), comment='상태')
    reject = Column(String(255), comment='반려 사유')
    tax = Column(String(1))
    payment = Column(String(2), comment='지급 방식')
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    account_raw = relationship('SettlementRaw')
    member = relationship('Member')


class MenuClass(Base, BaseMixin):
    __tablename__ = 'menu_class'

    id = Column(INTEGER(11), primary_key=True)
    menu_id = Column(ForeignKey('menu.id', ondelete='CASCADE'), nullable=False, index=True)
    class_code = Column(ForeignKey('class.code', ondelete='CASCADE'), nullable=False, index=True)

    _class = relationship('Class')
    menu = relationship('Menu')


class SettlementShip(Base, BaseMixin):
    __tablename__ = 'settlement_ship'

    id = Column(INTEGER(10), primary_key=True)
    target_date = Column(Date, nullable=False)
    order_id = Column(BIGINT(20), nullable=False)
    order_shipping_id = Column(BIGINT(20), nullable=False)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    type = Column(String(2), nullable=False, comment='S(공급가), C(수수료)')
    sequence = Column(INTEGER(11), nullable=False, comment='정산 순번')
    target_amount = Column(DECIMAL(10, 2), nullable=False, comment='정산 대상 금액')
    amount = Column(DECIMAL(10, 2), nullable=False, comment='정산 금액')
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    payment_date = Column(DateTime, comment='정산 지급일')
    reg_date = Column(DateTime, server_default=text("current_timestamp()"))
    commission_type = Column(String(2))
    commission_value = Column(DECIMAL(10, 2))
    pg_provider = Column(String(16))
    pg_kind = Column(String(16))
    status = Column(String(2), server_default=text("'R'"), comment='상태')
    reject = Column(String(255), comment='반려 사유')
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    member = relationship('Member')
    store = relationship('Store')


class ProductRequest(Base, BaseMixin):
    __tablename__ = 'product_request'

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    memo = Column(String(255))
    status = Column(String(2), nullable=False, server_default=text("'R'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    manager = Column(ForeignKey('member.id'), index=True, comment='담당자')

    member = relationship('Member', primaryjoin='ProductRequest.member_id == Member.id')
    manager_member = relationship('Member', primaryjoin='ProductRequest.manager == Member.id')
    store = relationship('Store', primaryjoin='ProductRequest.store_code == Store.code')
    products = relationship('Product', secondary='product_request_prd')


class Product(Base, BaseMixin):
    __tablename__ = 'product'
    __table_args__ = {'comment': '상품'}

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True, comment='등록 회원')
    name = Column(String(100), nullable=False, comment='상품명')
    type = Column(String(16), comment='타입')
    status = Column(String(16), nullable=False, server_default=text("'N'"), comment='상태')
    view_yn = Column(String(1), comment='노출 여부')
    code = Column(String(255), nullable=False, unique=True)
    summary = Column(String(255), comment='간략 설명')
    keyword = Column(Text, comment='검색 키워드')
    contents = Column(Text, comment='상품 내용')
    tax = Column(String(8), comment='과세 여부')
    min_purchase_limit = Column(String(10), comment='최소 구매수량')
    max_purchase_limit = Column(String(10), comment='최대 구매수량')
    adult = Column(String(1), server_default=text("'N'"), comment='성인 인증 필요 여부')
    hscode = Column(String(16), comment='수출입코드')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    ipcc_yn = Column(String(1), server_default=text("'N'"), comment='개인통관고유부호 사용 여부')
    cancel_yn = Column(String(1), server_default=text("'Y'"), comment='청약 철회 여부')
    confirm = Column(String(1), server_default=text("'N'"), comment='승인 여부')
    video = Column(String(255))
    memo = Column(Text)
    common_info_id = Column(ForeignKey('common_info.id'), index=True, comment='공통정보')
    shipping_info_id = Column(ForeignKey('shipping_info.id'), index=True, comment='배송정보')
    writer_id = Column(ForeignKey('member.id'), nullable=False, index=True, comment='작성자')
    inven_use = Column(String(1), nullable=False, server_default=text("'Y'"), comment='재고 사용')
    coupon_yn = Column(String(1), nullable=False, server_default=text("'Y'"), comment='쿠폰 사용 여부')
    option_use = Column(String(1), server_default=text("'N'"), comment='옵션 사용 여부')
    barcode = Column(String(45))
    user_limit = Column(INTEGER(11), comment='1인당 구매횟수 제한')
    use_end_period = Column(INTEGER(11), comment='비실물 상품 사용 기한 (일)')
    use_end_date = Column(DateTime, comment='비실물 상품 사용 기한 (지정 일시)')
    sale_start_date = Column(DateTime, comment='판매 가능 시간 시작')
    sale_end_date = Column(DateTime, comment='판매 가능 시간 종료')
    sale_start_time = Column(Time, comment='판매 가능 일(시각) 시작')
    sale_end_time = Column(Time, comment='판매 가능 일(시각) 종료')
    tel = Column(String(16))
    address = Column(String(128))
    address_detail = Column(String(255))
    lat = Column(String(32))
    lng = Column(String(32))
    subtitle = Column(String(100), comment='부제목')
    view_inventory = Column(String(1), server_default=text("'N'"), comment='재고 노출여부')
    view_end_time = Column(String(1), server_default=text("'N'"), comment='판매 종료시간 노출여부')
    reject = Column(String(255), comment='반려 사유')
    pg_provider = Column(String(256), comment='PG사 선택, 구분자 |, 없으면 전체')
    api_provider = Column(String(64), comment='외부업체 연동 구분')
    api_goods_id = Column(Text, comment='외부업체 상품 ID')
    use_place = Column(Text, comment='E쿠폰 사용처')
    user_limit_reset = Column(String(128), comment='1인당 구매횟수 제한 초기화 방법')
    resale = Column(String(2), server_default=text("'N'"), comment='사입 여부')

    common_info = relationship('CommonInfo')
    member = relationship('Member', primaryjoin='Product.member_id == Member.id')
    shipping_info = relationship('ShippingInfo')
    writer = relationship('Member', primaryjoin='Product.writer_id == Member.id')
    options = relationship('ProductOption', primaryjoin="and_(Product.id==ProductOption.product_id, ProductOption.status=='Y')", back_populates="product")
    photos = relationship('ProductPhoto', back_populates="product")
    categories = relationship('Category', secondary="product_category")
    brands = relationship('Brand', secondary="product_brand")
    badges = relationship('Badge', secondary="product_badge")
    reviews = relationship('ProductReview', back_populates="product")


class ProductRequestPrd(Base, BaseMixin):
    __tablename__ = 'product_request_prd'
    __table_args__ = (
        Index('u_product_request_product', 'product_request_id', 'product_id', unique=True),
        {'comment': '상품요청-상품 연결'}
    )

    product_request_id = Column(ForeignKey('product_request.id'), primary_key=True, nullable=False, index=True)
    product_id = Column(ForeignKey('product.id'), primary_key=True, nullable=False, index=True)


class ShippingCost(Base, BaseMixin):
    __tablename__ = 'shipping_cost'
    __table_args__ = {'comment': '배송 금액'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(10), comment='배송비 타입 free, fix, cost, ea, weight')
    category = Column(String(16), comment='basic(기본), add(추가)')
    cost = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='비용')
    section_start = Column(INTEGER(11), comment='구간시작')
    section_end = Column(INTEGER(11), comment='구간끝')
    section_repeat = Column(INTEGER(11), comment='구간 반복')
    shipping_info_id = Column(ForeignKey('shipping_info.id'), nullable=False, index=True)

    shipping_info = relationship('ShippingInfo', back_populates="shipping_costs")


class Store(Base, BaseMixin):
    __tablename__ = 'store'
    __table_args__ = {'comment': '상점'}

    code = Column(String(16), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True, comment='상점 생성 회원')
    title = Column(String(45), comment='상점명')
    type = Column(String(2), comment='폐쇄몰 오픈몰')
    domain = Column(String(128))
    status = Column(String(2), nullable=False, server_default=text("'R'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    layout = Column(Text, comment='홈 레이아웃 데이터 (Json)')
    auto_join = Column(String(2), nullable=False, server_default=text("'Y'"), comment='회원가입 자동승인')
    logo_pc = Column(String(512))
    logo_mobile = Column(String(512))
    favicon = Column(String(512))
    info = Column(Text)
    dupl_store = Column(String(16), comment='복제 대상 상점 코드')
    able_target_use = Column(String(2), nullable=False, server_default=text("'N'"))
    verify_code = Column(String(32), comment='가입방식 고정일때 사용하는 가입 검증 코드')
    exclude_menu = Column(Text, comment='상점에서 보이지 않을 메뉴 , split')
    group = Column(String(32))
    prd_pg_opt_use = Column(String(2), comment='상품 PG 옵션 사용 여부')
    meal_opt_use = Column(String(2), server_default=text("'N'"), comment='식권 결제 옵션 사용 여부')
    meal_opt_limit_use = Column(String(2), server_default=text("'N'"), comment='식권 결제 사용시간 제한 사용 여부')
    meal_opt_limit_time = Column(String(512), server_default=text("'[]'"), comment='식권 결제 사용시간 제한 시간 정보')
    meal_opt_cancel_use = Column(String(2), server_default=text("'N'"), comment='식권 결제 일괄 취소 기능 사용 여부')
    keyword = Column(Text)
    copy_setting = Column(String(16), comment='설정 복사 대상 상점코드')

    member = relationship('Member', back_populates="store")


class AbleTarget(Base, BaseMixin):
    __tablename__ = 'able_target'
    __table_args__ = (
        Index('able_target_store_code_unique_value_uindex', 'store_code', 'unique_value', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    unique_value = Column(String(45))
    name = Column(String(45))
    mobile = Column(String(128))
    used = Column(String(1), server_default=text("'N'"))

    store = relationship('Store')


class CatalogProduct(Base, BaseMixin):
    __tablename__ = 'catalog_product'
    __table_args__ = (
        Index('u_ catalog_product', 'catalog_id', 'product_id', unique=True),
        {'comment': '카탈로그-상품 연결'}
    )

    id = Column(BIGINT(20), primary_key=True)
    catalog_id = Column(ForeignKey('catalog.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    variation = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='가격변동값')

    catalog = relationship('Catalog')
    product = relationship('Product')


class CatalogStore(Base, BaseMixin):
    __tablename__ = 'catalog_store'
    __table_args__ = (
        Index('u_catalog_store', 'catalog_id', 'store_code', unique=True),
        {'comment': '카탈로그-상점 연결'}
    )

    id = Column(INTEGER(10), primary_key=True)
    catalog_id = Column(ForeignKey('catalog.id'), nullable=False, index=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)

    catalog = relationship('Catalog')
    store = relationship('Store')


class Dept(Base, BaseMixin):
    __tablename__ = 'dept'
    __table_args__ = {'comment': '관리자 부서'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='이름')
    description = Column(String(255), comment='설명')
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    member_company_id = Column(ForeignKey('member_company.id'), nullable=False, index=True)
    pid = Column(ForeignKey('dept.id'), index=True)

    member_company = relationship('MemberCompany')
    parent = relationship('Dept', remote_side=[id])


class ExtraInfo(Base, BaseMixin):
    __tablename__ = 'extra_info'
    __table_args__ = {'comment': '추가 정보'}

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    category = Column(String(45), nullable=False, comment='분류')
    contents = Column(String(255), nullable=False, comment='내용')

    product = relationship('Product')


class Faq(Base, BaseMixin):
    __tablename__ = 'faq'
    __table_args__ = {'comment': '자주하는질문'}

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(128), nullable=False, comment='제목')
    contents = Column(Text, nullable=False, comment='내용')
    category = Column(String(45), comment='분류')
    status = Column(String(2), nullable=False, server_default=text("'N'"), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    target = Column(String(16), nullable=False, comment='노출 대상 (admin, partner, customer)')
    store_code = Column(ForeignKey('store.code'), index=True, comment='상점에 노출되는 FAQ인 경우')
    file = Column(String(512))

    store = relationship('Store')


class LogStore(Base, BaseMixin):
    __tablename__ = 'log_store'
    __table_args__ = {'comment': '상점 로그'}

    id = Column(INTEGER(10), primary_key=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    action = Column(String(16), nullable=False)
    msg = Column(Text, nullable=False)
    writer = Column(String(64), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    _del = Column('del', String(1), nullable=False, server_default=text("'N'"))

    store = relationship('Store')


class FaqCategory(Base, BaseMixin):
    __tablename__ = 'faq_category'
    __table_args__ = {'comment': '자주하는질문 분류'}

    id = Column(INTEGER(10), primary_key=True)
    category = Column(String(45), nullable=False, comment='분류')
    sort = Column(INTEGER(11), server_default=text("99"), comment='순서')


class LogProduct(Base, BaseMixin):
    __tablename__ = 'log_product'
    __table_args__ = {'comment': '상품 로그'}

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    action = Column(String(16), nullable=False)
    msg = Column(Text, nullable=False)
    writer = Column(String(64), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    _del = Column('del', String(1), nullable=False, server_default=text("'N'"))

    product = relationship('Product')


class MemberStore(Base, BaseMixin):
    __tablename__ = 'member_store'
    __table_args__ = (
        Index('u_customer_store', 'customer_id', 'store_code', unique=True),
        {'comment': '이용 신청 상점'}
    )

    id = Column(INTEGER(10), primary_key=True)
    confirm = Column(String(1), nullable=False, server_default=text("'N'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    store_code = Column(ForeignKey('store.code'), nullable=False, unique=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    recommander_member_id = Column(ForeignKey('member.id'), index=True, comment='상점 이용 추천 회원')
    value = Column(String(45))

    customer = relationship('Customer', primaryjoin="Customer.id == MemberStore.customer_id", back_populates='member_store')
    recommander_member = relationship('Member')
    store = relationship('Store')


class Notice(Base, BaseMixin):
    __tablename__ = 'notice'
    __table_args__ = {'comment': '공지사항'}

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(128), nullable=False, comment='제목')
    contents = Column(Text, nullable=False, comment='내용')
    pin = Column(String(1), server_default=text("'N'"), comment='상위 고정')
    sort = Column(INTEGER(11), server_default=text("99"), comment='순서')
    status = Column(String(2), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    target = Column(String(16), nullable=False, comment='노출 대상 (admin, partner, customer)')
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    store_code = Column(ForeignKey('store.code'), index=True)
    file = Column(String(512))

    member = relationship('Member')
    store = relationship('Store')


class NoticeInfo(Base, BaseMixin):
    __tablename__ = 'notice_info'
    __table_args__ = {'comment': '상품정보제공고시'}

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    item = Column(String(255), nullable=False, comment='품목')
    category = Column(String(45), nullable=False, comment='항목')
    contents = Column(String(255), nullable=False, comment='내용')
    sort = Column(INTEGER(11), nullable=False, server_default=text("99"), comment='순서')

    product = relationship('Product')


class Order(Base, BaseMixin):
    __tablename__ = 'order'
    __table_args__ = {'comment': '주문'}

    id = Column(BIGINT(20), primary_key=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    origin_order_id = Column(ForeignKey('order.id'), index=True, comment='연결된 주문')
    origin_amount = Column(DECIMAL(10, 2), nullable=False, comment='정상 판매가 금액')
    raw_amount = Column(DECIMAL(10, 2), nullable=False, comment='결제 대상 금액')
    final_amount = Column(DECIMAL(10, 2), nullable=False, comment='최종 결제 금액')
    tex_free_amount = Column(DECIMAL(10, 2), comment='비과세 금액')
    tax_rate = Column(String(3), comment='부가세율')
    discount = Column(DECIMAL(10, 2), comment='할인 금액')
    status = Column(String(3), nullable=False, comment='상태')
    user_name = Column(String(32), comment='주문자명')
    user_phone = Column(String(20), comment='주문자 전화번호')
    user_mobile = Column(String(20), comment='주문자 휴대전화')
    user_email = Column(String(100), comment='주문자 이메일')
    recipient_name = Column(String(32), comment='수령인')
    recipient_phone = Column(String(20), comment='수령인 전화번호')
    recipient_mobile = Column(String(20), comment='수령인 휴대전화')
    shipping_cost = Column(DECIMAL(10, 2), comment='배송비결제금액')
    shipping_cost_post = Column(DECIMAL(10, 2), comment='착불배송비')
    shipping_condition = Column(String(255), comment='배송비 조건')
    shipping_msg = Column(String(255), comment='배송메세지')
    zipcode = Column(String(10), comment='우편번호')
    address = Column(String(255), comment='주소')
    address_detail = Column(String(128), comment='주소상세')
    coupon_discount = Column(DECIMAL(10, 2), comment='쿠폰할인금액')
    step_type = Column(String(10), comment='(direct:바로구매, cart:장바구니구매)')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    client_type = Column(String(10), comment='P, M, AOS, IOS')
    referer = Column(String(45), comment='유입매체')
    referer_url = Column(String(255), comment='유입 url')
    total_ea = Column(INTEGER(11), comment='총삼품수')
    total_kind = Column(INTEGER(11), comment='총삼품종류')
    ipcc_code = Column(String(45), comment='개인통관고유번호')
    ip = Column(String(50))
    settlement_date = Column(DateTime, comment='정산 처리일시')
    password = Column(String(256), comment='비회원 주문일 경우 비밀번호')
    cert_id = Column(ForeignKey('cert.id'), index=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)

    cert = relationship('Cert')
    customer = relationship('Customer')
    origin_order = relationship('Order', remote_side=[id])
    store = relationship('Store')
    products = relationship('OrderProduct', back_populates="order")
    pg_info = relationship('PgInfo', uselist=False, back_populates="order")


class PgInfo(Base, BaseMixin):
    __tablename__ = 'pg_info'

    id = Column(INTEGER(10), primary_key=True)
    order_id = Column(ForeignKey('order.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    provider = Column(String(16), nullable=False, comment='PG사')
    kind = Column(String(16), nullable=False, comment='결제 방법')
    tid = Column(String(45), comment='PG사 트랜잭션 ID')
    amount = Column(INTEGER(11), nullable=False)
    remain_amount = Column(INTEGER(11), nullable=False, server_default=text("0"))
    app_time = Column(String(16), nullable=False, comment='승인 시간')
    deposit_yn = Column(String(1), server_default=text("'N'"), comment='무통장 입금 여부')
    deposit_date = Column(DateTime, comment='무통장 입금 일시')
    deposit_name = Column(String(45), comment='무통장 입금자명')
    bank_account = Column(String(100), comment='무통장 입금계좌정보')
    virtual_account = Column(String(255), comment='가상계좌정보')
    virtual_date = Column(DateTime, comment='가상계좌입금제한일')
    card_app_num = Column(String(45), comment='신용카드 승인번호')
    card_name = Column(String(45), comment='신용카드 발급사명')
    card_no = Column(String(45), comment='신용카드 번호')
    card_quota = Column(String(8), comment='신용카드 할부 기간')
    card_partcanc_yn = Column(String(2), comment='신용카드 부분취소 가능 유무')
    card_bin_type_01 = Column(String(2), comment='카드구분 개인: 0 / 법인: 1')
    card_bin_type_02 = Column(String(2), comment='카드구분 일반: 0 / 체크: 1')
    cash_authno = Column(String(16), comment='현금영수증 승인번호')
    cash_no = Column(String(16), comment='현금영수증 거래번호')
    bankname = Column(String(20), comment='은행 명')
    commid = Column(String(8), comment='휴대폰 결제 통신사 코드')
    mobile_no = Column(String(11), comment='휴대폰 결제 휴대폰 번호')
    cancel_type = Column(String(10), comment='취소 타입(all, part)')
    cancel_date = Column(DateTime, comment='취소 시각')
    cancel_mny = Column(INTEGER(11), comment='취소 금액')
    cancel_part_seq = Column(String(32), comment='부분취소 일련번호')
    cancel_key = Column(String(128), comment='취소 키')
    raw_data = Column(Text, nullable=False, comment='결제 데이터')

    order = relationship('Order', uselist=False, back_populates="pg_info")
    pg_info_sub = relationship('PgInfoSub', back_populates="pg_info")


class OrderSheet(Base, BaseMixin):
    __tablename__ = 'order_sheet'
    __table_args__ = {'comment': '주문서'}

    id = Column(String(36), primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    step_type = Column(String(10), comment='생성 경로')

    customer = relationship('Customer')
    store = relationship('Store')

    products = relationship("OrderSheetProduct", back_populates="order_sheet")


class OrderSheetProduct(Base, BaseMixin):
    __tablename__ = 'order_sheet_product'
    __table_args__ = {'comment': '주문서 상품'}

    order_sheet_id = Column(ForeignKey('order_sheet.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    product_option_id = Column(ForeignKey('product_option.id'), primary_key=True, nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False, comment='금액')
    ea = Column(INTEGER(11), nullable=False, comment='수량')

    order_sheet = relationship('OrderSheet')
    product_option = relationship('ProductOption')


class PgCancel(Base, BaseMixin):
    __tablename__ = 'pg_cancel'

    id = Column(INTEGER(10), primary_key=True)
    pg_info_order_id = Column(BIGINT(20), nullable=False, index=True)
    tno = Column(String(45))
    type = Column(String(10), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    amount = Column(INTEGER(11), nullable=False)
    remain = Column(INTEGER(11))
    part_seq = Column(String(20))


class ProductBadge(Base, BaseMixin):
    __tablename__ = 'product_badge'
    __table_args__ = (
        Index('u_product_badge', 'product_id', 'badge_id', unique=True),
        {'comment': '상품-뱃지 연결'}
    )

    product_id = Column(ForeignKey('product.id'), primary_key=True, nullable=False, index=True)
    badge_id = Column(ForeignKey('badge.id'), primary_key=True, nullable=False, index=True)


class ProductBrand(Base, BaseMixin):
    __tablename__ = 'product_brand'
    __table_args__ = (
        Index('u_product_brand', 'product_id', 'brand_id', unique=True),
        {'comment': '상품-브랜드 연결'}
    )

    product_id = Column(ForeignKey('product.id'), primary_key=True, nullable=False, index=True)
    brand_id = Column(ForeignKey('brand.id'), primary_key=True, nullable=False, index=True)


class ProductCategory(Base, BaseMixin):
    __tablename__ = 'product_category'
    __table_args__ = (
        Index('u_product_category', 'product_id', 'category_id', unique=True),
        {'comment': '상품-분류 연결'}
    )

    product_id = Column(ForeignKey('product.id'), primary_key=True, nullable=False, index=True)
    category_id = Column(ForeignKey('category.id'), primary_key=True, nullable=False, index=True)


class ProductGroup(Base, BaseMixin):
    __tablename__ = 'product_group'
    __table_args__ = (
        Index('u_pid_product_id', 'pid', 'product_id', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    pid = Column(ForeignKey('product.id'), nullable=False, index=True, comment='그룹 상품')
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True, comment='대상 상품')

    parent = relationship('Product', primaryjoin='ProductGroup.pid == Product.id')
    product = relationship('Product', primaryjoin='ProductGroup.product_id == Product.id')


class ProductOption(Base, BaseMixin):
    __tablename__ = 'product_option'
    __table_args__ = {'comment': '상품 옵션'}

    id = Column(INTEGER(10), primary_key=True)
    code = Column(String(45), comment='코드')
    supply_price = Column(DECIMAL(10, 2), nullable=False, comment='공급가')
    origin_price = Column(DECIMAL(10, 2), nullable=False, comment='정상가')
    selling_price = Column(DECIMAL(10, 2), nullable=False, comment='판매가')
    view_yn = Column(String(1), nullable=False, server_default=text("'Y'"), comment='노출 여부')
    default_yn = Column(String(45), nullable=False, server_default=text("'N'"), comment='기본 값 여부')
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    weight = Column(DECIMAL(5, 2), comment='무게')
    status = Column(String(2), server_default=text("'Y'"), comment='상태')
    option_title = Column(String(100))
    option_1 = Column(String(100))
    option_2 = Column(String(100))
    option_3 = Column(String(100))
    option_4 = Column(String(100))
    option_5 = Column(String(100))
    option_code_1 = Column(String(100))
    option_code_2 = Column(String(100))
    option_code_3 = Column(String(100))
    option_code_4 = Column(String(100))
    option_code_5 = Column(String(100))
    option_tmp_price = Column(String(100))

    product = relationship('Product', back_populates="options")
    inventory = relationship('Inventory', back_populates="option", uselist=False)


class ProductPhoto(Base, BaseMixin):
    __tablename__ = 'product_photo'
    __table_args__ = {'comment': '상품 사진'}

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    uri = Column(String(256), comment='URI')
    reg_dt = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_dt = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    product_option_id = Column(ForeignKey('product_option.id'), index=True)

    product = relationship('Product', back_populates="photos")
    product_option = relationship('ProductOption')


class ProductQna(Base, BaseMixin):
    __tablename__ = 'product_qna'
    __table_args__ = {'comment': '상품 문의'}

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(128), nullable=False, comment='제목')
    contents = Column(Text, nullable=False, comment='내용')
    product_id = Column(ForeignKey('product.id'), index=True)
    status = Column(String(2), server_default=text("'Y'"), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    product_qna_id = Column(ForeignKey('product_qna.id'), index=True, comment='답변일 경우 질문 product qna id')
    admin_id = Column(INTEGER(10))
    a_member_id = Column(ForeignKey('member.id'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True)
    secret = Column(String(1), server_default=text("'N'"))
    customer_id = Column(ForeignKey('customer.id'), index=True)

    a_member = relationship('Member', primaryjoin='ProductQna.a_member_id == Member.id')
    customer = relationship('Customer')
    product = relationship('Product')
    product_qna = relationship('ProductQna', remote_side=[id])
    store = relationship('Store')


class ProductReview(Base, BaseMixin):
    __tablename__ = 'product_review'
    __table_args__ = {'comment': '상품 리뷰'}

    id = Column(INTEGER(10), primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    title = Column(String(128), comment='제목')
    contents = Column(Text, comment='내용')
    rating = Column(DECIMAL(2, 1), comment='별점')
    status = Column(String(2), server_default=text("'Y'"), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    order_info = Column(String(255), comment='구매 관련 정보')
    order_product_id = Column(ForeignKey('order_product.id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)

    customer = relationship('Customer')
    order_product = relationship('OrderProduct')
    product = relationship('Product', back_populates="reviews")
    photos = relationship('ProductReviewPhoto', back_populates="review")


class ProductStoreMemo(Base, BaseMixin):
    __tablename__ = 'product_store_memo'
    __table_args__ = (
        Index('u_product_store_memo', 'product_id', 'store_code', unique=True),
    )

    id = Column(INTEGER(10), primary_key=True)
    memo = Column(Text, nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    member = relationship('Member')
    product = relationship('Product')
    store = relationship('Store')


class Qna(Base, BaseMixin):
    __tablename__ = 'qna'
    __table_args__ = {'comment': '문의'}

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(128), nullable=False, comment='제목')
    contents = Column(Text, nullable=False, comment='내용')
    q_member_id = Column(ForeignKey('member.id'), nullable=False, index=True, comment='질문자')
    status = Column(String(2), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    qna_id = Column(ForeignKey('qna.id'), index=True, comment='답변일 경우 질문 qna id')
    admin_id = Column(INTEGER(10))
    a_member_id = Column(ForeignKey('member.id'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True)
    secret = Column(String(1), server_default=text("'N'"))

    a_member = relationship('Member', primaryjoin='Qna.a_member_id == Member.id')
    q_member = relationship('Member', primaryjoin='Qna.q_member_id == Member.id')
    qna = relationship('Qna', remote_side=[id])
    store = relationship('Store')


class QnaStore(Base, BaseMixin):
    __tablename__ = 'qna_store'
    __table_args__ = {'comment': '문의 (상점)'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(32), comment='문의유형')
    title = Column(String(128), nullable=False, comment='제목')
    contents = Column(Text, nullable=False, comment='내용')
    status = Column(String(2), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    qna_id = Column(ForeignKey('qna_store.id', ondelete='CASCADE'), index=True, comment='답변일 경우 질문 qna id')
    admin_id = Column(INTEGER(10))
    a_member_id = Column(ForeignKey('member.id', ondelete='SET NULL'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True)
    secret = Column(String(1), server_default=text("'N'"))
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)

    a_member = relationship('Member')
    customer = relationship('Customer')
    qna = relationship('QnaStore', remote_side=[id])
    store = relationship('Store')


class ShippingArea(Base, BaseMixin):
    __tablename__ = 'shipping_area'
    __table_args__ = {'comment': '배송지역'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False, comment='이름')
    cost = Column(INTEGER(11), nullable=False, comment='비용')
    shipping_cost_id = Column(ForeignKey('shipping_cost.id', ondelete='CASCADE'), nullable=False, index=True)

    shipping_cost = relationship('ShippingCost')


class StoreProduct(Base, BaseMixin):
    __tablename__ = 'store_product'
    __table_args__ = (
        Index('u_store_product', 'store_code', 'product_id', unique=True),
        {'comment': '상점-상품 연결'}
    )

    id = Column(INTEGER(10), primary_key=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    view_yn = Column(String(1), nullable=False, server_default=text("'Y'"))
    variation = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='가격 변동값')
    catalog_id = Column(INTEGER(11), comment='카탈로그 출처')

    product = relationship('Product')
    store = relationship('Store')


class StorePopup(Base, BaseMixin):
    __tablename__ = 'store_popup'

    id = Column(INTEGER(11), primary_key=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    title = Column(String(45), nullable=False)
    contents = Column(Text)
    img = Column(String(512))
    link = Column(String(512))
    type = Column(String(3))
    status = Column(String(2), nullable=False, server_default=text("'N'"))
    view_start_date = Column(DateTime, comment='노출 시작일')
    view_end_date = Column(DateTime, comment='노출 종료일')
    duplicate = Column(String(1), server_default=text("'N'"), comment='복제상점에서 보여질지 여부')
    sort = Column(INTEGER(11), server_default=text("99"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    store = relationship('Store')


class StoreTheme(Base, BaseMixin):
    __tablename__ = 'store_theme'
    __table_args__ = {'comment': '상점 테마(상품 분류)'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(String(255), nullable=False)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    pid = Column(ForeignKey('store_theme.id'), index=True)
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    layout = Column(Text, comment='레이아웃 데이터 (Json)')
    visible = Column(String(2), server_default=text("'Y'"), comment='노출 여부')
    top_visible = Column(String(2), nullable=False, server_default=text("'Y'"), comment='상단 메뉴 노출')
    use_layout = Column(String(2), nullable=False, server_default=text("'N'"))
    sort = Column(INTEGER(11), server_default=text("99"), comment='순서')

    parent = relationship('StoreTheme', remote_side=[id])
    store = relationship('Store')


class Cart(Base, BaseMixin):
    __tablename__ = 'cart'
    __table_args__ = (
        Index('u_cart_customer_option', 'customer_id', 'product_option_id', unique=True),
        {'comment': '장바구니'}
    )

    id = Column(BIGINT(20), primary_key=True)
    product_option_id = Column(ForeignKey('product_option.id', ondelete='CASCADE'), nullable=False, index=True)
    count = Column(INTEGER(11))
    checked = Column(TINYINT(1), server_default=text("1"))
    reg_date = Column(DateTime, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    type = Column(String(2), comment='D(배송),U(미배송)')

    customer = relationship('Customer')
    product_option = relationship('ProductOption')


class Commission(Base, BaseMixin):
    __tablename__ = 'commission'
    __table_args__ = {'comment': '수수료'}

    id = Column(BIGINT(20), primary_key=True)
    store_code = Column(ForeignKey('store.code'), index=True)
    product_id = Column(ForeignKey('product.id'), index=True)
    member_id = Column(ForeignKey('member.id'), index=True)
    type = Column(String(2), nullable=False, comment='퍼센트(P) or 고정(F)')
    value = Column(DECIMAL(10, 2), nullable=False, comment='수수료')
    default = Column(String(1), nullable=False, server_default=text("'N'"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    target = Column(ForeignKey('member.id'), nullable=False, index=True, comment='수익을 받을 대상')
    target_type = Column(String(10), comment='CC, CO, PAC')
    pg_provider = Column(String(16))
    pg_kind = Column(String(16))
    kind = Column(String(16), comment='prd 상품, ship 배송비')
    payment = Column(String(2), comment='이익차감[D], 분리지급[S]')

    member = relationship('Member', primaryjoin='Commission.member_id == Member.id')
    product = relationship('Product')
    store = relationship('Store')
    member1 = relationship('Member', primaryjoin='Commission.target == Member.id')


class DeptPermission(Base, BaseMixin):
    __tablename__ = 'dept_permission'
    __table_args__ = (
        Index('u_dept_permission_dept_code', 'dept_id', 'permission_code', unique=True),
        {'comment': '부서 권한'}
    )

    id = Column(INTEGER(10), primary_key=True)
    dept_id = Column(ForeignKey('dept.id'), nullable=False, index=True)
    permission_code = Column(ForeignKey('permission.code'), nullable=False, index=True)
    target = Column(String(16), nullable=False, server_default=text("'*'"))

    dept = relationship('Dept')
    permission = relationship('Permission')


class Inventory(Base, BaseMixin):
    __tablename__ = 'inventory'
    __table_args__ = {'comment': '재고'}

    id = Column(INTEGER(10), primary_key=True)
    count = Column(INTEGER(11), nullable=False, server_default=text("0"))
    safe_count = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='안전재고')
    product_option_id = Column(ForeignKey('product_option.id'), nullable=False, index=True)
    day_able_count = Column(INTEGER(11), comment='일 처리가능수량')
    use_acc_qty = Column(String(1), server_default=text("'N'"), comment='누적 수량 사용여부')

    option = relationship('ProductOption', back_populates="inventory")


class MemberWorker(Base, BaseMixin):
    __tablename__ = 'member_worker'
    __table_args__ = (
        Index('u_member_company_dept', 'member_id', 'dept_id', unique=True),
        {'comment': '회원 조직 직원 연결'}
    )

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    dept_id = Column(ForeignKey('dept.id'), nullable=False, index=True)
    member_company_id = Column(ForeignKey('member_company.id'), nullable=False, index=True)

    dept = relationship('Dept')
    member_company = relationship('MemberCompany')
    member = relationship('Member')


class Message(Base, BaseMixin):
    __tablename__ = 'message'
    __table_args__ = {'comment': '메세지'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(16), comment='타입')
    mobile = Column(String(16), comment='휴대전화')
    title = Column(String(32), comment='제목')
    body = Column(Text, comment='내용')
    status = Column(String(2), comment='상태')
    mid = Column(String(32), comment='전송결과 id')
    provider = Column(String(16), comment='제공 업체')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    res_date = Column(DateTime, comment='예약일시')
    can_date = Column(DateTime, comment='취소일시')
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    order_id = Column(ForeignKey('order.id'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True)

    member = relationship('Member')
    order = relationship('Order')
    store = relationship('Store')


class OrderCoupon(Base, BaseMixin):
    __tablename__ = 'order_coupon'
    __table_args__ = (
        Index('u_order_coupon_order_coupon', 'order_id', 'coupon_id', unique=True),
        {'comment': '주문-쿠폰 연결'}
    )

    id = Column(BIGINT(20), primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    coupon_id = Column(ForeignKey('coupon.id'), nullable=False, index=True)

    coupon = relationship('Coupon')
    order = relationship('Order')


class OrderRe(Base, BaseMixin):
    __tablename__ = 'order_re'
    __table_args__ = {'comment': '주문 반품교환 요청'}

    id = Column(INTEGER(10), primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    type = Column(String(16), nullable=False, comment='타입, return, refund, exchange')
    contents = Column(Text)
    category = Column(String(128))
    memo = Column(Text)
    status = Column(String(2), nullable=False, server_default=text("'R'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    end_date = Column(DateTime)
    refund_amount = Column(DECIMAL(10, 2))
    pay_type = Column(String(45))
    refund_date = Column(DateTime)
    log = Column(Text)

    order = relationship('Order')
    products = relationship('OrderProduct', secondary='order_re_product')


class OrderProduct(Base, BaseMixin):
    __tablename__ = 'order_product'
    __table_args__ = {'comment': '주문-상품옵션 연결'}

    id = Column(BIGINT(20), primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    product_option_id = Column(ForeignKey('product_option.id'), nullable=False, index=True)
    product_code = Column(String(255), nullable=False)
    ea = Column(INTEGER(11), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(3), nullable=False, server_default=text("'Y'"))
    seller_title = Column(String(45), nullable=False)
    product_name = Column(String(45), nullable=False)
    product_description = Column(String(255), nullable=False)
    product_thumbnail = Column(String(512), nullable=False)
    origin_price = Column(DECIMAL(10, 2))
    order_shipping_id = Column(ForeignKey('order_shipping.id'), index=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True, comment='공급자 회원 ID')
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    settlement_date = Column(DateTime, comment='정산 처리일시')
    use_end_date = Column(DateTime, comment='사용 만료일')
    use_date = Column(DateTime, comment='사용 일시')
    code = Column(String(128), comment='발행 코드')
    user_name = Column(String(32))
    user_phone = Column(String(16))
    user_email = Column(String(45))
    type = Column(String(16), comment='상품 유형')
    discount = Column(DECIMAL(10, 2))
    complete_date = Column(DateTime, comment='구매 확정일')
    balance = Column(INTEGER(11), server_default=text("0"), comment='잔액')

    member = relationship('Member')
    order = relationship('Order', back_populates="products")
    order_shipping = relationship('OrderShipping')
    product = relationship('Product')
    product_option = relationship('ProductOption')
    ecoupon = relationship('Ecoupon', back_populates='order_product', uselist=False)


class ProductReviewPhoto(Base, BaseMixin):
    __tablename__ = 'product_review_photo'
    __table_args__ = {'comment': '상품 리뷰 사진'}

    id = Column(INTEGER(10), primary_key=True)
    product_review_id = Column(ForeignKey('product_review.id'), nullable=False, index=True)
    uri = Column(String(256), comment='URI')
    reg_dt = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_dt = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    review = relationship('ProductReview', back_populates="photos")


class ShippingAreaDetail(Base, BaseMixin):
    __tablename__ = 'shipping_area_detail'
    __table_args__ = {'comment': '배송지역 상세'}

    id = Column(INTEGER(10), primary_key=True)
    category_text = Column(String(128), comment='계층구조 풀 텍스트')
    zipcode = Column(String(45), comment='우편번호')
    address_house = Column(String(64), comment='지번 주소')
    address_street = Column(String(64), comment='도로명 주소')
    shipping_area_id = Column(ForeignKey('shipping_area.id', ondelete='CASCADE'), nullable=False, index=True)

    shipping_area = relationship('ShippingArea')


class StoreThemeProduct(Base, BaseMixin):
    __tablename__ = 'store_theme_product'
    __table_args__ = (
        Index('u_store_theme_product', 'store_theme_id', 'product_id', unique=True),
        {'comment': '상점 테마 상품'}
    )

    id = Column(INTEGER(10), primary_key=True)
    store_theme_id = Column(ForeignKey('store_theme.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)

    product = relationship('Product')
    store_theme = relationship('StoreTheme')


class OrderShipping(Base, BaseMixin):
    __tablename__ = 'order_shipping'
    __table_args__ = {'comment': '주문 상품 배송'}

    id = Column(BIGINT(20), primary_key=True)
    provider = Column(String(45), comment='운송업체')
    provider_code = Column(String(16), comment='운송업체 코드')
    number = Column(String(45), comment='운송번호')
    status = Column(String(2), comment='상태')
    cost = Column(DECIMAL(10, 2), nullable=False, comment='요금')
    shipping_type = Column(String(10), nullable=False, comment='배송타입')
    pay_type = Column(String(4), nullable=False, comment='선불(pre), 후불(post)')
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True, comment='공급자 회원 ID')
    shipping_info_id = Column(ForeignKey('shipping_info.id'), nullable=False, index=True)
    settlement_date = Column(DateTime, comment='정산 처리일시')
    number_reg_date = Column(DateTime, comment='송장 등록일')
    complete_date = Column(DateTime, comment='배송 완료일')

    member = relationship('Member')
    order = relationship('Order')
    shipping_info = relationship('ShippingInfo')


class OrderReProduct(Base, BaseMixin):
    __tablename__ = 'order_re_product'

    id = Column(INTEGER(10), primary_key=True)
    order_re_id = Column(ForeignKey('order_re.id'), nullable=False, index=True)
    order_product_id = Column(ForeignKey('order_product.id'), nullable=False, index=True)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    end_date = Column(DateTime)

    parent = relationship('OrderRe', uselist=False, viewonly=True)
    product = relationship('OrderProduct', uselist=False, viewonly=True)


class SubCommission(Base, BaseMixin):
    __tablename__ = 'sub_commission'

    id = Column(BIGINT(20), primary_key=True)
    type = Column(String(2), nullable=False, comment='퍼센트(P) or 고정(F)')
    value = Column(DECIMAL(10, 2), nullable=False, comment='수수료')
    commission_id = Column(ForeignKey('commission.id'), index=True)
    sub_commission_id = Column(ForeignKey('sub_commission.id'), index=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)

    commission = relationship('Commission')
    member = relationship('Member')
    sub_commission = relationship('SubCommission', remote_side=[id])


class ShippingTracking(Base, BaseMixin):
    __tablename__ = 'shipping_tracking'
    __table_args__ = {'comment': '배송 추적 상세'}

    id = Column(BIGINT(20), primary_key=True)
    location = Column(String(45))
    status = Column(String(45))
    msg = Column(String(128), nullable=False)
    agent = Column(String(16))
    tel = Column(String(16))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    order_shipping_id = Column(ForeignKey('order_shipping.id'), nullable=False, index=True)

    order_shipping = relationship('OrderShipping')


class WishProduct(Base, BaseMixin):
    __tablename__ = 'wish_product'
    __table_args__ = {'comment': '관심 상품'}

    product_id = Column(ForeignKey('product.id', ondelete='CASCADE'), primary_key=True, index=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    reg_date = Column(DateTime, server_default=text("current_timestamp()"))

    customer = relationship('Customer')


class DeliveryAddress(Base, BaseMixin):
    __tablename__ = 'delivery_address'
    __table_args__ = {'comment': '배송지'}

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(45), nullable=False, comment='배송지명')
    name = Column(String(45), nullable=False)
    address = Column(String(255), nullable=False)
    address_detail = Column(String(255), nullable=False)
    zipcode = Column(String(16), nullable=False, comment='우편번호')
    mobile = Column(String(255), nullable=False)
    phone = Column(String(255))
    default_yn = Column(String(1), nullable=False, server_default=text("'N'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)

    customer = relationship('Customer')


class StoreBoardGroup(Base, BaseMixin):
    __tablename__ = 'store_board_group'

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False)
    menu_visible = Column(String(2), nullable=False, server_default=text("'N'"))
    view_type = Column(String(16), nullable=False, server_default=text("'thumbnail'"), comment='thumbnail, banner')
    view_end_content = Column(String(1), nullable=False, server_default=text("'N'"), comment='기간 지난 컨텐츠 노출 여부')
    status = Column(String(2), nullable=False, server_default=text("'Y'"), comment='상태')
    sort = Column(INTEGER(11), server_default=text("99"), comment='순서')
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)

    store = relationship('Store')


class StoreBoard(Base, BaseMixin):
    __tablename__ = 'store_board'
    __table_args__ = {'comment': '공지사항'}

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(128), nullable=False, comment='제목')
    contents = Column(Text, nullable=False, comment='내용')
    pin = Column(String(1), server_default=text("'N'"), comment='상위 고정')
    sort = Column(INTEGER(11), server_default=text("99"), comment='순서')
    status = Column(String(2), nullable=False, server_default=text("'Y'"), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    image = Column(String(512))
    view_start_date = Column(DateTime, comment='노출 시작일')
    view_end_date = Column(DateTime, comment='노출 종료일')
    start_date = Column(DateTime, comment='\\n시작일')
    end_date = Column(DateTime, comment='종료일')
    store_board_group_id = Column(ForeignKey('store_board_group.id'), index=True)
    member_id = Column(ForeignKey('member.id'), index=True)
    customer_id = Column(ForeignKey('customer.id'), index=True)

    customer = relationship('Customer')
    member = relationship('Member')
    store_board_group = relationship('StoreBoardGroup')


class StoreBoardCmt(Base, BaseMixin):
    __tablename__ = 'store_board_cmt'
    __table_args__ = {'comment': '상점 게시판 댓글'}

    id = Column(INTEGER(10), primary_key=True)
    comment = Column(String(255), nullable=False)
    status = Column(String(2), nullable=False, server_default=text("'Y'"), comment='상태')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    store_board_id = Column(ForeignKey('store_board.id'), nullable=False, index=True)
    member_id = Column(ForeignKey('member.id'), index=True)
    customer_id = Column(ForeignKey('customer.id'), index=True)
    p_id = Column(ForeignKey('store_board_cmt.id'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True, comment='작성된 상점')
    ip = Column(String(100))

    customer = relationship('Customer')
    member = relationship('Member')
    p = relationship('StoreBoardCmt', remote_side=[id])
    store_board = relationship('StoreBoard')
    store = relationship('Store')


class Shop(Base, BaseMixin):
    __tablename__ = 'shop'
    __table_args__ = {'comment': '매장'}

    id = Column(INTEGER(10), primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(Text, nullable=False)
    address = Column(String(255))
    address_detail = Column(String(255))
    work_time = Column(String(512), comment='운영시간')
    holiday = Column(String(128), comment='휴무일')
    image = Column(String(512))
    lat = Column(String(45))
    lng = Column(String(45))
    tel = Column(String(45))
    subtitle = Column(String(100))
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    reg_date = Column(DateTime, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    member = relationship('Member')
    badges = relationship('Badge', secondary="shop_badge")


class StoreThemeShop(Base, BaseMixin):
    __tablename__ = 'store_theme_shop'

    id = Column(INTEGER(10), primary_key=True)
    store_theme_id = Column(ForeignKey('store_theme.id'), nullable=False, index=True)
    shop_id = Column(ForeignKey('shop.id'), nullable=False, index=True)

    shop = relationship('Shop')
    store_theme = relationship('StoreTheme')


class LogOrder(Base, BaseMixin):
    __tablename__ = 'log_order'

    id = Column(INTEGER(10), primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    action = Column(String(16), nullable=False)
    msg = Column(Text, nullable=False)
    writer = Column(String(64), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    _del = Column('del', String(1), nullable=False, server_default=text("'N'"))

    order = relationship('Order')


class SmsHistory(Base, BaseMixin):
    __tablename__ = 'sms_history'
    __table_args__ = {'comment': 'SMS 전송 기록'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(16), comment='타입')
    mobile = Column(String(16), comment='휴대전화')
    title = Column(String(32), comment='제목')
    body = Column(Text, comment='내용')
    status = Column(String(2), comment='상태')
    mid = Column(String(32), comment='전송결과 id')
    provider = Column(String(16), comment='제공 업체')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    res_date = Column(DateTime, comment='예약일시')
    can_date = Column(DateTime, comment='취소일시')
    member_id = Column(ForeignKey('member.id'), index=True)
    customer_id = Column(ForeignKey('customer.id'), index=True)
    order_id = Column(ForeignKey('order.id'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True)

    customer = relationship('Customer')
    member = relationship('Member')
    order = relationship('Order')
    store = relationship('Store')


class EmailHistory(Base, BaseMixin):
    __tablename__ = 'email_history'
    __table_args__ = {'comment': '이메일 전송 기록'}

    id = Column(INTEGER(10), primary_key=True)
    type = Column(String(16), comment='타입')
    to = Column(String(45))
    title = Column(String(32), comment='제목')
    body = Column(Text, comment='내용')
    status = Column(String(2), comment='상태')
    mid = Column(String(32), comment='전송결과 id')
    provider = Column(String(16), comment='제공 업체')
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    res_date = Column(DateTime, comment='예약일시')
    can_date = Column(DateTime, comment='취소일시')
    member_id = Column(ForeignKey('member.id'), index=True)
    customer_id = Column(ForeignKey('customer.id'), index=True)
    order_id = Column(ForeignKey('order.id'), index=True)
    store_code = Column(ForeignKey('store.code'), index=True)

    customer = relationship('Customer')
    member = relationship('Member')
    order = relationship('Order')
    store = relationship('Store')


class LogCommission(Base, BaseMixin):
    __tablename__ = 'log_commission'
    __table_args__ = {'comment': '수수료 로그'}

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id', ondelete='CASCADE'), nullable=False, index=True)
    action = Column(String(32), nullable=False)
    msg = Column(Text, nullable=False)
    writer = Column(String(64), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    _del = Column('del', String(1), nullable=False, server_default=text("'N'"))

    member = relationship('Member')


class PgInfoSub(Base, BaseMixin):
    __tablename__ = 'pg_info_sub'

    id = Column(INTEGER(10), primary_key=True)
    pg_info_id = Column(ForeignKey('pg_info.id'), nullable=False, index=True)
    kind = Column(String(45), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    tno = Column(String(45), nullable=False)

    pg_info = relationship('PgInfo', back_populates='pg_info_sub')


class RuralPostcode(Base, BaseMixin):
    __tablename__ = 'rural_postcode'
    __table_args__ = {'comment': '도서산간 우편번호'}

    post_code = Column(INTEGER(11), primary_key=True)
    area = Column(String(100))


class Ecoupon(Base, BaseMixin):
    __tablename__ = 'ecoupon'

    id = Column(INTEGER(10), primary_key=True)
    provider = Column(String(45), nullable=False)
    goods_id = Column(String(256), nullable=False)
    tr_id = Column(String(512), nullable=False)
    pin_code = Column(Text, nullable=False)
    period_date = Column(DateTime, nullable=False)
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    kind = Column(String(45))
    duty_code = Column(Text)
    raw_data = Column(Text)
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    order_product_id = Column(ForeignKey('order_product.id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    order_code = Column(String(512))

    customer = relationship('Customer')
    order = relationship('Order')
    order_product = relationship('OrderProduct', back_populates='ecoupon')



class RevenueOffline(Base, BaseMixin):
    __tablename__ = 'revenue_offline'
    __table_args__ = {'comment': '오프라인 매출'}

    id = Column(INTEGER(10), primary_key=True)
    code = Column(String(100), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    sales_date = Column(DateTime, nullable=False)
    status = Column(String(2), nullable=False, server_default=text("'Y'"))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    member_id = Column(ForeignKey('member.id'), index=True, comment='등록자')

    member = relationship('Member')


class AdminRefund(Base, BaseMixin):
    __tablename__ = 'admin_refund'
    __table_args__ = {'comment': '관리자 환불 내역'}

    id = Column(INTEGER(10), primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False, index=True)
    product_name = Column(String(512), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    store_code = Column(String(45), nullable=False)
    store_name = Column(String(45), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)

    customer = relationship('Customer')
    member = relationship('Member')
    order = relationship('Order')


class SettlementExcel(Base, BaseMixin):
    __tablename__ = 'settlement_excel'
    __table_args__ = {'comment': '정산 내역 엑셀 요청'}

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), nullable=False, index=True)
    member_type = Column(String(16))
    target_kind = Column(String(16))
    target_status = Column(String(2))
    s_reg_date = Column(Date)
    e_reg_date = Column(Date)
    request_member = Column(ForeignKey('member.id'), nullable=False, index=True)
    status = Column(String(2))
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    mod_date = Column(DateTime, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    file = Column(String(512))

    member = relationship('Member', primaryjoin='SettlementExcel.member_id == Member.id')
    member1 = relationship('Member', primaryjoin='SettlementExcel.request_member == Member.id')


class ShopBadge(Base, BaseMixin):
    __tablename__ = 'shop_badge'
    __table_args__ = (
        Index('u_shop_badge', 'shop_id', 'badge_id', unique=True),
        {'comment': '매장-뱃지 연결'}
    )

    shop_id = Column(ForeignKey('shop.id'), primary_key=True, nullable=False, index=True)
    badge_id = Column(ForeignKey('badge.id'), primary_key=True, nullable=False, index=True)


class CouponPublishTarget(Base, BaseMixin):
    __tablename__ = 'coupon_publish_target'

    id = Column(INTEGER(10), primary_key=True)
    store_code = Column(ForeignKey('store.code'), nullable=False, index=True)
    coupon_group_id = Column(ForeignKey('coupon_group.id'), nullable=False, index=True)

    coupon_group = relationship('CouponGroup', back_populates='coupon_publish_target')
    store = relationship('Store')


class CouponTarget(Base, BaseMixin):
    __tablename__ = 'coupon_target'

    id = Column(INTEGER(10), primary_key=True)
    member_id = Column(ForeignKey('member.id'), index=True)
    product_id = Column(ForeignKey('product.id'), index=True)
    coupon_group_id = Column(ForeignKey('coupon_group.id'), nullable=False, index=True)

    coupon_group = relationship('CouponGroup', back_populates='coupon_target')
    member = relationship('Member')
    product = relationship('Product')


class LogCustomer(Base, BaseMixin):
    __tablename__ = 'log_customer'

    id = Column(INTEGER(11), primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False, index=True)
    action = Column(String(32), nullable=False)
    msg = Column(Text, nullable=False)
    writer = Column(String(64), nullable=False)
    reg_date = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    _del = Column('del', String(1), nullable=False, server_default=text("'N'"))

    customer = relationship('Customer')
