declare module 'StoreListInfoModule' {
  export interface Store {
    code?: string;
    member_id?: number;
    title?: string;
    type?: string;
    domain?: string;
    status?: string;
    reg_date?: Date;
    mod_date?: Date;
    layout?: string;
    logo_pc?: string;
    logo_mobile?: string;
    favicon?: string;
    info?: string;
    dupl_store?: string;
    able_target_use?: string;
    verify_code?: string;
    exclude_menu?: string;
    group?: string;
    prd_pg_opt_use?: string;
    meal_opt_use?: string;
    meal_opt_limit_use?: string;
    meal_opt_limit_time?: string;
    meal_opt_cancel_use?: string;
    keyword?: string;
    member?: {
      id: number;
      name: string;
      email: string;
    };
  }

  export interface StoreList {
    total: number;
    datas: Store[];
  }

  export interface Log {
    total: number;
    datas: Data[];
  }

  export interface Data {
    action: string;
    msg: string;
    writer: string;
    reg_date: string;
  }
}
