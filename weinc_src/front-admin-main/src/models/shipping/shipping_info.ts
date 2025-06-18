declare module 'ShippingInfoModule' {
  export interface AddShippingInfo {
    type: string;
    category: string;
    cost: number;
    section_start?: number;
    section_end?: number;
    section_repeat?: number;
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
    member: {
      id: number;
      name: string;
      email: string;
      company: {
        id: number;
        name: string;
      };
    };
    shipping_costs: ShippingCost[];
  }
}
