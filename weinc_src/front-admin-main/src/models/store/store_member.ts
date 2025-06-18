declare module 'StoreMemberInfoModule' {
  export interface UserList {
    total: number;
    datas: User[];
  }

  export interface User {
    id: number;
    store_code: string;
    customer_id: number;
    confirm: string;
    reg_date: string;
    mod_date: string;
    recommander_member_id: number;
    value: string;
    customer: Customer;
    recommander_member: Recommender;
  }

  export interface Customer {
    id: number;
    name: string;
    email: string;
  }

  export interface Recommender {
    id: number;
    name: string;
    email: string;
  }
}

declare module 'StoreAbleTargetModule' {
  export interface AbleTargetList {
    total: number;
    datas: AbleTarget[];
  }

  export interface AbleTarget {
    id: number;
    store_code: string;
    unique_value: string;
    name: string;
    mobile: string;
    used: string;
  }
}
