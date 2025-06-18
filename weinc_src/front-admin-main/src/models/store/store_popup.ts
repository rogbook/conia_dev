declare module 'StorePopupInfoModule' {
  export interface PopupListInfo {
    total: number;
    datas: Popup[];
  }

  export interface Popup {
    id: number;
    store_code: string;
    title: string;
    contents: string;
    img: string;
    link: string;
    type: string;
    status: string;
    view_start_date: string;
    view_end_date: string;
    duplicate: string;
    sort: number;
    reg_date: string;
    mod_date: string;
  }
}
