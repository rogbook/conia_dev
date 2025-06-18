import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/order',
    name: 'order',
    children: [
      {
        path: 'list',
        name: 'orderList',
        component: () => import('@/pages/order/list/OrderList.vue'),
      },
      {
        path: 'detail',
        name: 'orderDetail',
        component: () => import('@/pages/order/list/detail/OrderDetail.vue'),
      },
      {
        path: 'exre/list',
        name: 'exreList',
        component: () => import('@/pages/order/exre/OrderExReList.vue'),
      },
      {
        path: 'exre/detail',
        name: 'exreDetail',
        component: () => import('@/pages/order/exre/detail/OrderExReDetail.vue'),
      },
      {
        path: 'receipt/list',
        name: 'receiptList',
        component: () => import('@/pages/order/receipt/list/ReceiptList.vue'),
      },
      {
        path: 'sales',
        name: 'salestList',
        component: () => import('@/pages/order/sales/salesList.vue'),
      },
      {
        path: 'offlist',
        name: 'orderOffline',
        component: () => import('@/pages/order/offline/OrderOffline.vue'),
      },
      {
        path: 'refund',
        name: 'refundList',
        component: () => import('@/pages/order/refund/RefundList.vue'),
      },
    ],
    redirect: { name: 'orderList' },
  },
];
export default routes;
