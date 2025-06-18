import { showLogConsole } from '@/utils/common-utils';

export default (accessToken: string): string => {
  try {
    const userInfoJWT = accessToken.split('.')[1];
    const tokenInfo = decodeURIComponent(escape(window.atob(userInfoJWT)));
    return tokenInfo;
  } catch (e) {
    showLogConsole(e);
    showLogConsole('failed decode');
    return '';
  }
};
