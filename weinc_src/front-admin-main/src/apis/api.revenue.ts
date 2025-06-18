import apiRequest from '@/apis/axios.client';
export const revenue = {
  // 오프라인 매출 목록
  get_revenue_offline: (query: string = '', offset: number, limit: number = 20) =>
    apiRequest
      .get(`/revenue/offline?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 오프라인 매출 Excel 업로드
  add_revenue_offline: (code: string, excel_file: File) =>
    apiRequest
      .post(
        `/revenue/offline`,
        { code: code, excel_file: excel_file },
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

  // 오프라인 매출 상태 수정
  mod_revenue_offline: (target_id: number, status: string) =>
    apiRequest
      .put(`/revenue/offline/${target_id}?status=${status}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 월별 매출
  get_revenue_month: (year: number, month: number) =>
    apiRequest
      .get(`/revenue/month?year=${year}&month=${month}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
