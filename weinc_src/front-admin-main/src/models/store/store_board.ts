declare module 'StoreBoardInfoModule' {
  export interface BoardListInfo {
    total: number;
    datas: Board[];
  }

  export interface Board {
    id: number;
    title: string;
    contents: string;
    pin: string;
    sort: number;
    status: string;
    reg_date: string;
    mod_date: string;
    image: string;
    view_start_date: string;
    view_end_date: string;
    start_date: string;
    end_date: string;
    store_board_group_id: number;
    member_id: number;
    customer_id: number;
  }
}
