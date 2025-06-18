import apiRequest from '@/apis/axios.client';
import type { IBrand } from '@/components/product/type';
import type { OptionListInfo } from 'ProductListModule';

export interface IProductAdditional {
  common_info?: ICommonInfo;
  shipping_info?: IShippingInfo;
  options?: IProductOption[];
  photos?: IProductPhoto[];
}

export interface ICommonInfo {
  id?: number;
  name: string;
  contents: string;
  status?: string;
  reg_date?: string;
  mod_date?: string;
}

export interface IShippingArea {
  id: number;
  name: string;
  cost: number;
  shipping_cost_id: number;
  shipping_area_details: Array<IShippingAreaDetail>;
}

export interface IShippingInfo {
  id?: number;
  name: string;
  type: string;
  pay_type: string;
  calc_type: string;
  return_cost: number;
  change_cost: number;
  status: string;
  reg_date: string;
  mod_date: string;
  shipping_costs?: IShippingCost[];
}

export interface IShippingCost {
  id: number;
  type: string;
  category: string;
  cost: number;
  section_start: number;
  section_end: number;
  section_repeat: number;
  shipping_info_id: number;
  shipping_areas?: IShippingArea[];
}

export interface IShippingAreaDetail {
  id: number;
  category_text: string;
  zipcode: string;
  address_house: string;
  address_street: string;
  shipping_area_id: number;
}

export interface IProductPhoto {
  id: number;
  uri: string;
}

export interface IProductOption {
  id?: number;
  code?: string;
  supply_price: number;
  origin_price: number;
  selling_price: number;
  view_yn?: string;
  default_yn: string;
  count: number;
  safe_count: number;
  day_able_count: number;
  use_acc_qty: string;
  weight: number;
  property_detail_ids?: number[];
}

export interface IProduct extends IProductAdditional {
  id?: number;
  member_id?: number;
  name?: string;
  type?: string;
  view_yn?: string;
  code?: string;
  summary?: string;
  keyword?: string;
  contents?: string;
  tax?: string;
  min_purchase_limit?: number | string;
  max_purchase_limit?: number | string;
  adult?: string;
  hscode?: string;
  ipcc_yn?: string;
  cancel_yn?: string;
  resale?: string;
  video?: string;
  memo?: string;
  common_info_id?: number;
  shipping_info_id?: number;
  inven_use?: string;
  coupon_yn?: string;
  tel?: string;
  address?: string;
  address_detail?: string;
  lat?: string;
  lng?: string;
  brands?: IBrand[];
  common_info?: ICommonInfo;
  shipping_info?: IShippingInfo;
  option_use?: string;
  barcode?: string;
  user_limit?: number | string;
  use_end_period?: number | string;
  use_end_date?: string;
  sale_start_date?: string;
  sale_end_date?: string;
  sale_start_time?: string;
  sale_end_time?: string;
  subtitle?: string;
  view_inventory?: string;
  view_end_time?: string;
  pg_provider?: string;
  api_provider?: string;
  use_place?: string;
  api_goods_id?: string;
  user_limit_reset?: string;
}

export interface ILinkCategory {
  productId: number;
  categoryId: number[];
}

export interface ILinkBrand {
  productId: number;
  brandId: number[];
}

export interface IRegAdditionalInfo {
  productId: number;
  contents: string;
  category: string;
}

export interface INotice {
  product_id: number;
  item: string;
  category: string;
  contents: string;
  sort: number;
}

