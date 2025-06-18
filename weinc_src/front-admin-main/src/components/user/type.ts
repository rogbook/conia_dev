export type TJoinType = 'P' | 'B' | 'PB' | 'PBS';
export interface IBankList {
  id: number;
  name: string;
  sort: number;
  type: string;
  value: string;
}

export interface ILogisticsList {
  id: number;
  name: string;
  sort: number;
  type: string;
  value: string;
}

export interface ISettingValueList {
  id: number;
  name: string;
  description: string;
  type: string;
  value: string;
}

export interface IPersonalJoin {
  member_id: number;
  corp_type: TJoinType;
  corp_number: string;
  tax_email: string;
  bank: string;
  bank_user: string;
  account: string;
  address: string;
  address_detail: string;
  zipcode: string;
  photo_bank: File;
}
