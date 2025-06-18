declare module 'BoardInfoModule' {
  export interface FaqInfo {
    id: number;
    title: string;
    contents: string;
    category: string;
    status: string;
    target: string;
    file: string;
    store_code: string;
    reg_date: Date;
    mod_date: Date;
    store?: {
      code: string;
      title: string;
    };
  }

  export interface NoticeInfoList {
    total: number;
    datas: NoticeInfo[];
  }
  export interface NoticeInfo {
    id: number;
    title: string;
    contents: string;
    pin: string;
    sort: number;
    status: string;
    target: string;
    member_id: number;
    file: string;
    store_code: string;
    reg_date: Date;
    mod_date: Date;
    member?: {
      id: number;
      name: string;
    };
    store?: {
      code: string;
      title: string;
    };
  }

  export interface QnaInfoList {
    total: number;
    datas: QnaInfo[];
  }
  export interface QnaInfo {
    id: number;
    title: string;
    contents: string;
    q_member_id: number;
    status: string;
    reg_date: Date;
    mod_date: Date;
    qna_id?: number;
    admin_id?: number;
    store_code?: string;
    secret: string;
    q_member: {
      id: number;
      name: string;
    };
    a_member?: {
      id: number;
      name: string;
    };
    store?: {
      code: string;
      title: string;
    };
  }
}
