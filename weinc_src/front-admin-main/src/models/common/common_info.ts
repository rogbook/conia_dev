declare module 'ProdCommonInfoListModule' {
  export interface ProdCommonInfo {
    id: number;
    member_id: number;
    name: string;
    contents: string;
    status: string;
    reg_date: Date;
    mod_date: Date;
    member: {
      id: number;
      name: string;
      email: string;
      company: {
        id: number;
        name: string;
      };
    };
  }
}
