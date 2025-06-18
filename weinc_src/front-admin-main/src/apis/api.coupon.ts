import apiRequest from '@/apis/axios.client';
export const coupon = {
  // 쿠폰 생성
  reg_coupon: (data: object) =>
    apiRequest
      .post(`/coupon`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 쿠폰 목록
  get_coupon_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/coupon?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 쿠폰 상세
  get_coupon: (id: number) =>
    apiRequest
      .get(`/coupon/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 쿠폰 삭제
  del_coupon: (id: number) =>
    apiRequest
      .delete(`/coupon/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 쿠폰 발급
  add_coupon: (id: number, data: object) =>
    apiRequest
      .post(`/coupon/${id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //발급 쿠폰 목록
  get_published_coupon_list: (id: number, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/coupon/${id}/published?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 쿠폰 상태 수정
  mod_coupon_status: (group_id: number, status: string) =>
    apiRequest
      .put(`/coupon/${group_id}?status=${status}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