export const product = {
  getProduct: (id: number) =>
    apiRequest
      .get(`/product/${id}`)
      .then(res => res.data)
      .catch(err => err),
  getProducts: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/product?${query}offset=${offset}&limit=${limit}`)
      .then(res => res.data)
      .catch(err => err),
  checkProductCode: (code: string) =>
    apiRequest
      .get(`/product/exist`, { params: { code } })
      .then(res => res.data)
      .catch(err => err),
  makeProduct: (data: IProduct) =>
    apiRequest
      .post('/product', data)
      .then(res => res.data)
      .catch(err => err),
  linkBrand: ({ productId, brandId }: ILinkBrand) =>
    apiRequest
      .post(`/product/brand/link`, brandId, { params: { product_id: productId } })
      .then(res => res.data)
      .catch(err => err),
  unlinkBrand: (productId: number) =>
    apiRequest
      .delete(`/product/brand/link?product_id=${productId}`)
      .then(res => res.data)
      .catch(err => err),
  linkCategory: ({ productId, categoryId }: ILinkCategory) =>
    apiRequest
      .post(`/product/category/link`, categoryId, { params: { product_id: productId } })
      .then(res => res.data)
      .catch(err => err),
  unlinkCategory: (productId: number) =>
    apiRequest
      .delete(`/product/category/link?product_id=${productId}`)
      .then(res => res.data)
      .catch(err => err),
  // 상품 상세설명 이미지 업로드
  uploadForExplanInfo: (formData: FormData) =>
    apiRequest
      .post('/product/photo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(res => res.data),
  // 상품 수정
  updateBaseInfo: (productId: number, rest: IProduct) =>
    apiRequest
      .put(`/product/${productId}`, JSON.stringify({ ...rest }))
      .then(res => res.data)
      .catch(err => err),
  //TODO: 삭제예정
  regDefaultOption: ({ productId, ...rest }: IProductOption & { productId: number }) =>
    apiRequest
      .post(`product/${productId}/option`, rest)
      .then(res => res.data)
      .catch(err => err),
  //TODO: 삭제예정
  regCommonInfo: (data: ICommonInfo) =>
    apiRequest
      .post(`product/common-info/`, data)
      .then(res => res.data)
      .catch(err => err),
  // 상품 옵션 목록
  getProdOption: (prodId: number) =>
    apiRequest
      .get(`/product/${prodId}/option`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 옵션 등록
  addProdOption: (prodId: number, list: OptionListInfo[]) =>
    apiRequest
      .post(`/product/${prodId}/option`, JSON.stringify(list))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 옵션 삭제
  deleteProdOption: (prodId: number, list: number[]) =>
    apiRequest
      .delete(`/product/${prodId}/option`, { data: list })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 옵션 수정
  modProdOption: (prodId: number, list: any[]) =>
    apiRequest
      .put(`/product/${prodId}/option`, JSON.stringify(list))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 사진 등록
  regPhotoInfo: ({ productId, formData, query = '' }: { productId: number; formData: FormData; query?: string }) =>
    apiRequest
      .post(`/product/${productId}/info/photo${query}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(res => res.data)
      .catch(err => err),
  // 상품 사진 목록
  getProdPhotoInfo: (prodId: number) =>
    apiRequest
      .get(`/product/${prodId}/info/photo`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 사진 삭제
  deletePhotoInfo: (prodId: number, photoId: number) =>
    apiRequest
      .delete(`/product/${prodId}/info/photo/${photoId}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품정보제공고시 목록
  getProdNoticeInfo: (prodId: number) =>
    apiRequest
      .get(`/product/${prodId}/info/notice`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품정보제공고시 등록
  addProdNoticeInfo: (prodId: number, list: any[]) =>
    apiRequest
      .post(`/product/${prodId}/info/notice`, JSON.stringify(list))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  deleteProdNoticeInfo: (prodId: number, ids: number[]) =>
    apiRequest
      .delete(`/product/${prodId}/info/notice`, { data: ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  modProdNoticeInfo: (prodId: number, list: any[]) =>
    apiRequest
      .put(`/product/${prodId}/info/notice`, JSON.stringify(list))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 요청 등록
  reqProdReq: (data: { store_code: string; title: string; memo?: string; product_ids: number[] }) =>
    apiRequest
      .post(`/product/request`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 요청 목록
  reqProdList: (query: string, offset: number, limit: number = 20) =>
    apiRequest
      .get(`/product/request?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 요청 상세
  getProdReq: (reqId: number) =>
    apiRequest
      .get(`/product/request/${reqId}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 요청 수정
  modProdReq: (reqId: number, data: { status: string }) =>
    apiRequest
      .put(`/product/request/${reqId}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 요청 삭제
  deleteProdReq: (reqId: number) =>
    apiRequest
      .delete(`/product/request/${reqId}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품 배지 등록
  add_prod_badge: (data: any) =>
    apiRequest
      .post(`/product/badge`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 배지 목록
  get_prod_badge_list: (query: string = '') =>
    apiRequest
      .get(`/product/badge?${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품 배지 수정
  mod_prod_badge: (badge_id: number, data: any) =>
    apiRequest
      .put(`/product/badge/${badge_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품 배지 연결
  link_prod_badge: (prod_id: number, badge_ids: number[]) =>
    apiRequest
      .post(`/product/badge/link?product_id=${prod_id}`, JSON.stringify(badge_ids))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품 배지 연결 해제
  unlink_prod_badge: (prod_id: number, badge_ids: number[]) =>
    apiRequest
      .delete(`/product/badge/link?product_id=${prod_id}`, { data: badge_ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품에 연결된 배지 목록
  get_prod_link_badge_list: (prod_id: number) =>
    apiRequest
      .get(`/product/${prod_id}/badge`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품 qna 목록
  getProdQnaList: (customer_id: number = 0, product_id: number = 0, member_id: number = 0, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/product/qna?customer_id=${customer_id}&product_id=${product_id}&member_id=${member_id}&offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 qna 상세
  getProdQna: (qna_id: number) =>
    apiRequest
      .get(`/product/qna/${qna_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 qna 답변 등록
  addProdQnaAnswer: (qna_id: number, data: any) =>
    apiRequest
      .post(`/product/qna/answer?qna_id=${qna_id}`, data)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 qna 답변 수정
  modProdQnaAnswer: (answer_id: number, data: any) =>
    apiRequest
      .put(`/product/qna/answer/${answer_id}`, data)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 리뷰 목록
  getProdReviewList: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/product/review?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 리뷰 삭제
  delProdReview: (review_id: number) =>
    apiRequest
      .put(`/product/review/${review_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 리뷰 사진 삭제
  delProdReviewPhoto: (review_id: number, photo_id: number) =>
    apiRequest
      .delete(`/product/review/${review_id}/photo/${photo_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 그룹 상품 목록
  getProdGroupList: (product_id: number, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/product/${product_id}/group?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 그룹 상품 연결
  addProdToGroup: (product_id: number, prod_ids: number[]) =>
    apiRequest
      .post(`/product/${product_id}/group-link`, JSON.stringify(prod_ids))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 그룹 상품 연결 해제
  deleteProdFromGroup: (product_id: number, prod_ids: number[]) =>
    apiRequest
      .delete(`/product/${product_id}/group-link`, { data: prod_ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상품 로그
  getProdLog: (product_id: number, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/product/${product_id}/log?offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상품 추가 정보 목록
  get_prod_extra_info: (prod_id: number) =>
    apiRequest
      .get(`/product/${prod_id}/info/extra`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 추가정보 등록
  add_prod_extra_info: (prod_id: number, list: { id?: number; product_id?: number; category: string; contents: string }[]) =>
    apiRequest
      .post(`/product/${prod_id}/info/extra`, JSON.stringify(list))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 추가 정보 수정
  mod_prod_extra_info: (prod_id: number, list: { id: number; category: string; contents: string }[]) =>
    apiRequest
      .put(`/product/${prod_id}/info/extra`, JSON.stringify(list))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상품 추가정보 삭제
  delete_prod_extra_info: (prod_id: number, list: number[]) =>
    apiRequest
      .delete(`/product/${prod_id}/info/extra`, { data: list })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  get_api_provider_List: () =>
    apiRequest
      .get('/value/option?option_type=e_coupon_provider')
      .then(res => res.data)
      .catch(err => err),

  // 상품 일괄상태변경
  update_status: (status: string, list: number[]) =>
    apiRequest
      .put(`/product/update_status`, { status: status, product_ids: list })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
