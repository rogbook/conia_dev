declare module 'RefundeInfoModule' {
  export interface RefundList {
    total: number;
    datas: Refund[];
  }

  export interface Refund {
    id: number;
    order_id: string;
    product_name: string;
    reg_date: string;
    store_code: string;
    store_name: string;
    amount: number;
    member_id: number;
    customer_id: number;
    member: Member;
    customer: Customer;
  }

  export interface Member {
    name: string;
    email: string;
  }

  export interface Customer {
    name: string;
    email: string;
  }
}
