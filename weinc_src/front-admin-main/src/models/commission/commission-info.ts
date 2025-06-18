declare module 'CommissionInfoModule' {
  export interface CommissionList {
    total: number;
    datas: Commission[];
  }

  export interface Commission {
    id: number;
    store_code: string;
    product_id: number;
    member_id: number;
    type: string;
    value: number;
    default: string;
    mod_date: string;
    target: number;
    target_type: string;
    pg_provider: string;
    pg_kind: string;
    member: Member;
    member1: Member;
    store: Store;
    product: Product;
    payment: string;
  }

  export interface Member {
    id: number;
    name: string;
    email: string;
  }

  export interface Store {
    code: string;
    title: string;
  }

  export interface Product {
    id: string;
    code: string;
    name: string;
    photos: Photo[];
  }

  export interface Photo {
    uri: string;
  }

  export interface SubStore {
    title: string;
    store_code: string;
  }
}
