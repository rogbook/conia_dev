export type useType = 'Y' | 'N';
export interface IProductBasInfo {
  editMode: boolean;
  categories?: [];
  brands?: [];
  productName?: string;
  productCode?: string;
  words?: string;
  desc?: string;
}

export interface ICategory {
  id: number;
  name: string;
  status?: string;
  description?: string;
  reg_date?: string;
  mod_date?: string;
  photo?: string;
  pid?: number;
  sub?: [];
}

export interface IBrand {
  id: number;
  description?: string;
  mod_date?: string;
  name: string;
  photo?: string;
  pid?: number | null;
  reg_date?: string;
  status?: 'Y' | 'N';
  sub?: unknown;
}
