<template>
  <PageNavigator :before_link="[]" :current="'상품문의관리'" />
  <div class="card col-md-10">
    <div class="card-header py-3">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">상품문의내역</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto"></div>
        <div class="col-auto">
          <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-align-middle border card-table table-vertical-border-striped table-bordered table-nowrap">
          <thead class="thead-light">
            <tr class="text-center">
              <th style="width: 30%">제목</th>
              <th style="width: 30%">상품</th>
              <th>등록일</th>
              <th>상태</th>
              <th>상세</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in prodQnaList.datas" :key="item.id">
              <td>{{ item.title }}</td>
              <td class="text-center text-wrap p-0">
                <div class="card-body">
                  <div class="row align-items-center">
                    <div class="col-auto">
                      <img :src="item.product.photos[0].uri" style="width: 50px" />
                    </div>
                    <div class="col text-start">
                      <div class="mb-1">
                        <b>{{ item.product.name }}</b>
                      </div>
                      <div class="" style="font-size: 0.8rem">
                        (상품코드 : &nbsp;<RouterLink :to="{ path: '/product/detail', state: { id: item.product.id } }">{{ item.product.code }} </RouterLink>)
                      </div>
                    </div>
                  </div>
                </div>
              </td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.status === 'R' ? '답변대기중' : item.status === 'C' ? '답변완료' : '-' }}</td>
              <td>
                <div v-if="item.status === 'R'">
                  <button type="button" class="btn btn-sm btn-warning" @click.prevent="router.push({ path: '/product/qna/detail', state: { id: item.id } })">답변하기</button>
                </div>
                <div v-if="item.status === 'C'">
                  <button type="button" class="btn btn-sm btn-success" @click.prevent="router.push({ path: '/product/qna/detail', state: { id: item.id } })">상세보기</button>
                </div>
              </td>
            </tr>
            <tr v-if="prodQnaList.total === 0">
              <td colspan="5" class="text-center">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area mt-2" v-if="prodQnaList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, showLogConsole, dateTimeFormatConverter, getUserClassStr } from '@/utils/common-utils';
import apis from '@/apis';
import { useUserStore } from '@/stores/user';
import { AxiosError } from 'axios';
import type { ProdQnaInfoList } from 'ProdQnaInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const router = useRouter();

const paId = ref(0);
const prodQnaList = ref({} as ProdQnaInfoList);
const customer_id = ref(0);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(prodQnaList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getProdQnaList();
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  if (getUserClassStr.value.includes('PA')) {
    paId.value = useUserStore().user.id as number;
  }
  getProdQnaList();
});

const getProdQnaList = async (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  const product_id = 0;

  apis.product.getProdQnaList(customer_id.value, product_id, paId.value, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      prodQnaList.value.datas = res.datas;
      prodQnaList.value.total = res.total;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProdQnaList(false);
  window.scrollTo({ top: 100, left: 0 });
};
</script>
