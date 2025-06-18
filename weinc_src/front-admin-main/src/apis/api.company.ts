import apiRequest from '@/apis/axios.client';

export const company = {
  // 회사 정보 (본인)
  me: () =>
    apiRequest
      .get('/company/me')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 회사 정보
  get_company: (id: string | number) =>
    apiRequest
      .get(`/company/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  //회사정보 수정
  mod_company: (id: string | number, info: object) =>
    apiRequest
      .put(`/company/${id}`, JSON.stringify(info))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),
  // 사진정보 수정
  mod_company_photo: (id: string | number, data: any) =>
    apiRequest
      .put(`/company/${id}/photo`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 매장정보 상세
  get_shop: (id: number) =>
    apiRequest
      .get(`/shop/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  //매장정보 등록
  reg_shop: (id: number, data: object) =>
    apiRequest
      .post(`/shop/${id}`, JSON.stringify(data))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),

  //매장정보 수정
  mod_shop: (id: number, data: object) =>
    apiRequest
      .put(`/shop/${id}`, JSON.stringify(data))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),

  // 상점 배지 연결
  link_shop_badge: (id: number, badge_ids: number[]) =>
    apiRequest
      .post(`/shop/badge/link?shop_id=${id}`, JSON.stringify(badge_ids))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 배지 연결 해제
  unlink_shop_badge: (id: number, badge_ids: number[]) =>
    apiRequest
      .delete(`/shop/badge/link?shop_id=${id}`, { data: badge_ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
