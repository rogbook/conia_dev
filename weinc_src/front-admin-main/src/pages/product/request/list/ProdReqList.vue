<template>
  <PageNavigator :before_link="[]" :current="'상품 요청'" />
  <div class="card">
    <div class="card-header py-2">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">상품 요청 목록</div>
        </div>
        <div class="col-auto">
          <div class="text-end">
            <button
              type="submit"
              class="btn btn-info"
              @click.prevent="
                useSearchStore().$reset();
                router.push(`/product/req`);
              "
              style="float: right">
              상품요청
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="row mb-2 align-items-center" v-if="userClass.includes('CM')">
        <label for="idLabel" class="col-md-1 col-form-label">상점검색</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" v-model="store.store_name" placeholder="상점을 선택해주세요." aria-label="" readonly />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('findStoreModal')">검색</button>
          </div>
        </div>
      </div>
      <!-- 요청상태 Checkbox -->
      <div class="row">
        <label for="idLabel" class="col-md-1 col-form-label form-label">요청상태</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_y" class="form-check-input" name="search_type" value="R" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_y">요청</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_p" class="form-check-input" name="search_type" value="C" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_p">완료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_n" class="form-check-input" name="search_type" value="D" v-model="checkedStatus" />
              <label class="form-check-label px-1" for="radio_status_n">반려</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(요청일)</label>
        <div class="col">
          <div class="row">
            <div class="col-md-2">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="startDatepicker"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#startDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange()" v-model="searchDate.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-md-2">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="endDatepicker"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#endDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange()" v-model="searchDate.eDate" />
                </div>
              </div>
            </div>
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
              <button type="button" class="btn btn-outline-info mb-1" @click.prevent="setSearchPeriod('all')">전체</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 세부검색어 입력 -->
      <div class="row col" v-if="false">
        <label class="col-1 col-form-label">세부검색</label>
        <div class="col-2">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getReqList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>

        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getReqList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mProdReqList.total > 0">총 : {{ mProdReqList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <div class="table-responsive datatable-custom position-relative">
    <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 5%">요청번호</th>
          <th>요청 상품</th>
          <th style="width: 10%">요청자</th>
          <th style="width: 10%">상점</th>
          <th style="width: 10%">요청일</th>
          <th style="width: 5%">요청상태</th>
          <th style="width: 5%">요청상세</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="item in mProdReqList.datas" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.title }}</td>
          <td>{{ `${item.member.name} (${item.member.email})` }}</td>
          <td>{{ `${item.store.title} (${item.store.code})` }}</td>
          <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
          <td>{{ item.status === 'R' ? '요청중' : item.status === 'C' ? '요청완료' : '요청반려' }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: '/product/req/detail', state: { id: item.id } })">상세</button>
          </td>
        </tr>
        <tr v-if="mProdReqList.total === 0">
          <td class="text-center" colspan="7">검색결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="mProdReqList.total > 0">
      <div class="row" v-if="total_page > 1">
        <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
      </div>
    </div>
  </div>

  <!-- 상점검색 Modal -->
  <Modal :id="'findStoreModal'" :title="'상점 검색'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">상점을 검색해주세요.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <div class="mb-6">
              <div class="row col align-items-center">
                <label class="col-md-1 col-form-label text-nowrap">상점검색</label>
                <div class="col-md-2"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="store_title" v-model="store_title" placeholder="검색할 상점의 이름을 입력해주세요." @submit.stop.prevent="reqStoreList()" @keypress.enter.prevent="reqStoreList()" />
                    <button type="button" class="btn btn-outline-info" @click.prevent="reqStoreList()">검색</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Member List Table -->
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>상점</th>
                  <th style="width: 10%">선택</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(store, i) in storeList.datas" :key="JSON.stringify(store)">
                  <td>{{ store.title }}</td>
                  <td>
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="setStore(store.title as string, store.code as string)">선택</button>
                  </td>
                </tr>
                <tr v-if="!storeList.datas || storeList.datas.length === 0">
                  <td colspan="2" class="text-center">검색 결과가 없습니다.</td>
                </tr>
              </tbody>
            </table>
            <!-- Member List Table End-->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';
