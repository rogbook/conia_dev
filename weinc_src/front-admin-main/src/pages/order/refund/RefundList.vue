<template>
  <PageNavigator :before_link="[]" :current="'관리자 환불내역'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">관리자 환불내역</div>
    </div>
    <div class="card-body">
      <!-- 상점 검색 -->
      <div class="row mb-2">
        <label class="col-md-1 col-form-label">상점선택</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" v-model="searchCondition.store.name" placeholder="조회할 상점을 선택하세요." aria-label="조회할 상점을 선택하세요." disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('findStoreModal')">검색</button>
          </div>
        </div>
      </div>
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(환불일자)</label>
        <div class="col">
          <div class="row">
            <div class="col-md-2">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange()" v-model="searchCondition.date.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-md-2">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange()" v-model="searchCondition.date.eDate" />
                </div>
              </div>
            </div>
            <div class="d-md-none mb-1"></div>
            <div class="col">
              <button class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
              <button class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
              <button class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
              <button class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
              <button class="btn btn-outline-info mb-1" @click.prevent="setSearchPeriod('all')">전체</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-md-1 col-form-label">세부검색</label>
        <div class="col-md-2 mb-1">
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getRefundList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getRefundList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="refundList.total > 0">총 : {{ refundList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive datatable-custom position-relative">
    <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 10%">주문번호</th>
          <th style="width: 20%">상품명</th>
          <th style="width: 5%">상점명</th>
          <th style="width: 5%">상점코드</th>
          <th style="width: 5%">주문자이름</th>
          <th style="width: 10%">주문자이메일</th>
          <th style="width: 10%">환불일자</th>
          <th style="width: 10%">환불금액</th>
          <th style="width: 5%">처리자</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(item, i) in refundList.datas" :key="item.id">
          <td>
            <a @click.prevent="router.push({ name: 'orderDetail', state: { orderId: item.order_id } })" style="cursor: pointer">{{ item.order_id }}</a>
          </td>
          <td>{{ item.product_name }}</td>
          <td>{{ item.store_name }}</td>
          <td>{{ item.store_code }}</td>
          <td>{{ item.customer.name }}</td>
          <td>{{ item.customer.email }}</td>
          <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
          <td>{{ item.amount.toLocaleString() }}원</td>
          <td>{{ item.member.name }}</td>
        </tr>
        <tr>
          <td colspan="9" class="text-center" v-if="refundList.total === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="refundList.total > 0">
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
            <div class="table-responsive">
              <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table table-nowrap">
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
            </div>
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
import { onMounted, reactive, computed, ref, watch } from 'vue';
import { getUserClassStr, dateTimeFormatConverter, showAlert, showLogConsole, apiResponseCheck, showModal, hideModal } from '@/utils/common-utils';
import type { StoreList } from 'StoreListInfoModule';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useRouter, useRoute } from 'vue-router';
import apis from '@/apis';
import type { RefundList } from 'RefundeInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';
import Modal from '@/components/comm/modal.vue';

const router = useRouter();
const route = useRoute();
const isChangeDate = ref(true);
const refundList = ref({} as RefundList);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(refundList.value.total / limit.value));

const store_title = ref('');
const storeList = ref({} as StoreList);
const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  searchCondition.store.name = title;
  searchCondition.store.code = code;

  store_title.value = '';
  storeList.value = {} as StoreList;
};

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

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getRefundList();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getRefundList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const searchCondition = reactive({
  date: {
    sDate: '',
    eDate: '',
  },
  store: {
    name: '',
    code: '',
  },
});

const selDetailSearch = reactive({
  items: [
    { name: '주문자이름', value: 'customer_name' },
    { name: '주문자이메일', value: 'customer_email' },
    { name: '주문번호', value: 'order_id' },
    { name: '상품명', value: 'product_name' },
  ],
  selectedItem: 'customer_name',
  q: '',
  placeholder: '검색할 주문자의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'customer_name':
      selDetailSearch.placeholder = '검색할 주문자의 이름을 입력해주세요.';
      break;
    case 'customer_email':
      selDetailSearch.placeholder = '검색할 주문자의 이메일을 입력해주세요.';
      break;
    case 'order_id':
      selDetailSearch.placeholder = '검색할 주문번호를 입력해주세요.';
      break;
    case 'product_name':
      selDetailSearch.placeholder = '검색할 상품명을 입력해주세요.';
      break;
  }
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
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        case 'customer_name':
        case 'customer_email':
        case 'order_id':
        case 'product_name':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        case 'store_code':
          searchCondition.store.code = value;
          break;
        case 'store_name':
          searchCondition.store.name = value;
          break;
        default:
          break;
      }
    }
  }
};
/** */

const getRefundList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  //상점선택
  if (searchCondition.store.code) {
    query = query.concat(query ? `&store_code=${searchCondition.store.code}&store_name=${searchCondition.store.name}` : `store_code=${searchCondition.store.code}&store_name=${searchCondition.store.name}`);
  }
  // //검색기간
  if (searchCondition.date.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchCondition.date.sDate}` : `s_reg_date=${searchCondition.date.sDate}`);
  }
  // //검색기간
  if (searchCondition.date.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchCondition.date.eDate}` : `e_reg_date=${searchCondition.date.eDate}`);
  }
  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  setSearchInfo(query);

  apis.order.get_refund_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      refundList.value.datas = res.datas;
      refundList.value.total = res.total;
      console.log(res);
    });
  });
};

const clearSearchCondition = () => {
  searchCondition.store.name = '';
  searchCondition.store.code = '';
  setSearchPeriod('all');
  selDetailSearch.selectedItem = 'customer_name';
  selDetailSearch.q = '';
  getRefundList();
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
      searchCondition.date.sDate = '';
      searchCondition.date.eDate = '';
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

onMounted(() => {
  setSearchPeriod('all');
  getSearchInfo();
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? getRefundList(false) : getRefundList();
});
</script>

<style scoped></style>
