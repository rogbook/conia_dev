import type { RouteRecordRaw } from 'vue-router';
import { ROUTE_PATH } from '@/router/route.constant';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/permission',
    name: 'permission',
    children: [
      {
        path: 'type',
        name: 'permissionType',
        component: () => import('@/pages/permission/type/TypePermission.vue'),
      },
      {
        path: 'type/menu',
        name: 'permissionTypeMenu',
        component: () => import('@/pages/permission/menu/TypeMenu.vue'),
      },
      {
        path: 'type/detail',
        name: 'permissionTypeDetail',
        component: () => import('@/pages/permission/type/detail/TypePermissionDetail.vue'),
      },
      {
        path: 'member/list',
        name: 'permissionMemberList',
        component: () => import('@/pages/permission/member/MemberPermission.vue'),
      },
      {
        path: 'member/detail',
        name: 'permissionMemberDetail',
        component: () => import('@/pages/permission/member/detail/MemberPermissionDetail.vue'),
      },
    ],
    redirect: { path: ROUTE_PATH.HOME },
  },
];
export default routes;
