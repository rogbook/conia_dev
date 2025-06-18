declare module 'FavOptListInfo' {
  export interface FavProperty {
    code: string;
    value: string;
    price: number;
  }

  export interface FavOpt {
    id?: number;
    name: string;
    type: string;
    propertys: FavProperty[];
  }
}
