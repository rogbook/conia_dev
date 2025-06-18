import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/store',
    name: 'store',
    children: [
      {
        path: 'list',
        name: 'storeList',
        component: () => import('@/pages/store/list/StoreList.vue'),
      },
      {
        path: 'qna',
        name: 'storeQna',
        component: () => import('@/pages/store/qna/StoreQna.vue'),
      },
      {
        path: 'reg',
        name: 'storeReg',
        component: () => import('@/pages/store/list/detail/StoreDetail.vue'),
      },
      {
        path: 'detail',
        name: 'storeDetail',
        component: () => import('@/pages/store/list/detail/StoreDetail.vue'),
      },
      {
        path: 'detail/exmenu',
        name: 'storeExcludeMenu',
        component: () => import('@/pages/store/list/detail/menu/SetExcludeMenu.vue'),
      },
      {
        path: 'detail/product',
        name: 'storeDetailProduct',
        component: () => import('@/pages/store/list/detail/product/StoreProdMng.vue'),
      },
      {
        path: 'detail/product/memo',
        name: 'storeDetailProdMemo',
        component: () => import('@/pages/store/list/detail/product/memo/StoreProdMemo.vue'),
      },
      {
        path: 'detail/layout',
        name: 'storeDetailLayout',
        component: () => import('@/pages/store/list/detail/layout/SetStoreHomeLayout.vue'),
      },
      {
        path: 'detail/popup',
        name: 'storeDetailPopup',
        component: () => import('@/pages/store/list/detail/popup/StoreEventList.vue'),
      },
      {
        path: 'detail/boardgroup',
        name: 'storeDetailBoardGroup',
        component: () => import('@/pages/store/list/detail/board_group/BoardGroupList.vue'),
      },
      {
        path: 'detail/board',
        name: 'storeDetailBoardList',
        component: () => import('@/pages/store/list/detail/board_group/board/BoardList.vue'),
      },
      {
        path: 'detail/board/detail',
        name: 'storeDetailBoardDetail',
        component: () => import('@/pages/store/list/detail/board_group/board/detail/BoardDetail.vue'),
      },
      {
        path: 'detail/board/detail/comment',
        name: 'storeDetailBoardDetailComment',
        component: () => import('@/pages/store/list/detail/board_group/board/detail/BoardComment.vue'),
      },
      {
        path: 'detail/theme',
        name: 'storeDetailTheme',
        component: () => import('@/pages/store/list/detail/theme/StoreThemeMng.vue'),
      },
      {
        path: 'detail/member',
        name: 'storeDetailMember',
        component: () => import('@/pages/store/list/detail/member/StoreMemberList.vue'),
      },
      {
        path: 'detail/qna/list',
        name: 'storeDetailQna',
        component: () => import('@/pages/store/list/detail/qna/index.vue'),
      },
      {
        path: 'detail/qna',
        name: 'storeDetailQnaShow',
        component: () => import('@/pages/store/list/detail/qna/show.vue'),
      },
    ],
    redirect: { name: 'storeList' },
  },
];

export default routes;
