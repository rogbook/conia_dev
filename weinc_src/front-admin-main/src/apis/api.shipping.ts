import apiRequest from '@/apis/axios.client';
import type { AddShippingInfo } from 'ShippingInfoModule';

export const shipping = {
  get_shipping_info_list: (query: string) =>
    apiRequest
      .get(`/product/shipping-info?${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  add_shipping_info: (data: { name: string; type: string; pay_type: string; calc_type: string; return_cost: number; change_cost: number; member_id?: number }) =>
    apiRequest
      .post('/product/shipping-info', JSON.stringify(data))
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),
  get_shipping_info: (id: string) =>
    apiRequest
      .get(`/product/shipping-info/${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_shipping_info: (id: string, info: { name?: string; type?: string; pay_type?: string; calc_type?: string; return_cost?: number; change_cost?: number; status?: string }) =>
    apiRequest
      .put(`/product/shipping-info/${id}`, JSON.stringify(info))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_shipping_cost_info: (id: string, cost: AddShippingInfo[]) =>
    apiRequest
      .post(`/product/shipping-info/${id}/cost`, JSON.stringify(cost))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  delete_shipping_cost_info: (id: string) =>
    apiRequest
      .delete(`/product/shipping-info/${id}/cost`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
