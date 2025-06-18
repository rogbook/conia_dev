declare module 'CustomerInfoModule' {
  export interface CustomerList {
    total: number;
    datas: Customer[];
  }

  export interface Customer {
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
    birthday: string;
    recommend: string;
    status: string;
    login_cnt: number;
    review_cnt: number;
    order_cnt: number;
    order_sum: number;
    lastlogin_date: string;
    reg_date: string;
    mod_date: string;
    auth_yn: string;
    adult_auth: string;
    referer: string;
    referer_domain: string;
    join_platform: string;
    marketing_agree_date: string;
    adult_auth_date: string;
    sns_naver: string;
    sns_kakao: string;
    sns_google: string;
    sns_facebook: string;
    sns_apple: string;
    sns_payco: string;
    grade: string;
    memo: string;
    member_store: Store[];
  }

  export interface Store {
    confirm: string;
    store: {
      code: string;
      title: string;
    };
  }
}
