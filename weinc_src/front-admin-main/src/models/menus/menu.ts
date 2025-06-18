declare module 'MenuInfoModule' {
  export interface MenuInfo {
    depth1: Depth1[];
    depth2: Depth2[];
    depth3: Depth3[];
  }

  export interface Depth1 {
    name: string;
    depth: number;
    menu_id: number;
  }

  export interface Depth2 {
    name: string;
    depth: number;
    menu_id: number;
  }

  export interface Depth3 {
    name: string;
    depth: number;
    menu_id: number;
  }

  export interface ClassMenu {
    class_code: string;
    menu: Depth1;
  }
}
