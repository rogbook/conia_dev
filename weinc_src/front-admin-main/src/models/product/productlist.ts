declare module 'ProductListModule' {
  export interface Item {
    id: number;
    code: string;
    name: string;
    img: string;
    price: number;
    brand: string;
    sales_price: number;
    stack: string;
    delivery_fee: string;
    created_at: Date;
    updated_at: Date;
    status: string;
    visible: string;
  }

  export interface Opt {
    id?: number;
    type: OptionType;
    code: string;
    name: string;
    value: string;
    price: string;
  }

  export interface OptionType {
    value: string;
    name: string;
  }

  export interface OptChild {
    id: number;
    options: OptionType[];
    weight: number;
    stack: number;
    sale_price: number;
    supply_price: number;
    normal_price: number;
    visible: string;
    is_standard: boolean;
  }

  export interface OptionListInfo {
    id?: number;
    code?: string;
    view_yn: string;
    default_yn: string;
    status?: string;
    product_id?: number;
    weight: number;
    supply_price: number;
    origin_price: number;
    selling_price: number;
    count?: number;
    safe_count: number;
    day_able_count: number;
    use_acc_qty: string;

    option_title?: string;
    option_1?: string;
    option_2?: string;
    option_3?: string;
    option_4?: string;
    option_5?: string;

    option_code_1?: string;
    option_code_2?: string;
    option_code_3?: string;
    option_code_4?: string;
    option_code_5?: string;

    option_tmp_price?: string;

    inventory: {
      id?: number;
      count: number;
      safe_count: number;
      day_able_count: number;
      use_acc_qty: string;
    };
  }
}