import type { StoreList } from 'StoreListInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useUserStore } from '@/stores/user';
import type { ProdReqListInfo } from 'ProdReqListInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const user_id = ref(0);

const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const router = useRouter();
const route = useRoute();
const mProdReqList = ref({} as ProdReqListInfo);
const mProductList = ref({} as any);
const checkedStatus = ref('R');
const isChangeDate = ref(true);
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProdReqList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getReqList();
};

const searchDate = reactive({
  sDate: '',
  eDate: '',
});

const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 상품의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearch.placeholder = '검색할 상품의 코드를 입력해주세요.';
      break;
  }
};

const store_title = ref('');
const storeList = ref({} as StoreList);

const reqStoreList = () => {
  if (!store_title.value) {
    //검색어 입력안함.
    showAlert('검색할 상점의 이름을 입력해주세요.', 'warning');
  } else {
    //검색어 입력함.
    apis.store.get_list(`title=${store_title.value}&`).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        storeList.value = res;
      });
    });
  }
};

const store = reactive({
  store_code: '',
  store_name: '',
});

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  store.store_name = title;
  store.store_code = code;

  store_title.value = '';
  storeList.value = {} as StoreList;
};

const pageChange = (page: number) => {
  page_no.value = page;
  getReqList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const setSearchPeriod = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
  switch (period) {
    case 'today':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(today, true, 'Y-m-d');
      break;
    case 'week':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 7), true, 'Y-m-d');
      break;
    case 'month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 30), true, 'Y-m-d');
      break;
    case '3month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 90), true, 'Y-m-d');
      break;
    case '6month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 180), true, 'Y-m-d');
      break;
    default:
      searchDate.sDate = '';
      searchDate.eDate = '';
      break;
  }
  isChangeDate.value = true;
};

const sDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        sfp.setDate(new Date(eDate), true, 'Y-m-d');
      });
    }
  }
};
const eDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        efp.setDate(new Date(sDate), true, 'Y-m-d');
      });
    }
  }
};

const clearSearchCondition = () => {
  setSearchPeriod('all');
  checkedStatus.value = 'R';
  store.store_code = '';
  store.store_name = '';
  selDetailSearch.q = '';
  getReqList();
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}&store_name=${store.store_name}`;
  useSearchStore().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  if (useSearchStore().getSearchInfo) {
    const paramsArray = JSON.parse(JSON.stringify(useSearchStore().getSearchInfo)).split('&');

    for (const param of paramsArray) {
      const [key, value] = param.split('=');
      switch (key) {
        case 's_reg_date':
          searchDate.sDate = value;
          break;
        case 'e_reg_date':
          searchDate.eDate = value;
          break;
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        case 'store_code':
          store.store_code = value;
          break;
        case 'store_name':
          store.store_name = value;
          break;
        case 'status':
          checkedStatus.value = value;
          break;
        default:
          break;
      }
    }
  }
};
/** */

const getReqList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = `status=${checkedStatus.value}`;

  if (store.store_name) {
    query = query.concat(query ? `&store_code=${store.store_code}` : `store_code=${store.store_code}`);
  }

  //검색기간
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `s_reg_date=${searchDate.sDate}`);
  }
  //검색기간
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `e_reg_date=${searchDate.eDate}`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (user_id.value > 0) {
    query = query.concat(query ? `&member_id=${user_id.value}` : `member_id=${user_id.value}`);
  }

  if (query) {
    query = query.concat('&');
  }

  setSearchInfo(query);

  apis.product.reqProdList(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProdReqList.value = res;
    });
  });
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  setSearchPeriod('all');
  getSearchInfo();
  if (!userClass.value.includes('CM')) {
    user_id.value = useUserStore().user.id as number;
  }
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? getReqList(false) : getReqList();
});
</script>

<style scoped></style>
