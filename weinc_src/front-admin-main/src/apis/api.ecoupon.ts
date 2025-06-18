import apiRequest from '@/apis/axios.client';
export const ecoupon = {
  //E쿠폰 재발송
  resend_ecoupon: (order_product_id: number) =>
    apiRequest
      .get(`/ecoupon/resend/${order_product_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
