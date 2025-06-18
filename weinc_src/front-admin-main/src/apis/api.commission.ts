import apiRequest from '@/apis/axios.client';

export const commission = {
  get_commission_list: (target_id: number, query: string, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/commission?target_id=${target_id}${query}&offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_commission: (member_id: number, data: any) =>
    apiRequest
      .post(`/commission`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_commission: (id: number, value: number) =>
    apiRequest
      .put(`/commission`, JSON.stringify({ id: id, value: value }))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  delete_commission: (commission_id: number) =>
    apiRequest
      .delete(`/commission/${commission_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_default_commission: (member_id: number, kind: string = '') =>
    apiRequest
      .get(`/commission/default?member_id=${member_id}${kind}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_default_commission: (member_id: number, data: any) =>
    apiRequest
      .put(`/commission/default?member_id=${member_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_pg_commission_list: () =>
    apiRequest
      .get(`/commission/pg`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
