import apiRequest from '@/apis/axios.client';

export const order = {
  // 주문 상품 목록
  get_order_list: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/order?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 주문 상세
  get_order_detail: (order_id: number) =>
    apiRequest
      .get(`/order/${order_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 주문 수정
  mod_order_detail: (order_id: number, data: any) =>
    apiRequest
      .put(`/order/${order_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 일괄 준비중 변경
  delivery_wait_update_select: (status: string, order_prod_ids: number[]) =>
    apiRequest
      .put(`/order/update_status`, JSON.stringify({ status: status, order_product_ids: order_prod_ids }))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 배송 등록 (출고 처리)
  order_shipping_reg: (o_ship_id: number, deliveryInfo: { delivery_code: string; delivery_provider: string; delivery_provider_code: string }) =>
    apiRequest
      .put(`/order/shipping/${o_ship_id}`, JSON.stringify(deliveryInfo))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 배송상품 배송완료 강제변경
  order_shipping_force_end: (o_ship_id: number) =>
    apiRequest
      .put(`/order/shipping/${o_ship_id}/force_end`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 주문상품 강제 구매확정
  order_force_end: (order_id: string, order_prod_id: number) =>
    apiRequest
      .put(`/order/${order_id}/force_end/${order_prod_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 교환/반품 목록
  get_exre_list: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/order/re?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 교환/반품 상세
  // TODO: 삭제 예정 (사유: 사용안함)
  get_exre_detail: (re_id: number) =>
    apiRequest
      .get(`/order/re/${re_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //교환/반품 상태 변경
  mod_exre_status: (re_id: number, data: any) =>
    apiRequest
      .put(`/order/re/${re_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  //주문 부분 취소
  order_cancel_exre: (order_id: string, data: any) =>
    apiRequest
      .post(`/order/${order_id}/cancel_part`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 교환 주문 생성
  order_exchange: (order_prod_id: number, exchange_prod_op_id: string, amount: number, count: number) =>
    apiRequest
      .post(`/order/exchange?order_product_id=${order_prod_id}&exchange_product_option_id=${exchange_prod_op_id}&amount=${amount}&count=${count}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  //주문 로그
  getOrderLog: (order_id: string, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/order/${order_id}/log?offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 주문 취소
  order_all_cancel: (order_id: string) =>
    apiRequest
      .post(`/order/${order_id}/cancel`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 주문 부분취소
  order_part_cancel: (order_id: string, data: { cancel_amount: number; order_product_ids: string[]; order_shipping_ids: string[] }) =>
    apiRequest
      .post(`/order/${order_id}/cancel_part`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 주문 취소 내역
  order_cancel_list: (order_id: string) =>
    apiRequest
      .get(`/order/${order_id}/cancel`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 주문내역 엑셀 다운로드
  order_list_excel: (query: string) =>
    apiRequest
      .get(`/order/excel?${query}`, { responseType: 'blob' })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 주문상품 기간 연장
  prod_use_date_extension: (o_id: string, op_id: number, use_end_date: string) =>
    apiRequest
      .put(`/order/${o_id}/period/${op_id}?use_end_date=${use_end_date}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 관리자 환불 내역 목록
  get_refund_list: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/order/admin-refund?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 관리자 환불 기능
  order_admin_refund: (order_id: string, amount: number) =>
    apiRequest
      .put(`/order/${order_id}/admin-refund?amount=${amount}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 송장번호 일괄등록용 엑셀파일 생성
  order_bulk_excel_ship_down: () =>
    apiRequest
      .get(`/order/bulk_excel_shipping`, { responseType: 'blob' })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  // 송장번호 일괄등록 업로드
  order_bulk_excel_ship_upload: (file: File) =>
    apiRequest
      .put(
        `/order/bulk_excel_shipping`,
        { file: file },
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
