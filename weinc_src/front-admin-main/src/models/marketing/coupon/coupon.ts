declare module 'CouponInfoModule' {
  export interface CouponList {
    total: number;
    datas: Coupon[];
  }
  export interface Coupon {
    id: number;
    name: string;
    description: string;
    status: string;
    reg_date: string;
    mod_date: string;
    expire_days: number;
    begin_date: string;
    end_date: string;
    begin_time: string;
    end_time: string;
    amount: number;
    percent: number;
    store_code: string;
    brand_id: number;
    category_id: number;
    product_id: number;
    min_price: number;
    max_price: number;
    issuer: number;
    auto: string;
    publish_limit: number;
    publish_begin_date: string;
    publish_end_date: string;
    target: string;
    type: string;
    image: string;
    publish_cnt: number;
    product: Product;
    coupon_target: CouponTarget[];
    coupon_publish_target: CouponPublishTarget[];
    reg_coupon_target: RegCouponTarget[];
  }

  export interface Product {
    id: number;
    name: string;
    code: string;
    type: string;
    status: string;
    view_yn: string;
    options: Option[];
    photos: Photo[];
  }

  export interface Option {
    code: string;
    supply_price: number;
    origin_price: number;
    selling_price: number;
    view_yn: string;
    default_yn: string;
    status: string;
  }

  export interface Photo {
    id: number;
    uri: string;
  }

  export interface CouponTarget {
    id: number;
    member_id: number;
    product_id: number;
    member: Member;
    product: Product2;
  }

  export interface RegCouponTarget {
    product_id?: number;
    member_id?: number;
    code?: string;
    name?: string;
  }

  export interface Member {
    id: number;
    name: string;
    email: string;
    company: Company;
  }

  export interface Company {
    id: number;
    name: string;
  }

  export interface Product2 {
    id: number;
    name: string;
    code: string;
    type: string;
    status: string;
    view_yn: string;
    options: Option2[];
    photos: Photo2[];
  }

  export interface Option2 {
    code: string;
    supply_price: number;
    origin_price: number;
    selling_price: number;
    view_yn: string;
    default_yn: string;
    status: string;
  }

  export interface Photo2 {
    id: number;
    uri: string;
  }

  export interface CouponPublishTarget {
    id: number;
    store_code: string;
    store: Store;
  }

  export interface Store {
    code: string;
    title: string;
    status: string;
    logo_pc: string;
    logo_mobile: string;
    keyword: string;
  }
}
