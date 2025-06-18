declare module 'PublishedCouponInfoModule' {
  export interface PublishedCouponList {
    total: number;
    datas: PublishedCoupon[];
  }

  export interface PublishedCoupon {
    id: number;
    code: string;
    name: string;
    description: string;
    reg_date: string;
    use_date: string;
    begin_date: string;
    end_date: string;
    use_yn: string;
    amount: number;
    percent: number;
    min_price: number;
    max_price: number;
    issuer: number;
    coupon_group_id: number;
    target: string;
    type: string;
    customer_id: number;
    product_id: number;
    customer: Customer;
  }

  export interface Customer {
    id: number;
    email: string;
    name: string;
  }
}
