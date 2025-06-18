import apiRequest from '@/apis/axios.client';
import type { Store } from 'StoreListInfoModule';

export const store = {
  // 상점 목록
  get_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 상세
  get_store: (code: string) =>
    apiRequest
      .get(`/store/${code}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 등록
  reg_store: (store: Store) =>
    apiRequest
      .post('/store', JSON.stringify(store))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),
  // 상점 수정
  mod_store: (code: string, modData: Store) =>
    apiRequest
      .put(`/store/${code}`, JSON.stringify(modData))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 코드 중복 체크
  check_store_code: (code: string) =>
    apiRequest
      .get(`/store/exist?code=${code}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_store_prod_list: (query: string = '', storeCode: string, offset: number, limit: number = 20) =>
    apiRequest
      .get(`/store/${storeCode}/product?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 상품 연결
  add_prod_to_store: (storeCode: string, catalogId: number, pList: any) =>
    apiRequest
      .post(`/store/${storeCode}/product/link?catalog_id=${catalogId}`, JSON.stringify(pList))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),
  delete_prod_to_store: (storeCode: string, pList: number[]) =>
    apiRequest
      .delete(`/store/${storeCode}/product/link`, { data: pList })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_store_theme_list: (storeCode: string, searchType: string = 'all') =>
    apiRequest
      .get(`/store/${storeCode}/theme/list/${searchType}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_store_theme: (storeCode: string, themeInfo: object) =>
    apiRequest
      .post(`/store/${storeCode}/theme`, JSON.stringify(themeInfo))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_store_theme: (storeCode: string, themeId: number, themeInfo: object) =>
    apiRequest
      .put(`/store/${storeCode}/theme/${themeId}`, JSON.stringify(themeInfo))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  uploadPhoto: (img: File) =>
    apiRequest
      .post(
        `/store/photo`,
        { file: img },
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      )
      .then(res => res.data)
      .catch(err => err),

  add_prod_to_theme: (storeCode: string, themeId: number, pList: number[]) =>
    apiRequest
      .post(`/store/${storeCode}/theme/${themeId}/link`, JSON.stringify(pList))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),
  delete_prod_to_theme: (storeCode: string, themeId: number, pList: number[]) =>
    apiRequest
      .delete(`/store/${storeCode}/theme/${themeId}/link`, { data: pList })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  get_theme_prod_list: (storeCode: string, themeId: number, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${storeCode}/theme/${themeId}/product?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_sub_store_list: (member_id: number) =>
    apiRequest
      .get(`/store/sub_store?member_id=${member_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 이용자 목록
  get_store_user_list: (store_code: string, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/user?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 이용자 상태 수정
  mod_store_user_status: (store_code: string, req_id: number, confirm: string) =>
    apiRequest
      .put(`/store/${store_code}/user/${req_id}`, JSON.stringify({ confirm: confirm }))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 이용자 삭제
  delete_store_user: (store_code: string, req_id: number) =>
    apiRequest
      .delete(`/store/${store_code}/user/${req_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  //전체 상점 qna 목록
  get_total_store_qna_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/board/qna-store?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상점 qna 목록
  get_store_qna_list: (customer_id: number = 0, store_code: string, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/board/qna-store`, {
        params: {
          customer_id: customer_id,
          store_code: store_code,
          offset: offset,
          limit: limit,
        },
      })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상점 qna 상세
  get_store_qna: (qna_id: number) =>
    apiRequest
      .get(`/board/qna-store/${qna_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상점 qna 답변 등록
  add_store_qna_answer: (qna_id: number, data: any) =>
    apiRequest
      .post(`/board/qna-store/answer?qna_id=${qna_id}`, data)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상점 qna 답변 수정
  mod_store_qna_answer: (answer_id: number, data: any) =>
    apiRequest
      .put(`/board/qna-store/answer/${answer_id}`, data)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상점 로고 이미지 등록
  uploadLogo: (store_code: string, logo_type: string, img: File) =>
    apiRequest
      .post(
        `/store/logo?store_code=${store_code}&logo_type=${logo_type}`,
        { file: img },
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      )
      .then(res => res.data)
      .catch(err => err),
  // 상점 이용 가능자 목록
  get_able_target_list: (store_code: string, q: string, offset: number = 0, limit: number = 10) =>
    apiRequest
      .get(`/store/${store_code}/able_target?${q}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이용 가능자 일괄 추가 (Excel)
  add_able_target: (store_code: string, data_excel: File) =>
    apiRequest
      .post(
        `/store/${store_code}/able_target`,
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
  // 상점 이용 가능자 개별 등록
  add_able_target_one: (store_code: string, data: { name: string; mobile: string; unique_value: string }) =>
    apiRequest
      .post(`/store/${store_code}/able_target/one`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이용 가능자 삭제
  delete_able_target: (store_code: string, target_id: number) =>
    apiRequest
      .delete(`/store/${store_code}/able_target/${target_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이용가능자 수정
  mod_able_target: (store_code: string, target_id: number, data: { name: string; mobile: string; unique_value: string; used: string }) =>
    apiRequest
      .put(`/store/${store_code}/able_target/${target_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이벤트팝업 목록
  get_store_popup_list: (store_code: string, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/popup?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이벤트팝업 등록
  reg_store_popup: (store_code: string, data: object) =>
    apiRequest
      .post(`/store/${store_code}/popup`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이벤트팝업 수정
  mod_store_popup: (store_code: string, target: number, data: object) =>
    apiRequest
      .put(`/store/${store_code}/popup/${target}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 이벤트팝업 삭제
  delete_store_popup: (store_code: string, target: number) =>
    apiRequest
      .delete(`/store/${store_code}/popup/${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시판그룹 목록
  get_store_board_group_list: (store_code: string, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/board-group?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시판그룹 생성
  reg_store_board_group: (store_code: string, data: object) =>
    apiRequest
      .post(`/store/${store_code}/board-group`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시판그룹 수정
  mod_store_board_group: (store_code: string, target: number, data: object) =>
    apiRequest
      .put(`/store/${store_code}/board-group/${target}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시판그룹 삭제
  delete_store_board_group: (store_code: string, target: number) =>
    apiRequest
      .delete(`/store/${store_code}/board-group/${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 목록
  get_store_board_list: (store_code: string, group_id: number, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/board?group_id=${group_id}&${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 생성
  reg_store_board: (store_code: string, data: object) =>
    apiRequest
      .post(`/store/${store_code}/board`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 수정
  mod_store_board: (store_code: string, target: number, data: object) =>
    apiRequest
      .put(`/store/${store_code}/board/${target}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 삭제
  delete_store_board: (store_code: string, target: number) =>
    apiRequest
      .delete(`/store/${store_code}/board/${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 게시글 댓글 목록
  get_store_board_comment: (store_code: string, board_id: number, query: string = '') =>
    apiRequest
      .get(`/store/${store_code}/board-comment?board_id=${board_id}&${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 댓글 등록
  reg_store_board_comment: (store_code: string, data: object) =>
    apiRequest
      .post(`/store/${store_code}/board-comment`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 댓글 수정
  mod_store_board_comment: (store_code: string, target: number, data: object) =>
    apiRequest
      .put(`/store/${store_code}/board-comment/${target}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 게시글 댓글 삭제
  delete_store_board_comment: (store_code: string, target: number) =>
    apiRequest
      .delete(`/store/${store_code}/board-comment/${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 게시글 댓글 엑셀 다운로드
  get_store_board_comment_excel: (store_code: string, board_id: number, query: string = '') =>
    apiRequest
      .get(`/store/${store_code}/board-comment/excel?board_id=${board_id}&${query}`, { responseType: 'blob' })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 테마 매장 목록
  get_theme_shop_list: (store_code: string, target: number, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/theme/${target}/shop?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 테마 매장 연결
  add_link_theme_shop: (store_code: string, target: number, ids: number[]) =>
    apiRequest
      .post(`/store/${store_code}/theme/${target}/shop_link`, JSON.stringify(ids))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 테마 매장 연결 해제
  delete_link_theme_shop: (store_code: string, target: number, ids: number[]) =>
    apiRequest
      .delete(`/store/${store_code}/theme/${target}/shop_link`, { data: ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 매장 목록
  get_store_shop: (store_code: string, query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/shop?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //상점 로그
  getStoreLog: (store_code: string, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/store/${store_code}/log?offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점 그룹 목록
  get_store_group_list: () =>
    apiRequest
      .get(`/store/group`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 카탈로그 상품 상점에 일괄 추가
  add_all_cata_prod: (store_code: string, cata_id: number) =>
    apiRequest
      .post(`/store/${store_code}/product/link/${cata_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점상품 추가설명등록 (개별)
  reg_store_prod_memo_list: (store_code: string, memo: string, prod_ids: number[]) =>
    apiRequest
      .post(`/store/${store_code}/product/memo/list`, { memo: memo, products: prod_ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점상품 추가설명삭제 (개별)
  delete_store_prod_memo_list: (store_code: string, prod_ids: number[]) =>
    apiRequest
      .delete(`/store/${store_code}/product/memo/list`, { data: prod_ids })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점상품 추가설명등록 (검색)
  reg_store_prod_memo_all: (store_code: string, memo: string, query: string) =>
    apiRequest
      .post(`/store/${store_code}/product/memo/search?${query}`, { memo: memo })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점상품 추가설명삭제 (검색)
  delete_store_prod_memo_all: (store_code: string, query: string) =>
    apiRequest
      .delete(`/store/${store_code}/product/memo/search?${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 상점상품 추가설명 정보 (단독)
  get_store_prod_memo: (store_code: string, prod_id: number) =>
    apiRequest
      .get(`/store/${store_code}/product/memo/${prod_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 상점 설정 복사 요청
  store_setting_copy: (store_code: string, data: object) =>
    apiRequest
      .put(`/store/${store_code}/copy-setting`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
