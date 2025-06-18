declare module 'SettingValueModule' {
  export interface SettingValue {
    id?: number;
    type?: string;
    name?: string;
    value?: string;
    description?: string;
  }

  export interface OptionValue {
    id?: number;
    type?: string;
    name?: string;
    value?: string;
    sort?: number;
  }
}
