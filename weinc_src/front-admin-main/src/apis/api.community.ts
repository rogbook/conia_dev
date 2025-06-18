import apiRequest from '@/apis/axios.client';

export const community = {
  get_faq_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/board/faq?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  get_faq: (faq_id: number) =>
    apiRequest
      .get(`/board/faq/${faq_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_faq: (data: any) =>
    apiRequest
      .post(`/board/faq`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_faq: (faq_id: number, data: any) =>
    apiRequest
      .put(`/board/faq/${faq_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  del_faq: (faq_id: number) =>
    apiRequest
      .delete(`/board/faq/${faq_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  faq_cate_list: () =>
    apiRequest
      .get('/board/faq/category')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  get_notice_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/board/notice?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  get_notice: (notice_id: number) =>
    apiRequest
      .get(`/board/notice/${notice_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_notice: (data: any) =>
    apiRequest
      .post(`/board/notice`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_notice: (notice_id: number, data: any) =>
    apiRequest
      .put(`/board/notice/${notice_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_qna_list: (query: string, offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/board/qna?${query}&offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_qna: (data: any) =>
    apiRequest
      .post(`/board/qna`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_qna: (q_id: number, data: any) =>
    apiRequest
      .put(`/board/qna/${q_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_qna: (qna_id: number) =>
    apiRequest
      .get(`/board/qna/${qna_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_qna_answer: (qna_id: number) =>
    apiRequest
      .get(`/board/qna/answer/${qna_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_qna_answer: (qna_id: number, data: any) =>
    apiRequest
      .post(`/board/qna/answer?qna_id=${qna_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_qna_answer: (answer_id: number, data: any) =>
    apiRequest
      .put(`/board/qna/answer${answer_id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
