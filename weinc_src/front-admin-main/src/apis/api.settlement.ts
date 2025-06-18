import apiRequest from '@/apis/axios.client';

export const settlement = {
  get_list: (member_id: number, query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/settlement?member_id=${member_id}${query}&offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_ship_list: (member_id: number, query: string = '') =>
    apiRequest
      .get(`/settlement/shipping?member_id=${member_id}${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_settlement_members: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/settlement/member?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_settlements: (data: { ids: number[]; status?: string; date_range?: string; reject?: string }) =>
    apiRequest
      .post(`/settlement`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_ship_settlement_members: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/settlement/shipping/member?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_ship_settlements: (data: { ids: number[]; status?: string; date_range?: string; reject?: string }) =>
    apiRequest
      .post(`/settlement/shipping`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_settlement_history: (target: number, kind: string) =>
    apiRequest
      .get(`/settlement/history/${target}?kind=${kind}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 정산 내역 엑셀 요청
  req_settlement_excel: (query: string) =>
    apiRequest
      .post(`/settlement/excel?${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 정산 엑셀 요청 목록
  list_req_settlement_excel: () =>
    apiRequest
      .get(`/settlement/excel`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
