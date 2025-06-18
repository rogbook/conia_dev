<template>
  <PageNavigator :before_link="[]" :current="'교환/반품 관리'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">교환/반품 현황</div>
    </div>
    <div class="card-body py-2">
      <!-- 주문상태 Checkbox -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label form-label">교환/반품 상태</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_all" class="form-check-input" name="status_type" value="all" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_exr" class="form-check-input" name="status_type" value="EXR" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_exr">교환요청</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_exn" class="form-check-input" name="status_type" value="EXN" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_exn">교환진행중</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_exc" class="form-check-input" name="status_type" value="EXC" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_exc">교환완료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_rfr" class="form-check-input" name="status_type" value="RFR" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_rfr">반품요청</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_rfn" class="form-check-input" name="status_type" value="RFN" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_rfn">반품진행중</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_status_rfc" class="form-check-input" name="status_type" value="RFC" v-model="searchCondition.status" @change="getExReList()" />
              <label class="form-check-label px-1" for="radio_status_rfc">반품완료</label>
            </div>
          </div>
        </div>
        <!-- </div> -->
        <!-- 상점 검색 -->
        <div class="row mb-2">
          <label class="col-md-1 col-form-label">상점선택</label>
          <div class="col-md-4">
            <div class="input-group">
              <input type="text" class="form-control" v-model="searchCondition.store.name" placeholder="조회할 상점을 선택하세요." aria-label="조회할 상점을 선택하세요." disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('findStoreModal')" v-if="userClass.includes('PA') || userClass.includes('CM')">검색</button>
            </div>
          </div>
        </div>
        <!-- 검색기간 Datepicker -->
        <div class="row mb-2">
          <label for="idLabel" class="col-md-1 col-form-label">검색기간</label>
          <div class="col">
            <div class="row">
              <div class="col-md-2">
                <!-- Select -->
                <div class="tom-select-custom">
                  <select class="form-select" v-model="searchCondition.date.type" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                    <option value="request">요청일자</option>
                  </select>
                </div>
                <!-- End Select -->
              </div>
              <div class="d-md-none mt-1"></div>
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
                    <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="searchCondition.date.sDate" @change="sDateChange" />
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
                    <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="searchCondition.date.eDate" @change="eDateChange" />
                  </div>
                </div>
              </div>
              <div class="d-lg-none mt-2"></div>
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

        <div class="row">
          <label class="col-md-1 col-form-label">세부검색</label>
          <div class="col">
            <div class="row">
              <div class="col-md-2">
                <!-- Select -->
                <div class="tom-select-custom">
                  <select class="form-select" v-model="searchCondition.q.type" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                    <option value="order_name">주문자</option>
                    <option value="order_email">주문자 아이디(이메일)</option>
                    <option value="order_id">주문번호</option>
                  </select>
                </div>
                <!-- End Select -->
              </div>
              <div class="d-md-none mt-1"></div>
              <div class="col-md-4">
                <div class="input-group">
                  <input type="text" class="form-control" placeholder="검색어를 입력하세요." id="q" v-model="searchCondition.q.value" @keypress.enter.prevent="getExReList" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer py-2">
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="clearSearchCondition()">초기화</button>
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getExReList()">검색</button>
        </div>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>
  <div class="row align-items-center mb-3 justify-content-between" v-if="mExReList.total > 0">
    <div class="col-auto">총 : {{ mExReList.total }}개</div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <div class="list-area">
    <table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 5%">구분</th>
          <th style="width: 10%">주문번호</th>
          <th>상품</th>
          <th style="width: 10%">요청일자</th>
          <th style="width: 10%">완료일자</th>
          <th style="width: 5%">상태</th>
          <th style="width: 5%">상세</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <tr class="text-center" v-for="(exre, i) in mExReList.datas" :key="JSON.stringify(exre)">
          <td>{{ convertExReType(exre.parent.type) }}</td>
          <td>{{ exre.parent.order_id }}</td>
          <td class="text-center text-wrap">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-auto">
                  <img :src="exre.product.product_thumbnail" style="width: 50px" />
                </div>
                <div class="col text-start">
                  <div class="mb-1">
                    <b>{{ exre.product.product_name }}</b>
                  </div>
                  <div class="" v-if="exre.product.product_option_name">(옵션명 : {{ exre.product.product_option_name }})</div>
                </div>
              </div>
            </div>
          </td>
          <td>{{ dateTimeFormatConverter(exre.reg_date) }}</td>
          <td>{{ exre.end_date ? dateTimeFormatConverter(exre.end_date) : '-' }}</td>
          <td>{{ convertOrderStatus(exre.product.status) }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ name: 'exreDetail', state: { order_re: JSON.stringify(exre), orderOriginId: exre.parent.order_id } })">상세</button>
          </td>
        </tr>
        <tr>
          <td colspan="7" class="text-center" v-if="mExReList.total === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="mExReList.total > 0">
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
import Modal from '@/components/comm/modal.vue';
import { computed, onMounted, reactive, ref } from 'vue';
import { apiResponseCheck, convertOrderStatus, dateTimeFormatConverter, showAlert, showLogConsole, getUserClassStr, showModal, hideModal } from '@/utils/common-utils';
import type { StoreList } from 'StoreListInfoModule';
import apis from '@/apis';
import { useRouter, useRoute } from 'vue-router';
import Pagination from '@/components/comm/Pagination.vue';
import type { ExReList, ExReListInfo } from 'ExReInfoModule';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const router = useRouter();
const route = useRoute();
const isChangeDate = ref(true);
const searchCondition = reactive({
  q: {
    type: 'order_name',
    value: '',
  },
  status: 'all',
  date: {
    type: 'request',
    sDate: '',
    eDate: '',
  },
  store: {
    name: '',
    code: '',
  },
});
const user = useUserStore().user;
const userName = computed(() => {
  return `${useUserStore().user.name}`;
});
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

