import apiRequest from '@/apis/axios.client';
import type { DETECTED_M_TYPE } from '@/utils/machineDetector';
import { showLogConsole } from '@/utils/common-utils';

export interface IBaseInfo {
  email: string; // VARCHAR(45)
  password: string; // VARCHAR(256) 암호화기준
  name: string; //VARCHAR 32
  nickname: string; // VARCHAR 32
  mailling: string; // VARCHAR 1 default 'N'
  sms: string; //VARCHAR 1 default 'N'
  mobile: string; //VARCHAR 128
  join_platform: DETECTED_M_TYPE; // navigator.userAgentData
  referer: string;
  referer_domain: string;
  status: string;
  recommend: string;
}

export interface IAdditionalInfo {
  member_id: number; // INT NOT NULL
  name?: string; //VARCHAR 45
  ceo?: string; // VARCHAR(45)
  reg_no?: string; // VARCHAR(45)
  biz_type?: string; //VARCHAR(45)
  biz_item?: string; //VARCHAR(45)
  zipcode?: string; //VARCHAR(256)
  address?: string; // VARCHAR(256)
  address_detail?: string; // VARCHAR(128)
  mobile?: string; // VARCHAR(32)
  corp_type?: string; // VARCHAR(3) NOT NULL
  corp_number?: string; // VARCHAR(45) NOT NULL
  tax_email: string; // VARCHAR(128)
  bank: string; // VARCHAR(16)
  account: string; // VARCHAR(45)
  bank_user: string; // VARCHAR(45)
  photo_reg?: File | undefined; // VARCHAR(512)
  photo_bank: File | undefined; // VARCHAR(512)

  manager_name?: string; //VARCHAR(32)
  manager_phone?: string; // VARCHAR(32)
  manager_mobile?: string; // VARCHAR(32)
  manager_email?: string; //VARCHAR(128)

  settlement_name?: string; //VARCHAR(32)
  settlement_phone?: string; // VARCHAR(32)
  settlement_mobile?: string; // VARCHAR(32)
  settlement_email?: string; //VARCHAR(128)

  cs_name?: string; //VARCHAR(32)
  cs_phone?: string; // VARCHAR(32)
  cs_mobile?: string; // VARCHAR(32)
  cs_email?: string; //VARCHAR(128)
}

export const join = {
  checkIdIsValid: (email: string) =>
    apiRequest
      .get('/member/exist', { params: { email } })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  phCertReq: (host: string | null = null) =>
    apiRequest
      .post('/auth/cert-niceid', JSON.stringify({ return_url: `${host}/user/mobileCertResult` }))
      .then(res => {
        return res.data;
      })
      .catch(err => err),
  phCertResult: (token_version_id: string, enc_data: string, integrity_value: string) =>
    apiRequest
      .post('/auth/cert-niceid-verify', JSON.stringify({ token_version_id: token_version_id, enc_data: enc_data, integrity_value: integrity_value }))
      .then(res => {
        return res.data;
      })
      .catch(err => err),
  phCertVerify: (phoneNumber: string, certNumber: string) =>
    apiRequest
      .post('/auth/cert-sms-req', { mobile: phoneNumber, code: certNumber })
      .then(res => {
        return res.data;
      })
      .catch(err => err),
  onSubmitBaseInfo: (datas: IBaseInfo) =>
    apiRequest
      .post('/member', datas)
      .then(res => {
        return res.data;
      })
      .catch(err => err),
  onSubmitAdditionalInfo: ({ ...datas }: IAdditionalInfo) =>
    apiRequest
      .post('/company', datas, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(res => res.data)
      .catch(err => {
        showLogConsole(err, 'err');
        return err;
      }),
};
