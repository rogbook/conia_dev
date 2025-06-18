<template>
  <PageNavigator :before_link="[]" :current="'상점 관리'" />
  <div class="card">
    <div class="card-header py-2">
      <div class="row justify-content-between align-items-center">
        <div class="form-control-borderless h2 col-auto mb-0">상점 관리</div>
        <div class="col-auto">
          <button
            type="button"
            class="btn btn-sm btn-warning"
            @click.prevent="
              useSearchStore().$reset();
              router.push(`/store/reg`);
            ">
            상점 등록
          </button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-md-1 col-form-label">검색</label>
        <div class="col-md-2 mb-1">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>

        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getStoreList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStoreList">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mStoreList.total > 0">총 : {{ mStoreList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 20%">상점명</th>
          <th style="width: 20%">상점코드</th>
          <th>운영자</th>
          <th>운영상태</th>
          <th>설정</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(s, i) in mStoreList.datas" :key="JSON.stringify(s)">
          <td>
            {{ s.title }}
          </td>
          <td>{{ s.code }}</td>
          <td>{{ s.member?.name }} ({{ s.member?.email }})</td>
          <td>{{ s.status === 'Y' ? '운영중' : s.status === 'R' ? '오픈준비중' : s.status === 'N' ? '미운영' : '설정변경중' }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/store/detail`, state: { code: s.code } })">상세보기</button>
          </td>
        </tr>
        <tr class="text-center" v-if="mStoreList.total === 0">
          <td colspan="5">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mStoreList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { StoreList } from 'StoreListInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import Pagination from '@/components/comm/Pagination.vue';
import { useRouter, useRoute } from 'vue-router';
import { apiResponseCheck, getUserClassStr, showAlert, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const router = useRouter();
const route = useRoute();
const mStoreList = ref({} as StoreList);

const selDetailSearch = reactive({
  items: [
    { name: '상점명', value: 'title' },
    { name: '상점코드', value: 'code' },
  ],
  selectedItem: 'title',
  q: '',
  placeholder: '검색할 상점의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'title':
      selDetailSearch.placeholder = '검색할 상점의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearch.placeholder = '검색할 상점의 코드를 입력해주세요.';
      break;
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mStoreList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreList();
};

const clearSearchCondition = () => {
  selDetailSearch.selectedItem = 'title';
  selDetailSearch.q = '';
  onChangeDetailSearch();
  getStoreList();
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}`;
  useSearchStore().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  if (useSearchStore().getSearchInfo) {
    const paramsArray = JSON.parse(JSON.stringify(useSearchStore().getSearchInfo)).split('&');

    for (const param of paramsArray) {
      const [key, value] = param.split('=');

      switch (key) {
        case 'title':
        case 'code':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
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

const getStoreList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  setSearchInfo(query);

  apis.store.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mStoreList.value.total = res.total;
      mStoreList.value.datas = res.datas;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreList(false);
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  limit.value = useCommonStore().getLimit;
  if (getUserClassStr.value.includes('CM')) {
    getSearchInfo();
    page_no.value > 1 ? getStoreList(false) : getStoreList();
  } else {
    showAlert('비정상적인 접근입니다.');
    useRouter().back();
  }
});
</script>

<style scoped></style>
