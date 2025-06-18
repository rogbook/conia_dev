declare module 'CompanyInfoModule' {
  import type { User } from 'UserInfoModule';
  export interface Company {
    id: number;
    member_id: number;
    name: string;
    ceo: string;
    reg_no: string;
    biz_type: string;
    biz_item: string;
    zipcode: string;
    address: string;
    address_detail: string;
    phone: string;
    mobile: string;
    corp_type: string;
    corp_number: string;
    tax_email: string;
    bank: string;
    account: string;
    bank_user: string;
    photo_reg: string;
    photo_bank: string;
    status: string;
    reg_date: Date;
    mod_date: Date;
    manager_name: string;
    manager_phone: string;
    manager_mobile: string;
    manager_email: string;
    settlement_name: string;
    settlement_phone: string;
    settlement_mobile: string;
    settlement_email: string;
    cs_name: string;
    cs_phone: string;
    cs_mobile: string;
    cs_email: string;
    network_reg_no: string;
    member: User;
  }
}
