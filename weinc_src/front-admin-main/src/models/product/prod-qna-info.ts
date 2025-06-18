declare module 'ProdQnaInfoModule' {
  export interface ProdQnaInfoList {
    total: number;
    datas: ProdQnaInfo[];
  }

  export interface ProdQnaInfo {
    id: number;
    title: string;
    contents: string;
    product_id: number;
    status: string;
    reg_date: string;
    mod_date: string;
    product_qna_id: number;
    admin_id: number;
    a_member_id: number;
    store_code: string;
    secret: string;
    customer_id: number;
    customer: Customer;
    a_member: AMember;
    store: Store;
    answer: Answer | null;
    product: Product;
  }

  export interface Customer {
    id: number;
    name: string;
  }

  export interface AMember {
    id: number;
    name: string;
  }

  export interface Store {
    code: string;
    title: string;
  }
  export interface Answer {
    id: number;
    title: string;
    contents: string;
    a_member_id: number;
    reg_date: string;
  }

  export interface Product {
    id: number;
    code: string;
    name: string;
    photos: Photo[];
  }

  export interface Photo {
    id: number;
    uri: string;
  }
}
