declare module 'OfflineInfoModule' {
  export interface OfflineList {
    total: number;
    total_sum: number;
    data: Offline[];
  }

  export interface Offline {
    id: number;
    code: string;
    amount: number;
    sales_date: string;
    status: string;
    reg_date: string;
    mod_date: string;
    member_id: number;
  }
}
