declare module 'StoreProdListInfoMOdule' {
  export interface Option {
    code: string;
    supply_price: number;
    origin_price: number;
    selling_price: number;
    view_yn: string;
    default_yn: string;
    status: string;
  }

  export interface Photo {
    id: number;
    uri: string;
  }

  export interface Product {
    id: number;
    name: string;
    code: string;
    type: string;
    status: string;
    view_yn: string;
    options: Option[];
    photos: Photo[];
  }

  export interface StoreProd {
    id: number;
    view_yn: string;
    variation: number;
    product: Product;
  }

  export interface StoreProdList {
    total: number;
    datas: StoreProd[];
  }
}
