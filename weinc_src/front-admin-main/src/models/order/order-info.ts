declare module 'OrderInfoModule' {
  export interface OrderList {
    total: number;
    datas: Order[];
  }

  export interface Order {
    id: number;
    order_id: string;
    origin_order_id: string;
    product_option_id: number;
    ea: number;
    amount: number;
    status: string;
    seller_title: string;
    product_name: string;
    product_description: string;
    product_thumbnail: string;
    origin_price: number;
    order_shipping_id: number;
    member_id: number;
    order_date: string;
    pg_date: string;
    pg_kind: string;
    user_name: string;
    store_name: string;
    store_code: string;
    product_option_name: string;
    type: string;
  }
}

declare module 'OrderDetailInfoModule' {
  export interface OrderDetail {
    id: string;
    member_id: number;
    store_code: string;
    origin_order_id: number;
    origin_amount: number;
    raw_amount: number;
    final_amount: number;
    tex_free_amount: number;
    tax_rate: number;
    discount: number;
    status: string;
    user_name: string;
    user_phone: string;
    user_mobile: string;
    user_email: string;
    recipient_name: string;
    recipient_phone: string;
    recipient_mobile: string;
    shipping_cost: number;
    shipping_cost_post: number;
    shipping_condition: string;
    shipping_msg: string;
    zipcode: string;
    address: string;
    address_detail: string;
    coupon_discount: number;
    step_type: string;
    reg_date: string;
    mod_date: string;
    client_type: string;
    referer: string;
    referer_url: string;
    total_ea: number;
    total_kind: number;
    ipcc_code: string;
    ip: string;
    calculate_date: string;
    password: string;
    cert_id: number;
    products: Product[];
    pg_info: PgInfo;
    pg_cancel_disable: string;
  }

  export interface Product {
    id: number;
    order_id: string;
    product_option_id: number;
    ea: number;
    amount: number;
    discount: number;
    status: string;
    seller_title: string;
    product_code: string;
    product_name: string;
    product_description: string;
    product_thumbnail: string;
    origin_price: number;
    order_shipping_id: number;
    order_shipping: {
      id: 0;
      provider: string;
      provider_code: string;
      number: string;
      status: string;
      cost: number;
      shipping_type: string;
      pay_type: string;
      order_id: string;
      member_id: number;
      shipping_info_id: number;
    };
    member_id: number;
    order_date: string;
    pg_date: string;
    pg_kind: string;
    user_name: string;
    user_phone: string;
    user_email: string;
    store_name: string;
    store_code: string;
    product_option_name: string;
    type: string;
    pg_cancel_disable: string;
    use_end_date: string;
    ecoupon: Ecoupon;
  }

  export interface Ecoupon {
    provider: string;
    goods_id: string;
    tr_id: string;
    pin_code: string;
    period_date: string;
    status: string;
    reg_date: string;
    mod_date: string;
    kind: string;
    duty_code: string;
    raw_data: string;
  }

  export interface PgInfo {
    order_id: string;
    provider: string;
    kind: string;
    tid: string;
    app_time: string;
    deposit_yn: string;
    deposit_date: string;
    deposit_name: string;
    bank_account: string;
    virtual_account: string;
    virtual_date: string;
    card_app_num: string;
    card_name: string;
    card_no: string;
    card_quota: string;
    card_partcanc_yn: string;
    card_bin_type_01: string;
    card_bin_type_02: string;
    cash_authno: string;
    cash_no: string;
    bankname: string;
    commid: string;
    mobile_no: string;
    pg_info_sub: PgInfoSub[];
  }

  export interface PgInfoSub {
    amount: number;
    kind: string;
  }

  export interface Log {
    total: number;
    datas: Data[];
  }

  export interface Data {
    action: string;
    msg: string;
    writer: string;
    reg_date: string;
  }

  export interface PgCancel {
    id: number;
    pg_info_order_id: string;
    tno: string;
    type: string;
    reg_date: string;
    amount: number;
    remain: number;
    part_seq: string;
  }
}
