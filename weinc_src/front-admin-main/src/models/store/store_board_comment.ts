declare module 'StoreBoardCommentInfoModule' {
  export interface BoardCommentListInfo {
    total: number;
    datas: BoardComment[];
  }

  export interface BoardComment {
    id: number;
    comment: string;
    status: string;
    reg_date: string;
    mod_date: string;
    store_board_id: number;
    member_id: number;
    customer_id: number;
    p_id: number;
    customer: Customer;
    member: Member;
  }

  export interface Customer {
    id: number;
    name: string;
    email: string;
  }

  export interface Member {
    id: number;
    name: string;
    email: string;
  }
}
