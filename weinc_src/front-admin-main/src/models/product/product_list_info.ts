declare module 'ProductListInfoModule' {
  export interface ProductListInfo {
    total: number;
    datas: Prod[];
  }

  export interface Brand {
    id: number;
    name: string;
  }

  export interface Category {
    id: number;
    name: string;
    depth: number;
    depth1_name: string | null;
    depth2_name: string | null;
    depth3_name: string | null;
    depth4_name: string | null;
    depth1_id: number | null;
    depth2_id: number | null;
    depth3_id: number | null;
    depth4_id: number | null;
  }

  export interface Prod {
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
    min_purchase_limit: string;
    max_purchase_limit: string;
    adult: string;
    hscode: string;
    reg_date: string;
    mod_date: string;
    ipcc_yn: string;
    cancel_yn: string;
    resale: string;
    confirm: string;
    video: string;
    memo: string;
    common_info_id: number;
    shipping_info_id: number;
    inven_use: string;
    coupon_yn: string;
    option_use: string;
    barcode: string;
    user_limit: string | number;
    use_end_period: number | string;
    use_end_date: string;
    sale_start_date: string;
    sale_end_date: string;
    sale_start_time: string;
    sale_end_time: string;
    tel: string;
    address: string;
    address_detail: string;
    lat: string;
    lng: string;
    subtitle: string;
    view_inventory: string; // default = 'N'
    view_end_time: string;
    member: Member;
    categories: Category[];
    brands: Brand[];
    common_info: CommonInfo;
    shipping_info: ShippingInfo;
    options: Option[];
    photos: Photo[];
    badges: Badge[];
    up_min?: number;
    up_max?: number;
    pg_provider: string;
    api_provider: string;
    use_place: string;
    api_goods_id: string;
    user_limit_reset: string;
  }
  export interface CommonInfo {
    id: number;
    name: string;
    contents: string;
    status: string;
    reg_date: string;
    mod_date: string;
    member_id: number;
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
    reg_date: string;
    mod_date: string;
    shipping_costs: ShippingCost[];
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
  export interface ShippingArea {
    id: number;
    name: string;
    cost: number;
    shipping_cost_id: number;
    shipping_area_details: ShippingAreaDetail[];
  }
  export interface ShippingAreaDetail {
    id: number;
    category_text: string;
    zipcode: string;
    address_house: string;
    address_street: string;
    shipping_area_id: number;
  }

  export interface Member {
    email: string;
    name: string;
    company: Company;
  }

  export interface Company {
    id: number;
    name: string;
  }

  export interface Option {
    code?: string;
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
  export interface Badge {
    id: number;
    name: string;
    color: string;
    shape: string;
    imt: string;
  }

  export interface Log {
    total: number;
    datas: Data[];
  }

  export interface Data {
    action: string;
    msg: string;
    writer: string;
    reg_date: string;
  }
}
