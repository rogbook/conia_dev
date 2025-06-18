import type { RouteRecordRaw } from 'vue-router';
import { ROUTE_PATH } from '@/router/route.constant';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/setting',
    name: 'setting',
    children: [
      {
        path: 'shipping',
        name: 'shippingList',
        component: () => import('@/pages/settings/shipping/list/ShippingGroupList.vue'),
      },
      {
        path: 'shipping/add',
        name: 'shippingAdd',
        component: () => import('@/pages/settings/shipping/list/detail/ShippingGroupDetail.vue'),
      },
      {
        path: 'shipping/detail',
        name: 'shippingDetail',
        component: () => import('@/pages/settings/shipping/list/detail/ShippingGroupDetail.vue'),
      },
      {
        path: 'shipping/detail/area',
        name: 'shippingDetailArea',
        component: () => import('@/pages/settings/shipping/list/detail/area/ShippingAreaInfo.vue'),
      },
      {
        path: 'product/option',
        name: 'productOptionList',
        component: () => import('@/pages/settings/product/options/list/SettingProductOptionList.vue'),
      },
      {
        path: 'product/option/detail',
        name: 'productOptionDetail',
        component: () => import('@/pages/settings/product/options/list/detail/SettingProductOptionDetail.vue'),
      },
      {
        path: 'product/common',
        name: 'productCommonList',
        component: () => import('@/pages/settings/product/common/list/ProdCommonInfoList.vue'),
      },
      {
        path: 'product/common/reg',
        name: 'productCommonReg',
        component: () => import('@/pages/settings/product/common/list/detail/ProdCommonInfoDetail.vue'),
      },
      {
        path: 'product/common/detail',
        name: 'productCommonDetail',
        component: () => import('@/pages/settings/product/common/list/detail/ProdCommonInfoDetail.vue'),
      },
      {
        path: 'product/badge',
        name: 'productBadgeList',
        component: () => import('@/pages/settings/product/badge/BadgeList.vue'),
      },
      {
        path: 'community/notice',
        name: 'noticeMng',
        component: () => import('@/pages/settings/community/notice/NoticeList.vue'),
      },
      {
        path: 'community/notice/reg',
        name: 'noticeMngReg',
        component: () => import('@/pages/settings/community/notice/detail/NoticeDetail.vue'),
      },
      {
        path: 'community/notice/detail',
        name: 'noticeMngDetail',
        component: () => import('@/pages/settings/community/notice/detail/NoticeDetail.vue'),
      },
      {
        path: 'community/faq',
        name: 'faqMng',
        component: () => import('@/pages/settings/community/faq/FaqList.vue'),
      },
      {
        path: 'community/faq/reg',
        name: 'faqMngReg',
        component: () => import('@/pages/settings/community/faq/detail/FaqDetail.vue'),
      },
      {
        path: 'community/faq/detail',
        name: 'faqMngDetail',
        component: () => import('@/pages/settings/community/faq/detail/FaqDetail.vue'),
      },
      {
        path: 'community/qna',
        name: 'qnaMng',
        component: () => import('@/pages/settings/community/qna/QnaList.vue'),
      },
      {
        path: 'community/qna/detail',
        name: 'qnaMngDetail',
        component: () => import('@/pages/settings/community/qna/detail/QnaDetail.vue'),
      },
      {
        path: 'default',
        name: 'setDefaultValue',
        component: () => import('@/pages/settings/master/SetDefaultValue.vue'),
      },
      {
        path: 'sv',
        name: 'setSettingValue',
        component: () => import('@/pages/settings/master/SetSettingValue.vue'),
      },
      {
        path: 'ov',
        name: 'setOptionValue',
        component: () => import('@/pages/settings/master/SetOptionValue.vue'),
      },
    ],
    redirect: { path: ROUTE_PATH.HOME },
  },
];
export default routes;
