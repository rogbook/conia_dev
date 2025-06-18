import type { RouteRecordRaw } from 'vue-router';
import { useProductModeStore } from '@/stores/product';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/product',
    name: 'product',
    children: [
      {
        path: 'list',
        name: 'productList',
        component: () => import('@/pages/product/list/ProductList.vue'),
      },
      {
        path: 'reg',
        name: 'productReg',
        component: () => import('@/pages/product/register/ProductReg.vue'),
      },
      {
        path: 'detail',
        name: 'productDetail',
        component: () => import('@/pages/product/list/detail/ProductDetail.vue'),
      },
      {
        path: 'category',
        name: 'productCategory',
        component: () => import('@/pages/product/category/CategoryMng.vue'),
      },
      {
        path: 'brand',
        name: 'productBrand',
        component: () => import('@/pages/product/brand/BrandMng.vue'),
      },
      {
        path: 'qna',
        name: 'productQna',
        component: () => import('@/pages/product/qna/index.vue'),
      },
      {
        path: 'qna/detail',
        name: 'productQnaShow',
        component: () => import('@/pages/product/qna/show.vue'),
      },
      {
        path: 'catalog',
        name: 'productCatalog',
        children: [
          {
            path: '',
            name: 'productCatalogMain',
            component: () => import('@/pages/product/catalog/list/catalogue.vue'),
          },
          {
            path: 'detail',
            name: 'productCatalogDetail',
            component: () => import('@/pages/product/catalog/list/detail/CatalogDetail.vue'),
          },
          {
            path: 'edit',
            name: 'productCatalogEdit',
            component: () => import('@/pages/product/catalog/list/product/CatalogProductMng.vue'),
          },
          {
            path: 'view',
            name: 'productCatalogView',
            component: () => import('@/pages/product/catalog/list/link/CatalogLinkMng.vue'),
          },
        ],
      },
      {
        path: 'req',
        name: 'productRequest',
        component: () => import('@/pages/product/request/req/ProdReqInfo.vue'),
      },
      {
        path: 'req/detail',
        name: 'productReqDetail',
        component: () => import('@/pages/product/request/list/detail/ProdReqDetail.vue'),
      },
      {
        path: 'req/list',
        name: 'productReqList',
        component: () => import('@/pages/product/request/list/ProdReqList.vue'),
      },
      {
        path: 'stock/list',
        name: 'productStockList',
        component: () => import('@/pages/product/stock/ProdStockList.vue'),
      },
      {
        path: 'review',
        name: 'productReview',
        component: () => import('@/pages/product/review/ProdReviewList.vue'),
      },
    ],
    redirect: { name: 'productList' },
  },
];

export default routes;
