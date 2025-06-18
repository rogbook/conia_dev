import type { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/community',
    name: 'community',
    children: [
      {
        path: 'faq',
        name: 'faqList',
        component: () => import('@/pages/community/faq/FaqList.vue'),
      },
      {
        path: 'notice',
        name: 'noticeList',
        component: () => import('@/pages/community/notice/NoticeList.vue'),
      },
      {
        path: 'notice/detail',
        name: 'noticeDetail',
        component: () => import('@/pages/community/notice/detail/NoticeDetail.vue'),
      },
      {
        path: 'qna',
        name: 'qnaList',
        component: () => import('@/pages/community/qna/QnaList.vue'),
      },
      {
        path: 'qna/reg',
        name: 'qnaReg',
        component: () => import('@/pages/community/qna/detail/QnaDetail.vue'),
      },
      {
        path: 'qna/detail',
        name: 'qnaDetail',
        component: () => import('@/pages/community/qna/detail/QnaDetail.vue'),
      },
    ],
    redirect: { name: 'faqList' },
  },
];

export default routes;
