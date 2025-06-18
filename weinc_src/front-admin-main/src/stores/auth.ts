import { acceptHMRUpdate, defineStore } from 'pinia';
// @ts-ignore
import { ref } from 'vue';
import type { Ref } from 'vue';
import { useUserStore } from '@/stores/user';
import tokenParser from '@/utils/tokenParser';
import { useErrorStore } from '@/stores/error';
import { showAlert, showLogConsole } from '@/utils/common-utils';
import { useCommonStore } from '@/stores/common';
import apis from '@/apis';
import { useSearchStore } from '@/stores/search';

export interface Auth {
  access_token: string;
  refresh_token: string;
}

interface IAuthState {
  auth: Ref<{ access_token: string; refresh_token: string }>;
  store_code: string;
}

export const useAuthStore = defineStore('AuthStore', {
  state: (): IAuthState => ({
    auth: ref({
      access_token: '', // jwt access_token
      refresh_token: '', // jwt refresh_token
    }),
    store_code: '',
  }),
  getters: {
    //..
    isLoggedIn: state => !!state.auth.access_token,
    accessToken: state => state.auth.access_token,
    refreshToken: state => state.auth.refresh_token,
  },
  actions: {
    // 사용자 로그인시 jwt 값 갱신
    async login(access_token: string, refresh_token: string) {
      const authInfo = {
        access_token: access_token,
        refresh_token: refresh_token,
      };
      this.updateAuthInfo(authInfo);
      await useCommonStore().setLogisticsKey(await apis.common.getSettingValueOne('sweet_tracker_api_key'));
    },
    // 사용자 로그아웃시 jwt 값 초기화
    async logout(redirectLogin = true) {
      localStorage.removeItem('auth');
      localStorage.removeItem('CommonStore');
      useSearchStore().$reset();
      this.updateAuthInfo({
        access_token: '',
        refresh_token: '',
      });
      if (redirectLogin) this.router.push('/login');
    },
    updateAuthInfo(authInfo: Auth) {
      this.auth = authInfo;
      this.storeUserInfo();
    },
    storeUserInfo() {
      if (this.auth.access_token) {
        const unpackedToken = tokenParser(this.auth.access_token);
        if (unpackedToken === '') {
          showAlert('적절하지 않은 회원정보 입니다.', 'error');
          this.logout();
        } else {
          useUserStore().storeUser(unpackedToken);
        }
      } else {
        useUserStore().deleteUser();
      }
    },
    getStoreCode() {
      try {
        const userInfoJWT = this.auth.access_token.split('.')[1];
        const tokenInfo = decodeURIComponent(escape(window.atob(userInfoJWT)));

        const tokenObject = JSON.parse(tokenInfo.toString());
        // 추후 권한이 필요할떄
        // const scope = tokenObject.scopes;
        // for (const key of Object.keys(scope)) {
        //   console.log(`Scope is  ${key} : ${scope[key]}`);
        // }
        // 조직정보
        const organization = tokenObject.organization;
        if (!organization.my_company) {
          return '';
        } else {
          // 컴퍼니가 있을 경우 코드들을 출력
          return `${organization.my_company}`;
        }
      } catch (e) {
        showLogConsole('middleware token error');
        showLogConsole(e);
        return '';
      }
    },
  },
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot));
}
