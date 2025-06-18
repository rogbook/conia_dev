import apiRequest from '@/apis/axios.client';

export const permission = {
  // 권한 목록
  get_list: (query: string = '') =>
    apiRequest
      .get(`/permission?${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  link_permission: (code: string, target: string, query: string = '') =>
    apiRequest
      .post(`/permission/${code}/link?target=${target}&${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  unlink_permission: (code: string, query: string = '') =>
    apiRequest
      .delete(`/permission/${code}/link?${query}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  check_class_code_exist: (code: string) =>
    apiRequest
      .get(`/member/class/exist?code=${code}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  add_class: (code: string, name: string, description: string) =>
    apiRequest
      .post('/member/class', JSON.stringify({ code: code, name: name, description: description }))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  exclude_permission: (code: string, member_id: string, exclude: string) =>
    apiRequest
      .put(`/permission/${code}/${member_id}/exclude?exclude=${exclude}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 메뉴 목록
  get_menu: () =>
    apiRequest
      .get('/menu')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_class_menu: (class_code: string) =>
    apiRequest
      .get(`/menu/${class_code}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  link_menu: (class_code: string, target: number) =>
    apiRequest
      .post(`/menu/${class_code}/link?target=${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  unlink_menu: (class_code: string, menu_id: number) =>
    apiRequest
      .delete(`/menu/${class_code}/link?menu_id=${menu_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
