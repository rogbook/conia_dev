declare module 'ExReInfoModule' {
  export interface ExReList {
    total: number;
    datas: ExReListInfo[];
  }

  export interface ExReListInfo {
    reg_date: Date;
    end_date: Date;
    parent: Parent;
    product: Product;
  }

  export interface Parent {
    id: number;
    order_id: string;
    type: string;
    contents: string;
    category: string;
    memo: string;
    status: string;
    reg_date: string;
    mod_date: string;
    end_date: string;
    refund_amount: number;
    pay_type: string;
    refund_date: string;
    log: string;
  }

  export interface Product {
    id: number;
    order_id: string;
    product_id: number;
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
    order_shipping: OrderShipping;
  }

  export interface OrderShipping {
    id: number;
    provider: string;
    number: string;
    status: string;
    cost: number;
    shipping_type: string;
    pay_type: string;
    order_id: string;
    member_id: number;
    shipping_info_id: number;
  }
}

declare module 'ExReDetailInfoModule' {
  export interface ExReDetail {
    id: number;
    order_id: string;
    type: string;
    contents: string;
    category: string;
    memo: string;
    status: string;
    reg_date: string;
    mod_date: string;
    end_date: string;
    refund_amount: number;
    pay_type: string;
    refund_date: string;
    log: string;
    products: Product[];
  }

  export interface Product {
    id: number;
    order_id: string;
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
    order_shipping: OrderShipping;
  }

  export interface OrderShipping {
    id: number;
    provider: string;
    number: string;
    status: string;
    cost: number;
    shipping_type: string;
    pay_type: string;
    order_id: string;
    member_id: number;
    shipping_info_id: number;
  }
}
