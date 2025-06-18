declare module 'ThemeInfoModule' {
  export interface Theme {
    id: number;
    name: string;
    description: string;
    store_code: string;
    pid: number;
    status: string;
    layout: string | any;
    visible: string;
    top_visible: string;
    use_layout: string;
    reg_date: Date;
    mod_date: Date;
    sort: number;
    sub: Theme[] | any;
  }
}
