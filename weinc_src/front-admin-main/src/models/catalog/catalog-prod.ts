declare module 'CatalogProductModule' {
  export interface Option {
    code: string;
    status: string;
    supply_price: number;
    origin_price: number;
    selling_price: number;
    view_yn: string;
    default_yn: string;
  }

  export interface Photo {
    id: number;
    uri: string;
  }

  export interface Prod {
    id: number;
    name: string;
    code: string;
    type: string;
    status: string;
    view_yn: string;
    up_min?: number;
    up_max?: number;
    options: Option[];
    photos: Photo[];
  }

  export interface CatalogProd {
    id: number;
    variation: number;
    product: Prod;
  }

  export interface CatalogProductList {
    total: number;
    datas: CatalogProd[];
  }

  export interface Catalog {
    id: number;
    name: string;
    description: string;
    member_id: number;
    open: string;
    reg_date: string;
    mod_date: string;
    status: string;
    member: {
      id: number;
      name: string;
      email: string;
    };
  }

  export interface CatalogDataList {
    total: number;
    datas: Catalog[];
  }
}
