import apiRequest from '@/apis/axios.client';

export const customer = {
  // 고객 회원 목록
  get_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/customer?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 고객 회원 상세
  get_customer: (id: string, target: string) =>
    apiRequest
      .get(`/customer/${id}?target=${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 고객 회원 수정
  mod_customer: (id: string, info: object) =>
    apiRequest
      .put(`/customer/${id}`, JSON.stringify(info))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 고객 회원 목록 엑셀 다운로드
  user_list_excel: (query: string) =>
    apiRequest
      .get(`/customer/excel?${query}`, { responseType: 'blob' })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 고객 회원일괄 추가 (Excel)
  add_store_customer_list: (store_code: string, data_excel: File) =>
    apiRequest
      .put(
        `/customer/bulk_excel_customer?store_code=${store_code}`,
        { file: data_excel },
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      )
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 고객회원 임시 비밀번호 발급
  temp_password: (customer_id: string) =>
    apiRequest
      .put(`/customer/${customer_id}/force-change-passwd`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
