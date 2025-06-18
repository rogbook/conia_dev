import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/oauth',
    name: 'oauth',
    children: [
      {
        path: 'kakao/connect',
        name: 'kakaoConnectCallback',
        component: () => import('@/pages/oauth/kakao/ConnectCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'kakao/login',
        name: 'kakaoLoginCallback',
        component: () => import('@/pages/oauth/kakao/LoginCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'google/connect',
        name: 'googleConnectCallback',
        component: () => import('@/pages/oauth/google/ConnectCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'google/login',
        name: 'googleLoginCallback',
        component: () => import('@/pages/oauth/google/LoginCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'payco/connect',
        name: 'paycoConnectCallback',
        component: () => import('@/pages/oauth/payco/ConnectCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'payco/login',
        name: 'paycoLoginCallback',
        component: () => import('@/pages/oauth/payco/LoginCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'naver/connect',
        name: 'naverConnectCallback',
        component: () => import('@/pages/oauth/naver/ConnectCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
      {
        path: 'naver/login',
        name: 'naverLoginCallback',
        component: () => import('@/pages/oauth/naver/LoginCallback.vue'),
        meta: { layout: 'nonelayout' },
      },
    ],
    // redirect: { name: 'callback' },
  },
];

export default routes;
