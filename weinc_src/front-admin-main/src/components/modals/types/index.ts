export type COLUMN_SELECTION = 'getCategories' | 'getBrands';

export type COLUMN_SELECTION_ID = 'modalCategory' | 'modalBrands';

export enum IColumnType {
  ONE = 'col-12',
  TWO = 'col-md-6 col-12',
  THREE = 'col-md-4 col-12',
  FOUR = 'col-md-3 col-12',
  DEFAULT = 'col-md col-12',
}

export enum MULTI_COLUMN_ORDER {
  'FIRST',
  'SECOND',
  'THIRD',
  'FOURTH',
}
