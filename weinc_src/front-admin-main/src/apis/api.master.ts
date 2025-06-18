import apiRequest from '@/apis/axios.client';
import type { OptionValue, SettingValue } from 'SettingValueModule';

export const master = {
  get_setting_value_list: (query: string = '') =>
    apiRequest
      .get(`/value/settings${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  add_setting_value: (data: SettingValue) =>
    apiRequest
      .post(`/value/setting`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_setting_value: (id: number, modData: SettingValue) =>
    apiRequest
      .put(`/value/setting/${id}`, JSON.stringify(modData))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  get_option_value_list: (query: string = '') =>
    apiRequest
      .get(`/value/option${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_option_value: (data: OptionValue) =>
    apiRequest
      .post(`/value/option`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_option_value: (id: number, data: SettingValue) =>
    apiRequest
      .put(`/value/option/${id}`, JSON.stringify(data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
