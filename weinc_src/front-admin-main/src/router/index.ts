import type { NavigationGuardNext, RouteLocationNormalized, RouteRecordRaw } from 'vue-router';
import { createRouter, createWebHistory, isNavigationFailure, NavigationFailureType } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useErrorStore } from '@/stores/error';
import { useUserStore } from '@/stores/user';
import productRouter from '@/router/product.router';
import userRouter from '@/router/user.router';
import customerRouter from '@/router/customer.router';
import orderRouter from '@/router/order.router';
import settingRouter from '@/router/setting.router';
import permissionRouter from '@/router/permission.router';
import storeRouter from '@/router/store.router';
import commissionRouter from '@/router/commission.router';
import communityRouter from '@/router/community.router';
import calculateRouter from '@/router/settlement.router';
import marketingRouter from '@/router/marketing.router';
import oauthRouter from '@/router/oauth.router';
import { ROUTE_PATH } from '@/router/route.constant';
import { STEP } from '@/models/users/join';
import { showLogConsole } from '@/utils/common-utils';
import { useModalStore } from '@/stores/modal';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: { path: ROUTE_PATH.HOME },
  },
  {
    path: ROUTE_PATH.JOIN,
    name: 'join',
    component: () => import('@/layouts/joinLayout.vue'),
    props: to => {
      showLogConsole(`join route props to: ${to}`);
      return to.meta.step;
    },
    meta: { layout: 'noneLayout' },
  },
  {
    path: ROUTE_PATH.LOGIN,
    name: 'login',
    component: () => import('@/pages/Login.vue'),
    meta: { layout: 'loginLayout' },
  },
  {
    path: ROUTE_PATH.HOME,
    name: 'home',
    component: () => import('@/pages/dashboard/dashboard.vue'),
  },
  ...productRouter,
  ...userRouter,
  ...customerRouter,
  ...orderRouter,
  ...settingRouter,
  ...permissionRouter,
  ...storeRouter,
  ...commissionRouter,
  ...communityRouter,
  ...calculateRouter,
  ...marketingRouter,
  ...marketingRouter,
  ...oauthRouter,
  {
    path: ROUTE_PATH.ERROR,
    name: 'error',
    props: true,
    component: () => import('@/pages/error/error.vue'),
    meta: { layout: 'noneLayout' },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: { path: ROUTE_PATH.ERROR },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

//전역 네비게이션 가드
router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  if (useModalStore().getModalIdArr.length !== 0) useModalStore().removeModalId();

  window.scrollTo({ top: 0, left: 0 });
  // user token이 localstorage에 존재한다.
  // https://github.com/vuejs/router/blob/main/packages/router/CHANGELOG.md#414-2022-08-22
  // props로 데이터 넘길때 그냥 pinia를 쓰거나 params로 넘기라는 내용
  if (from.path === to.path) {
    return;
  }
  if (useErrorStore().hasError) {
    to.path = ROUTE_PATH.ERROR;
    showLogConsole('hasError');
    next();
    return;
  }
  showLogConsole(`${to.path}`);
  const authInfo = localStorage.getItem('auth');
  const authStore = useAuthStore();
  if (authInfo) {
    const { access_token, refresh_token } = JSON.parse(authInfo);
    authStore.updateAuthInfo({ access_token, refresh_token });
  }

  // pinia store에 user정보를 성공적으로 저장했다.
  switch (to.path) {
    case '/login':
      authStore.isLoggedIn ? next(ROUTE_PATH.HOME) : next();
      showLogConsole('Router beforeEach path: REQ_LOGIN', 'info');
      return;
    case '/join':
      if (authStore.isLoggedIn) {
        if (useUserStore().user.status == 'R') {
          to.meta.step = STEP.ADMIN_INFO;
          next();
        } else {
          next(ROUTE_PATH.HOME);
        }
        showLogConsole('Router beforeEach path: LOGIN', 'info');
      } else {
        showLogConsole('Router beforeEach path: NO_LOGIN', 'info');
        next();
      }
      return;
    case '/user/mobileCertResult':
    case '/mobileCertResult':
    case '/user/find':
    case '/user/find/account':
    case '/user/find/password':
    case '/user/wait':

    case '/oauth/kakao/login':
    case '/oauth/google/login':
    case '/oauth/payco/login':
    case '/oauth/naver/login':
      next();
      return;
    default:
      if (authStore.isLoggedIn) {
        if (useUserStore().user.status == 'R') {
          //@ts-ignore
          if (useUserStore().user.organization.my_company) {
            next('/user/wait');
          } else {
            to.meta.step = STEP.ADMIN_INFO;
            next(ROUTE_PATH.JOIN);
          }
        } else {
          next();
        }
      } else {
        next(ROUTE_PATH.LOGIN);
      }
      showLogConsole('Router beforeEach path: DEFAULT_PATH', 'info');
      return;
  }
});

router.afterEach((to, from, failure) => {
  showLogConsole(`'after each:' ${from},  ${to}`);
  // Any kind of navigation failure
  if (isNavigationFailure(failure)) {
    // ...
    showLogConsole(`Any kind of navigation failure : ${failure}`, 'err');
  }
  // Only duplicated navigations
  if (isNavigationFailure(failure, NavigationFailureType.duplicated)) {
    // ...
    showLogConsole(`Only duplicated navigations : ${failure}`, 'err');
  }
  // Aborted or canceled navigations
  if (isNavigationFailure(failure, NavigationFailureType.aborted | NavigationFailureType.cancelled)) {
    // ...
    showLogConsole(`Aborted or canceled navigations : ${failure}`, 'err');
  }
});

export default router;
