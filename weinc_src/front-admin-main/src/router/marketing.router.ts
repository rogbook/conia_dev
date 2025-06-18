import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/marketing',
    name: 'marketing',
    children: [
      {
        path: 'coupon',
        name: 'couponList',
        component: () => import('@/pages/marketing/coupon/CouponList.vue'),
      },
      {
        path: 'coupon/reg',
        name: 'couponReg',
        component: () => import('@/pages/marketing/coupon/reg/CouponReg.vue'),
      },
      {
        path: 'coupon/detail',
        name: 'couponDetail',
        component: () => import('@/pages/marketing/coupon/detail/CouponDetail.vue'),
      },
      {
        path: 'acoupon',
        name: 'autoCouponList',
        component: () => import('@/pages/marketing/auto_coupon/AutoCouponList.vue'),
      },
      {
        path: 'message',
        name: 'messageList',
        component: () => import('@/pages/marketing/messaging/MessagingList.vue'),
      },
    ],
    redirect: { name: 'couponList' },
  },
];

export default routes;
