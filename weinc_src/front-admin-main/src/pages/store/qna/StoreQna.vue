<template>
  <PageNavigator :before_link="[]" :current="'통합 고객 문의 관리'" />
  <div class="col-lg-8">
    <div class="card">
      <div class="card-header">
        <div class="row align-items-center justify-content-between">
          <div class="col-auto">
            <div class="form-control-borderless h2 mb-0">통합 고객 문의 관리</div>
          </div>
        </div>
      </div>
      <div class="card-body">
        <div class="row align-items-center">
          <label for="idLabel" class="col-lg-1 col-form-label">상점 검색</label>
          <div class="col-lg-4">
            <div class="input-group">
              <input type="text" class="form-control" v-model="storeTitle" placeholder="상점을 선택해주세요." aria-label="" disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="openStoreSelModal">검색</button>
            </div>
          </div>
        </div>
      </div>

      <div class="card-footer py-2">
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition()">초기화</button>
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStoreQnaList">검색</button>
        </div>
      </div>
    </div>
    <span class="divider-center py-4">검색결과</span>
    <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto"></div>
      <div class="col-auto">
        <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-align-middle border card-table table-vertical-border-striped table-bordered">
        <thead class="thead-light">
          <tr class="text-center">
            <th style="width: 34%">제목</th>
            <th>등록일</th>
            <th>작성자</th>
            <th>상점명</th>
            <th>상태</th>
            <th>상세</th>
          </tr>
        </thead>
        <tbody>
          <tr class="text-center" v-for="(item, i) in storeQnaList.datas" :key="item.id">
            <td>{{ item.title }}</td>
            <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
            <td>{{ item.customer.name }}</td>
            <td>
              {{ item.store.title }} <br />
              ({{ item.store.code }})
            </td>
            <td>{{ item.status === 'R' ? '답변대기중' : item.status === 'C' ? '답변완료' : '-' }}</td>
            <td>
              <div v-if="item.status === 'R'">
                <button type="button" class="btn btn-sm btn-warning" @click.prevent="router.push({ path: `/store/detail/qna`, state: { show: item.id, isTotal: true } })">답변하기</button>
              </div>
              <div v-if="item.status === 'C'">
                <button type="button" class="btn btn-sm btn-success" @click.prevent="router.push({ path: `/store/detail/qna`, state: { show: item.id, isTotal: true } })">상세보기</button>
              </div>
            </td>
          </tr>
          <tr v-if="storeQnaList.total === 0">
            <td colspan="6" class="text-center">표시할 항목이 없습니다.</td>
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

  <!-- PA 선택 Modal -->
  <Modal :id="'storeSelModal'" :title="'상점 선택'" :xlarge="true">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="row col">
            <label class="col-md-2 col-form-label">상점 검색</label>
            <div class="col-md-2 mb-1">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="selDetailSearchStore.selectedItem" @change="onChangeDetailSearchStore" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option v-for="detail in selDetailSearchStore.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" id="q" v-model="selDetailSearchStore.q" :placeholder="selDetailSearchStore.placeholder" @keypress.enter.prevent="getStoreList" />
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer py-2">
          <div class="text-end">
            <!-- <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="clearSearchCondition()">초기화</button> -->
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStoreList">검색</button>
          </div>
        </div>
      </div>
      <span class="divider-center py-4">검색결과</span>

      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto"></div>
        <div class="col-auto">
          <PageLimitCustom v-if="store_limit" :limit="store_limit" @changeLimitData="storeChangeLimitData" />
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
              <td>{{ s.status === 'Y' ? '운영중' : s.status === 'R' ? '오픈준비중' : '미운영' }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="setStoreInfo(s.title, s.code)">선택</button>
              </td>
            </tr>
            <tr class="text-center" v-if="mStoreList.total === 0">
              <td colspan="5">검색 결과가 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="mStoreList.total > 0">
        <div class="row" v-if="store_total_page > 1">
          <Pagination :currentPage="store_page_no" :totalPages="store_total_page" :pageChange="store_pageChange" />
        </div>
      </div>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, reactive } from 'vue';
import type { storeQnaInfoList } from 'StoreQnaInfoMOdule';
import type { StoreList } from 'StoreListInfoModule';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';
import Modal from '@/components/comm/modal.vue';

const router = useRouter();
const route = useRoute();

const storeQnaList = ref({} as storeQnaInfoList);
const mStoreList = ref({} as StoreList);
const storeCode = ref('');
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

// 상점 목록 페이지네이션
const store_page_no = ref(1);
const store_offset = computed(() => (store_page_no.value - 1) * store_limit.value);
const store_limit = ref(10);
const store_total_page = computed(() => Math.ceil(mStoreList.value.total / store_limit.value));
const storeChangeLimitData = (setLimitNum: number) => {
  store_page_no.value = 1;
  store_limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreList();
};

const storeTitle = ref('');

const selDetailSearchStore = reactive({
  items: [
    { name: '상점명', value: 'title' },
    { name: '상점코드', value: 'code' },
  ],
  selectedItem: 'title',
  q: '',
  placeholder: '검색할 상점의 이름을 입력해주세요.',
});

const onChangeDetailSearchStore = () => {
  switch (selDetailSearchStore.selectedItem) {
    case 'title':
      selDetailSearchStore.placeholder = '검색할 상점의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearchStore.placeholder = '검색할 상점의 코드를 입력해주세요.';
      break;
  }
};

const clearSearchCondition = () => {
  storeTitle.value = '';
  storeCode.value = '';
  getStoreQnaList();
};

const openStoreSelModal = () => {
  store_limit.value = useCommonStore().getLimit;
  showModal('storeSelModal');
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
        case 'store_code':
          storeCode.value = value;
        case 'storeTitle':
          storeTitle.value = value;
          break;
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

const getStoreQnaList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }

  let query = '';
  query = `customer_id=${customer_id.value}&`;

  if (storeCode) {
    query = query.concat(`store_code=${storeCode.value}&storeTitle=${storeTitle.value}`);
  }

  if (query) {
    query = query.concat('&');
  }

  setSearchInfo(query);

  apis.store.get_total_store_qna_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      storeQnaList.value.datas = res.datas;
      storeQnaList.value.total = res.total;
    });
  });
};

const getStoreList = (reset: boolean = true) => {
  if (reset) {
    store_page_no.value = 1;
  }

  let query = '';

  // 세부검색어 체크
  if (selDetailSearchStore.q) {
    const detail = `${selDetailSearchStore.selectedItem}=${selDetailSearchStore.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_list(query, store_offset.value, store_limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mStoreList.value.total = res.total;
      mStoreList.value.datas = res.datas;
    });
  });
};

const setStoreInfo = (title: string = '', code: string = '') => {
  storeTitle.value = title;
  storeCode.value = code;
  hideModal('storeSelModal');
  selDetailSearchStore.selectedItem = 'title';
  selDetailSearchStore.q = '';
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreQnaList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const store_pageChange = (page: number) => {
  store_page_no.value = page;
  getStoreList(false);
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  getSearchInfo();
  page_no.value > 1 ? getStoreQnaList(false) : getStoreQnaList();
});
</script>

<style scoped></style>
