declare module 'ThemeProductListInfoModule' {
  export interface Brand {
    name: string;
  }

  export interface CommonInfo {
    id: number;
    name: string;
    contents: string;
    status: string;
    reg_date: Date;
    mod_date: Date;
  }

  export interface ShippingAreaDetail {
    id: number;
    category_text: string;
    zipcode: string;
    address_house: string;
    address_street: string;
    shipping_area_id: number;
  }

  export interface ShippingArea {
    id: number;
    name: string;
    cost: number;
    shipping_cost_id: number;
    shipping_area_details: ShippingAreaDetail[];
  }

  export interface ShippingCost {
    id: number;
    type: string;
    category: string;
    cost: number;
    section_start: number;
    section_end: number;
    section_repeat: number;
    shipping_info_id: number;
    shipping_areas: ShippingArea[];
  }

  export interface ShippingInfo {
    id: number;
    name: string;
    type: string;
    pay_type: string;
    calc_type: string;
    return_cost: number;
    change_cost: number;
    status: string;
    reg_date: Date;
    mod_date: Date;
    shipping_costs: ShippingCost[];
  }

  export interface Option {
    code: string;
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

  export interface Product {
    id: number;
    member_id: number;
    name: string;
    type: string;
    status: string;
    view_yn: string;
    code: string;
    summary: string;
    keyword: string;
    contents: string;
    tax: string;
    min_purchase_limit: number;
    max_purchase_limit: number;
    adult: string;
    hscode: string;
    reg_date: Date;
    mod_date: Date;
    ipcc_yn: string;
    cancel_yn: string;
    confirm: string;
    video: string;
    memo: string;
    common_info_id: number;
    shipping_info_id: number;
    inven_use: string;
    coupon_yn: string;
    brands: Brand[];
    common_info: CommonInfo;
    shipping_info: ShippingInfo;
    options: Option[];
    photos: Photo[];
  }

  export interface ThemeProductList {
    total: number;
    datas: Product[];
  }
}
