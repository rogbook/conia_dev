import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/settlement',
    name: 'settlement',
    children: [
      {
        path: 'list',
        name: 'settlementList',
        component: () => import('@/pages/settlement/member/SettlementList.vue'),
      },
      {
        path: 'member',
        name: 'settlementMember',
        component: () => import('@/pages/settlement/member/MemberSelect.vue'),
      },
      {
        path: 'ship/list',
        name: 'settlementShipList',
        component: () => import('@/pages/settlement/ship/SettlementShipList.vue'),
      },
      {
        path: 'ship',
        name: 'settlementShip',
        component: () => import('@/pages/settlement/ship/MemberSelectPA.vue'),
      },
      {
        path: 'conia',
        name: 'settlementConia',
        component: () => import('@/pages/settlement/conia/SettlementConia.vue'),
      },
      {
        path: 'conia/ship',
        name: 'settlementShipConia',
        component: () => import('@/pages/settlement/conia/SettlementShipConia.vue'),
      },
      {
        path: 'pg',
        name: 'settlementPG',
        component: () => import('@/pages/settlement/pg/SettlementPG.vue'),
      },
      {
        path: 'pg/ship',
        name: 'settlementPgShip',
        component: () => import('@/pages/settlement/pg/SettlementPgShip.vue'),
      },
      {
        path: 'excel',
        name: 'settlementExcel',
        component: () => import('@/pages/settlement/excel/SettlementReqExcel.vue'),
      },
    ],
    redirect: { name: 'calculateList' },
  },
];

export default routes;
