declare module 'ProdReqDetailInfoModule' {
  export interface ProdDetailInfo {
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
    products: Product[];
    store: Store;
    manager_member: ManagerMember;
  }

  export interface Member {
    id: number;
    name: string;
    email: string;
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
