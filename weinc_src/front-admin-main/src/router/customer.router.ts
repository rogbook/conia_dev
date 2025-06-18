import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/customer',
    name: 'customer',
    children: [
      { name: 'customerDetail', path: 'detail', component: () => import('@/pages/user/customer/detail/CustomerDetail.vue') },
      { name: 'customerList', path: '', component: () => import('@/pages/user/customer/CustomerList.vue') },
    ],
    redirect: { name: 'customerList' },
  },
];

export default routes;
