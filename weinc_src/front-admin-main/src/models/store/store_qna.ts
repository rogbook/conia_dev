declare module 'StoreQnaInfoMOdule' {
  export interface storeQnaInfoList {
    total: number;
    datas: storeQna[];
  }

  export interface storeQna {
    id: number;
    type: string;
    title: string;
    contents: string;
    customer_id: number;
    status: string;
    reg_date: string;
    mod_date: string;
    qna_id: number;
    admin_id: number;
    a_member_id: number;
    store_code: string;
    secret: string;
    customer: Customer;
    a_member: AMember;
    store: Store;
    answer: Answer | null;
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
}
