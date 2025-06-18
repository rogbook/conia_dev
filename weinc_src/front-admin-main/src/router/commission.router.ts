import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/commission',
    name: 'commission',
    children: [
      {
        path: 'partner',
        name: 'partnerCommission',
        component: () => import('@/pages/product/commission/member/PartnerCommission.vue'),
      },
      {
        path: 'intermediate',
        name: 'intermediCommission',
        component: () => import('@/pages/product/commission/member/IntermediCommission.vue'),
      },
      {
        path: 'shipping',
        name: 'paShipCommission',
        component: () => import('@/pages/product/commission/ship/ShipCommission.vue'),
      },
      {
        path: 'cmc',
        name: 'coniaCommission',
        component: () => import('@/pages/product/commission/CMCommission.vue'),
      },
      {
        path: 'member',
        name: 'memberList',
        component: () => import('@/pages/product/commission/member/MemberSelect.vue'),
      },
      {
        path: 'ship',
        name: 'shipMemberPaList',
        component: () => import('@/pages/product/commission/ship/MemberSelectPA.vue'),
      },
    ],
    redirect: { name: 'partnerCommission' },
  },
];

export default routes;
