declare module 'UserInfoModule' {
  export interface Class {
    class_code: string;
    grade: string;
  }

  export interface Company {
    id: number;
    name: string;
  }

  export interface Store {
    code: string;
    title: string;
  }

  export interface Log {
    action: string;
    msg: string;
    writer: string;
    reg_date: Date;
    del_column: string;
  }

  export interface User {
    id: number;
    email: string;
    name: string;
    nickname: string;
    mailling: string;
    sms: string;
    phone: string;
    mobile: string;
    zipcode: string;
    address: string;
    address_detail: string;
    sex: string;
    birthday: Date;
    recommend: string;
    status: string;
    login_cnt: number;
    review_cnt: number;
    order_cnt: number;
    order_sum: number;
    lastlogin_date: Date;
    reg_date: Date;
    mod_date: Date;
    auth_yn: string;
    adult_auth: string;
    referer: string;
    referer_domain: string;
    join_platform: string;
    marketing_agree_date: Date;
    adult_auth_date: Date;
    sns_naver: string;
    sns_kakao: string;
    sns_google: string;
    sns_facebook: string;
    sns_apple: string;
    sns_payco: string;
    bank: string;
    account: string;
    admin_yn: string;
    otp: string;
    grade: string;
    partner: string;
    memo: string;
    classes: Class[];
    company: Company;
    store: Store[];
    log: Log[];
    p_member: { id: number; name: string; email: string }[];
    confirm_pass: string;
    shop_yn: string;
  }
}
