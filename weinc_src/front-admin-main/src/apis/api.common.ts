import apiRequest from '@/apis/axios.client';
import type { FavOpt } from 'FavOptListInfo';

export const common = {
  uploadImage: (url: string, formData: FormData) =>
    apiRequest
      .post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(res => res.data),
  getBankList: () =>
    apiRequest
      .get('/value/option?option_type=bank_list')
      .then(res => res.data)
      .catch(err => err),
  getLogisticsList: () =>
    apiRequest
      .get('/value/option?option_type=logistics')
      .then(res => res.data)
      .catch(err => err),
  getSettingValueOne: (type: string) =>
    apiRequest
      .get(`/value/setting?setting_type=${type}`)
      .then(res => res.data)
      .catch(err => err),
  getOptionValue: (type: string) =>
    apiRequest
      .get(`/value/option?option_type=${type}`)
      .then(res => res.data)
      .catch(err => err),
  getCategories: (params: { pid?: number; name?: string; offset?: number; limit?: number } = {}) =>
    apiRequest
      .get(`/product/category`, { params: params.pid ? params : null })
      .then(res => res.data)
      .catch(err => err),
  addCategory: (data: { pid?: number; name: string }) =>
    apiRequest
      .post(`/product/category`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  modCategory: (cateId: number, data: any) =>
    apiRequest
      .put(`/product/category/${cateId}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  getBrands: (params: { pid?: number; name?: string; offset?: number; limit?: number } = {}) =>
    apiRequest
      .get(`/product/brand`, { params })
      .then(res => res.data)
      .catch(err => err),
  addBrand: (data: { name: string; description?: string; photo?: string; pid?: number }) =>
    apiRequest
      .post('/product/brand', JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  modBrand: (brandId: number, data: { name: string; description?: string; photo?: string; pid?: number }) =>
    apiRequest
      .put(`/product/brand/${brandId}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  getNoticeInfo: (category: string = '') =>
    apiRequest
      .get(`/value/notice-info-template${category}`)
      .then(res => res.data)
      .catch(err => err),

  get_prod_common_info_list: (query: string = '') =>
    apiRequest
      .get(`/product/common-info${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  reg_prod_common_info: (data: { name: string; content: string; member_id?: number }) =>
    apiRequest
      .post(`/product/common-info`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_prod_common_info: (id: string | number) =>
    apiRequest
      .get(`/product/common-info/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_prod_common_info: (id: string | number, data: { name?: string; content?: string; status?: string }) =>
    apiRequest
      .put(`/product/common-info/${id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_prod_common_info_template: (member_id: number) =>
    apiRequest
      .get(`/product/common-info/template?member_id=${member_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 자주쓰는상품옵션 목록
  getFavoriteOptionList: () =>
    apiRequest
      .get(`/value/favorite-option`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 자주쓰는상품옵션 등록
  regFavoriteOption: (data: FavOpt) =>
    apiRequest
      .post(`/value/favorite-option`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 자주쓰는상품옵션 삭제
  deleteFavoriteOption: (id: number) =>
    apiRequest
      .delete(`/value/favorite-option/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 사용 가능한 메뉴
  get_auth_menu: () =>
    apiRequest
      .get(`/auth/menu`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //공통 이미지 등록
  upload_photo: (img: File, path: string) =>
    apiRequest
      .post(
        `/photo?path=${path}`,
        { file: img },
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
};
