import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { showAlert, showLogConsole } from '@/utils/common-utils';
import { useLoadingStore } from '@/stores/loading';

export const BASE_URL = import.meta.env.VITE_API_HOST;
const REFRESH_URL = '/auth/refresh-token';
const LOGIN_URL = '/auth/login';

const apiRequest = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
});

const getRefreshToken = async (): Promise<string | void> => {
  try {
    const access_token = await apiRequest.get(REFRESH_URL).then(res => {
      return res.data.access_token;
    });
    localStorage.setItem('auth', JSON.stringify({ access_token: access_token, refresh_token: useAuthStore().refreshToken }));
    useAuthStore().updateAuthInfo({
      access_token: access_token,
      refresh_token: useAuthStore().refreshToken,
    });
    return access_token;
  } catch (e) {
    return;
  }
};

// jwt check interceptor
apiRequest.interceptors.request.use(
  config => {
    useLoadingStore().pushSize();
    useLoadingStore().updateIsLoading(true);

    let token: string | null = null;

    if (config.url === REFRESH_URL) {
      token = useAuthStore().refreshToken;
    } else {
      token = useAuthStore().accessToken;
    }

    if (token !== '') {
      // @ts-ignore
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  },
);

// jwt token refresh interceptor
apiRequest.interceptors.response.use(
  res => {
    useLoadingStore().popSize();
    if (useLoadingStore().getSize === 0) {
      useLoadingStore().updateIsLoading(false);
    }
    return res;
  },
  async err => {
    useLoadingStore().popSize();
    if (useLoadingStore().getSize === 0) {
      useLoadingStore().updateIsLoading(false);
    }
    const { config, response } = err;
    showLogConsole(`response interceptor config url : ${config.url}`);
    showLogConsole(`response interceptor status : ${response?.status}`);

    if (err.code === 'ECONNABORTED' || err.response?.status === 408) {
      return Promise.reject(err);
    }

    if (config.url === REFRESH_URL || config.url === LOGIN_URL || response.status !== 401 || config.sent) {
      return Promise.reject(err);
    }

    config.sent = true;
    const accessToken = await getRefreshToken();
    showLogConsole(accessToken);
    if (accessToken) {
      showLogConsole('갱신 성공 및 API 재요청');
      return apiRequest(config);
    } else {
      showAlert('로그인 정보가 만료되었습니다.<br/>다시 로그인해주세요.', 'error');
      await useAuthStore().logout();
    }
  },
);

export default apiRequest;
