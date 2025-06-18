<template>
  <PageNavigator :before_link="[]" :current="'1:1 문의'" />
  <div class="card col-lg-8">
    <div class="card-header py-2">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">1:1 문의 내역</div>
        </div>
        <div class="col text-end">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="router.push('/community/qna/reg')">1:1 문의하기</button>
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
              <th>상태</th>
              <th>상세</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in qnaList.datas" :key="item.id">
              <td>{{ item.title }}</td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.status === 'R' ? '답변대기중' : item.status === 'C' ? '답변완료' : '-' }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/community/qna/detail`, state: { id: item.id } })">상세</button>
              </td>
            </tr>
            <tr v-if="qnaList.total === 0">
              <td colspan="4" class="text-center">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-footer-area" v-if="qnaList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import type { QnaInfoList } from 'BoardInfoModule';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apis from '@/apis';
import { apiResponseCheck, dateTimeFormatConverter, showLogConsole } from '@/utils/common-utils';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const router = useRouter();
const route = useRoute();
const qnaList = ref({} as QnaInfoList);

const q_member_id = useUserStore().user.id as number;

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(qnaList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getQnaList();
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string = '') => {
  searchInfo.value = `${query}page_no=${page_no.value}`;
  useSearchStore().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  if (useSearchStore().getSearchInfo) {
    const paramsArray = JSON.parse(JSON.stringify(useSearchStore().getSearchInfo)).split('&');

    for (const param of paramsArray) {
      const [key, value] = param.split('=');

      switch (key) {
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        default:
          break;
      }
    }
  }
};
/** */

const getQnaList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  setSearchInfo();
  apis.community.get_qna_list(`q_member_id=${q_member_id}`, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      qnaList.value.datas = res.datas;
      qnaList.value.total = res.total;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getQnaList(false);
  window.scrollTo({ top: 100, left: 0 });
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  getSearchInfo();
  getQnaList();
});
</script>

<style scoped></style>
