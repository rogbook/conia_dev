import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/user',
    name: 'user',
    children: [
      { name: 'userMyinfo', path: 'myinfo', component: () => import('@/pages/user/detail/UserDetail.vue') },
      { name: 'userDetail', path: 'detail', component: () => import('@/pages/user/detail/UserDetail.vue') },
      { name: 'userList', path: 'list', component: () => import('@/pages/user/list/UserList.vue') },
      { name: 'mobileCertResult', path: 'mobileCertResult', component: () => import('@/pages/user/mobileCertResult.vue') },
      { name: 'hierarchyList', path: 'hierarchy', component: () => import('@/pages/user/hierarchy/HierarchyList.vue') },

      { name: 'userFind', path: 'find', component: () => import('@/pages/user/find/index.vue'), meta: { layout: 'noneLayout' } },
      { name: 'userFindAccount', path: 'find/account', component: () => import('@/pages/user/find/account.vue'), meta: { layout: 'noneLayout' } },
      { name: 'userFindPassword', path: 'find/password', component: () => import('@/pages/user/find/password.vue'), meta: { layout: 'noneLayout' } },
      { name: 'userWait', path: 'wait', component: () => import('@/pages/user/wait/index.vue'), meta: { layout: 'noneLayout' } },
    ],
    redirect: { name: 'userDetail' },
  },
];

export default routes;
