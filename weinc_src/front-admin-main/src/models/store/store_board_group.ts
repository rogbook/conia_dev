declare module 'StoreBoardGroupInfoModule' {
  export interface BoardGroupListInfo {
    total: number;
    datas: BoardGroup[];
  }

  export interface BoardGroup {
    id: number;
    name: string;
    menu_visible: string;
    view_type: string;
    status: string;
    store_code: string;
    view_end_content: string;
    sort: number;
  }
}
