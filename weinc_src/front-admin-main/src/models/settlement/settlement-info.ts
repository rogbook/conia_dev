declare module 'SettlementInfoModule' {
  export interface SettlementList {
    total: number;
    total_sum: number;
    datas: Settlement[];
  }

  export interface SettlementShipList {
    total: number;
    total_sum: number;
    datas: SettlementShip[];
  }

  export interface Settlement {
    id: number;
    target_date: string;
    account_raw_id: string;
    member_id: number;
    type: string;
    status: string;
    sequence: number;
    target_amount: number;
    amount: number;
    commission_type: string;
    commission_value: number;
    payment_date: string;
    reg_date: string;
    mod_date: string;
    pg_provider: string;
    pg_kind: string;
    tax: string;
    payment: string;
    reject: string;
    account_raw: AccountRaw;
    member: Member;
  }

  export interface SettlementShip {
    id: number;
    target_date: string;
    order_id: string;
    order_shipping_id: number;
    store_code: string;
    store: {
      code: string;
      title: string;
    };
    type: string;
    status: string;
    sequence: number;
    target_amount: number;
    amount: number;
    member_id: number;
    payment_date: string;
    reg_date: string;
    mod_date: string;
    commission_type: string;
    commission_value: number;
    tax: string;
    payment: string;
    reject: string;
    pg_provider: string;
    pg_kind: string;
    member: Member;
  }

  export interface AccountRaw {
    id: number;
    target_date: string;
    order_id: string;
    order_product: OrderProduct;
    order_product_id: number;
    product_id: number;
    store_code: string;
    store: {
      code: string;
      title: string;
    };
    amount: number;
    pg_type: string;
    supply_price: number;
    margin_price: number;
    processed: string;
    reg_date: string;
    product: Product;
  }

  export interface OrderProduct {
    complete_date: string;
    ea: number;
    id: number;
    product_option: {
      option_1: string;
      option_2: string;
      option_3: string;
      option_4: string;
      option_5: string;
      option_title: string;
      origin_price: number;
      selling_price: number;
      supply_price: number;
    };
  }

  export interface Product {
    id: number;
    name: string;
  }

  export interface Member {
    id: number;
    name: string;
    email: string;
  }
  export interface Histories {
    datas: History[];
  }

  export interface History {
    id: number;
    target_date: string;
    member: Member;
    type: string;
    sequence: number;
    target_amount: number;
    amount: number;
    commission_type: string;
    commission_value: number;
    reg_date: string;
    payment: string;
  }

  export interface ReqSettlementExcel {
    id: number;
    member_id: number;
    member_type: string;
    request_member: number;
    reg_date: string;
    mod_date: string;
    s_reg_date: string;
    e_reg_date: string;
    status: string;
    file: string;
    member: {
      id: number;
      name: string;
      email: string;
      store: {
        code: string;
        title: string;
      };
      company: {
        name: string;
      };
    };
    member1: {
      id: number;
      email: string;
      name: string;
    };
  }
}
