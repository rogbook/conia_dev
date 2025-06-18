export interface JoinStep {
  step: STEP;
}

export enum STEP {
  BASE_INFO,
  ADMIN_INFO,
  COMPLETE,
}

export interface IValidCommon {
  check: boolean;
  err_msg: string;
}

export interface IEmail extends IValidCommon {
  value: string;
}

export interface IPassword extends IValidCommon {
  password: string;
  chkPassword: string;
  pwdValidate: string;
}

export interface IName extends IValidCommon {
  value: string;
}

export interface IPhone extends IValidCommon {
  phoneNumber: string;
  validNumber: string;
}

export interface IAddress extends IValidCommon {
  zonecode: string;
  baseAddress: string;
  detailAddress: string;
}

export interface IUseAgree extends IValidCommon {
  all: boolean;
  use: boolean;
  sales: boolean;
  priv: boolean;
}

export interface IDaumPostcodeApi {
  jibunAddress: string;
  roadAddress: string;
  userSelectedType: 'R' | 'J';
  zonecode: string;
}
