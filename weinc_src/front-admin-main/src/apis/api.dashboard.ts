import apiRequest from '@/apis/axios.client';

export const dashboard = {
  get_dashboard_data: () =>
    apiRequest
      .get('/dashboard')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
