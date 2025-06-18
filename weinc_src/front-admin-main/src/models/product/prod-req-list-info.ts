declare module 'ProdReqListInfoModule' {
  export interface ProdReqListInfo {
    total: number;
    datas: ProdReq[];
  }

  export interface ProdReq {
    id: number;
    member_id: number;
    store_code: string;
    title: string;
    memo: string;
    status: string;
    reg_date: string;
    mod_date: string;
    manager: number;
    member: Member;
    store: Store;
    manager_member: ManagerMember;
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

  export interface ManagerMember {
    id: number;
    name: string;
    email: string;
  }
}
