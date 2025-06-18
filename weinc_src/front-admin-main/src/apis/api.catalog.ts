import apiRequest from '@/apis/axios.client';

export const catalog = {
  add_catalog: (name: string, description: string, member_id: number, status: string) =>
    apiRequest
      .post('/catalog', JSON.stringify({ name: name, description: description, member_id: member_id, status: status }))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 카탈로그 목록
  get_list: (query: string | null = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/catalog?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_catalog_info: (cid: string) =>
    apiRequest
      .get(`/catalog/${cid}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 카탈로그 상품 목록
  get_catalog_prod: (query: string = '', cid: string, offset: number, limit: number = 20) =>
    apiRequest
      .get(`/catalog/${cid}/product?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_catalog_store: (query: string = '', cid: string, offset: number, limit: number = 20) =>
    apiRequest
      .get(`/catalog/${cid}/store?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_catalog: (id: number, mod_data: object) =>
    apiRequest
      .put(`/catalog/${id}`, JSON.stringify(mod_data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_prod_to_catalog: (cId: string, pList: number[]) =>
    apiRequest
      .post(`/catalog/${cId}/product/link`, JSON.stringify(pList))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  delete_prod_to_catalog: (cId: string, pList: number[]) =>
    apiRequest
      .delete(`/catalog/${cId}/product/link`, { data: pList })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_store_to_catalog: (cId: string, sCode: string) =>
    apiRequest
      .post(`/catalog/${cId}/store/link?store_code=${sCode}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  delete_store_to_catalog: (cId: string, sCode: string) =>
    apiRequest
      .delete(`/catalog/${cId}/store/link?store_code=${sCode}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 카탈로그 상품 가격 변동값 일괄 설정
  mod_all_catalog_variation: (cId: string, variation: number) =>
    apiRequest
      .put(`/catalog/${cId}/product/variation?variation=${variation}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_catalog_prod_variation: (cId: string, variation: number, pIds: number[]) =>
    apiRequest
      .put(`/catalog/${cId}/product/variation?variation=${variation}`, JSON.stringify(pIds))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
