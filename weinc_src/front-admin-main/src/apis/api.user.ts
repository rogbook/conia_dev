import apiRequest from '@/apis/axios.client';

export const user = {
  // 로그인
  login: (id: string, pw: string) =>
    apiRequest
      .post(
        '/auth/login',
        JSON.stringify({
          email: id,
          password: pw,
        }),
      )
      .then(function (res) {
        localStorage.setItem('auth', JSON.stringify(res.data));
        return res.data;
      })
      .catch(function (err) {
        return err;
      }),
  //sns 로그인
  sns_login: (type: string, token: string = '') =>
    apiRequest
      .post(
        '/auth/sns_login',
        JSON.stringify({
          type: type,
          token: token,
        }),
      )
      .then(function (res) {
        localStorage.setItem('auth', JSON.stringify(res.data));
        return res.data;
      })
      .catch(function (err) {
        return err;
      }),
  // 로그아웃
  logout: () =>
    apiRequest
      .post('/auth/logout')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 회원 정보 (본인)
  me: () =>
    apiRequest
      .get('/member/me')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 회원 목록
  get_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/member?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // MC 회원 목록
  get_mc_list: (query: string = '', offset: number = 0, limit: number = 20) =>
    apiRequest
      .get(`/member/mc?${query}offset=${offset}&limit=${limit}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 회원 상세
  get_user: (id: string, target: string) =>
    apiRequest
      .get(`/member/${id}?target=${target}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  mod_user: (id: string | null | undefined = null, mod_data: object) =>
    apiRequest
      .put(id === null || undefined ? '/member/me' : `/member/${id}`, JSON.stringify(mod_data))
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  get_class: () =>
    apiRequest
      .get('/member/class')
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  link_class: (id: string | number, class_code: string) =>
    apiRequest
      .post(`/member/class/${class_code}/link?member_id=${id}`)
      .then(res => {
        return res;
      })
      .catch(err => {
        return err;
      }),
  unlink_class: (id: string | number, class_code: string) =>
    apiRequest
      .delete(`/member/class/${class_code}/link?member_id=${id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  link_member: (id: string | number, p_id: number) =>
    apiRequest
      .post(`/member/link?member_id=${id}&parent_id=${p_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  unlink_member: (id: string | number, p_id: number) =>
    apiRequest
      .delete(`/member/link?member_id=${id}&parent_id=${p_id}`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),

  findId: (token_version_id: string) =>
    apiRequest
      .post(`/auth/find-id-cert`, { token_version_id: token_version_id })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  changePw: (token_version_id: string, email_id: string, new_password: string) =>
    apiRequest
      .post(`/auth/password-change-cert`, {
        token_version_id: token_version_id,
        email_id: email_id,
        new_password: new_password,
      })
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
  // 회원 임시비밀번호 발급
  temp_password: (member_id: number) =>
    apiRequest
      .put(`/member/${member_id}/force-change-passwd`)
      .then(res => {
        return res.data;
      })
      .catch(err => {
        return err;
      }),
};
