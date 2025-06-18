declare module 'CatalogStoreModule' {
  export interface Store {
    code: string;
    title: string;
    status: string;
  }

  export interface CatalogStore {
    id: number;
    store: Store;
  }

  export interface CatalogStoreList {
    total: number;
    datas: CatalogStore[];
  }
}