// 선택 상품 리스트 (담은 상품)
const mSelOrderProdList = ref([] as number[]);

const mExReList = ref({} as ExReList);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mExReList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getExReList();
};

const store_title = ref('');
const storeList = ref({} as StoreList);
const storeCode = ref(useUserStore().user.store_code);
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

const clearSearchCondition = () => {
  if (userClass.value.includes('MC')) {
    //@ts-ignore
    searchCondition.store.code = useUserStore().user.store_code;
    searchCondition.store.name = userName.value;
  } else {
    searchCondition.store.code = '';
    searchCondition.store.name = '';
  }

  searchCondition.q.type = 'order_name';
  searchCondition.q.value = '';
  searchCondition.status = 'all';
  searchCondition.date.type = 'request';
  searchCondition.date.sDate = '';
  searchCondition.date.eDate = '';
  getExReList();
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
        case 'status':
          searchCondition.status = value;
          break;
        case 's_reg_date':
          searchCondition.date.sDate = value;
          break;
        case 'e_reg_date':
          searchCondition.date.eDate = value;
          break;
        case 'order_name':
        case 'order_email':
        case 'order_id':
          searchCondition.q.type = key;
          searchCondition.q.value = value;
          break;
        case 'page_no':
          page_no.value = parseInt(value);
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

const getExReList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  if (!getUserClassStr.value.includes('CM')) {
    if (getUserClassStr.value.includes('PA')) {
      query = query.concat(query ? `&pa_id=${useUserStore().user.id}` : `pa_id=${useUserStore().user.id}`);
    }
  }

  if (searchCondition.store.code) {
    query = query.concat(query ? `&store_code=${searchCondition.store.code}&store_name=${searchCondition.store.name}` : `store_code=${searchCondition.store.code}&store_name=${searchCondition.store.name}`);
  }

  if (searchCondition.status !== 'all') {
    query = query.concat(query ? `&status=${searchCondition.status}` : `status=${searchCondition.status}`);
  }

  // 검색기간 시작날짜
  if (searchCondition.date.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchCondition.date.sDate}` : `s_reg_date=${searchCondition.date.sDate}`);
  }
  // 검색기간 종료날짜
  if (searchCondition.date.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchCondition.date.eDate}` : `e_reg_date=${searchCondition.date.eDate}`);
  }

  // 세부 검색
  if (searchCondition.q.value) {
    query = query.concat(query ? `&${searchCondition.q.type}=${searchCondition.q.value}` : `${searchCondition.q.type}=${searchCondition.q.value}`);
  }

  if (query) {
    query = query.concat('&');
  }
  setSearchInfo(query);

  apis.order.get_exre_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mExReList.value = res;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getExReList(false);
  window.scrollTo({ top: 100, left: 0 });
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

const convertExReType = (type: string) => {
  return type === 'return' || type === '반품' ? '반품' : type === 'exchange' ? '교환' : '-';
};

const convertExReStatus = (status: string) => {
  return status === 'R' ? '요청중' : status === 'C' ? '완료' : '진행중';
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  setSearchPeriod('all');

  if (userClass.value.includes('MC')) {
    //@ts-ignore
    searchCondition.store.code = useUserStore().user.store_code;
    searchCondition.store.name = userName.value;
  } else {
    searchCondition.store.code = '';
    searchCondition.store.name = '';
  }
  getSearchInfo();
  page_no.value > 1 ? getExReList(false) : getExReList();
});
</script>

<style scoped></style>
