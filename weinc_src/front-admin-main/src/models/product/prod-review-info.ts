declare module 'ProdReviewInfo' {
  export interface ProdReviewList {
    total: number;
    datas: ProdReview[];
  }

  export interface ProdReview {
    id: number;
    product_id: string;
    title: string;
    contents: string;
    rating: number;
    status: string;
    reg_date: string;
    mod_date: string;
    order_info: string;
    order_product_id: number;
    customer_id: number;
    customer: Customer;
    product: Product;
    photos: Photos[];
  }

  export interface Customer {
    id: number;
    name: string;
  }

  export interface Product {
    id: number;
    code: string;
    name: string;
    photos: Photo[];
  }

  export interface Photo {
    id: number;
    uri: string;
  }

  export interface Photos {
    id: number;
    uri: string;
  }
}
