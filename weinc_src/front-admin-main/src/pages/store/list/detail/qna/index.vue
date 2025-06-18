<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'고객 문의 관리'" />
  <div class="card col-md-8">
    <div class="card-header">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">고객 문의 관리</div>
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
              <th style="width: 34%">제목</th>
              <th>등록일</th>
              <th>작성자</th>
              <th>상태</th>
              <th>상세</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in storeQnaList.datas" :key="item.id">
              <td>{{ item.title }}</td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.customer.name }}</td>
              <td>{{ item.status === 'R' ? '답변대기중' : item.status === 'C' ? '답변완료' : '-' }}</td>
              <td>
                <div v-if="item.status === 'R'">
                  <button type="button" class="btn btn-sm btn-warning" @click.prevent="router.push({ path: `/store/detail/qna`, state: { show: item.id } })">답변하기</button>
                </div>
                <div v-if="item.status === 'C'">
                  <button type="button" class="btn btn-sm btn-success" @click.prevent="router.push({ path: `/store/detail/qna`, state: { show: item.id } })">상세보기</button>
                </div>
              </td>
            </tr>
            <tr v-if="storeQnaList.total === 0">
              <td colspan="5" class="text-center">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="storeQnaList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import type { storeQnaInfoList } from 'StoreQnaInfoMOdule';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showLogConsole } from '@/utils/common-utils';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const router = useRouter();
const storeQnaList = ref({} as storeQnaInfoList);
const storeCode = history.state.code.toString();
const customer_id = ref(0);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(storeQnaList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreQnaList();
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  getStoreQnaList();
});

const getStoreQnaList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  apis.store.get_store_qna_list(customer_id.value, storeCode, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      storeQnaList.value.datas = res.datas;
      storeQnaList.value.total = res.total;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreQnaList(false);
  window.scrollTo({ top: 100, left: 0 });
};
</script>

<style scoped></style>
