<template>
  <PageNavigator :before_link="[]" :current="'고객 회원 관리'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">고객 회원 관리 - 상점 이용자</div>
    </div>
    <div class="card-body">
      <!-- 상점선택 영역 -->
      <div class="row" v-if="getUserClassStr.includes('CM')">
        <label class="col-md-1 col-form-label">상점선택</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" disabled :name="searchStore.code" id="storeModal" v-model="searchStore.title" placeholder="조회할 상점을 선택하세요." aria-label="조회할 상점을 선택하세요." />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('findStoreModal')" v-if="getUserClassStr.includes('CM')">검색</button>
          </div>
        </div>
      </div>
      <!-- 회원상태 Checkbox -->
      <div class="row">
        <label for="idLabel" class="col-md-1 col-form-label form-label">회원상태</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_all" class="form-check-input" name="search_type" value="all" v-model="checkedStatus.checkAll" @change="onChangeStatusAll" />
              <label class="form-check-label px-1" for="radio_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_y" class="form-check-input" name="search_type_status" value="Y" v-model="checkedStatus.checkY" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_y">정상</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_p" class="form-check-input" name="search_type_status" value="P" v-model="checkedStatus.checkP" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_p">이용정지</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_d" class="form-check-input" name="search_type_status" value="D" v-model="checkedStatus.checkD" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_d">탈퇴</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_r" class="form-check-input" name="search_type_status" value="R" v-model="checkedStatus.checkR" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_r">승인대기중</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_e" class="form-check-input" name="search_type_status" value="E" v-model="checkedStatus.checkE" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_e">이메일인증 대기중</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 가입기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label text-nowrap">검색기간 (가입기간)</label>
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
      <div class="row col">
        <label class="col-md-1 col-form-label">세부검색</label>
        <div class="col-md-2">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="reqUserList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqUserList">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="userList.total > 0">총 : {{ userList.total }}개</span>
    </div>
    <div class="col-auto row align-items-center">
      <div class="col-auto">
        <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="downloadExcel">조회내역 엑셀다운로드</button>
      </div>
      <div class="col-auto">
        <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
      </div>
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 5%">이름</th>
          <th style="width: 10%">아이디</th>
          <th style="width: 10%">휴대전화</th>
          <th style="width: 10%">가입일시</th>
          <th style="width: 5%">상태</th>
          <th style="width: 5%">추천인</th>
          <th style="width: 5%">이용상점(승인여부)</th>
          <th style="width: 5%">마케팅 동의여부</th>
          <th style="width: 10%">상세보기</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <tr class="text-center" v-for="(user, i) in userList.datas" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.mobile }}</td>
          <td>{{ dateTimeFormatConverter(user.reg_date) }}</td>
          <td>{{ convertUserStats(user.status) }}</td>
          <td>{{ user.recommend ? user.recommend : '-' }}</td>
          <td>
            <div v-if="!user.member_store || user.member_store.length === 0">없음</div>
            <div v-else>
              {{ user.member_store[0].store.title }} ({{ user.member_store[0].confirm === 'Y' ? '승인' : '미승인' }})
              <button type="button" class="btn badge bg-info ms-1 me-1" @click.prevent="showAllStore(user)" v-if="user.member_store.length > 1">{{ `외 ${user.member_store.length - 1}건` }}</button>
            </div>
          </td>
          <td>SMS{{ user.sms === 'Y' ? '(동의)' : '(미동의)' }} / EMAIL{{ user.mailling === 'Y' ? '(동의)' : '(미동의)' }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/customer/detail`, state: { id: user.id } })">상세보기</button>
          </td>
        </tr>
        <tr>
          <td colspan="8" class="text-center" v-if="userList.total == 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="userList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
  <!-- End Pagination -->

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
            <!-- Modal Search Form End -->
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
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="setStore(store.title!, store.code!)">선택</button>
                  </td>
                </tr>
                <tr>
                  <td colspan="2" class="text-center" v-if="storeList.total === 0">표시할 항목이 없습니다.</td>
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

  <!-- 정산보류사유  Modal -->
  <Modal :id="'allStoreModal'" :title="'이용상점목록'" :centered="true">
    <template #body>
      <div class="card">
        <div class="card-body">
          <table class="table table-nowrap table-align-middle card-table">
            <thead class="thead-light">
              <tr class="text-center">
                <th>상점명</th>
                <th>상점코드</th>
                <th>승인여부</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center" v-for="(s, i) in selectCustomer.member_store" :key="(s, i)">
                <td>{{ s.store.title }}</td>
                <td>{{ s.store.code }}</td>
                <td>{{ s.confirm === 'Y' ? '승인' : '미승인' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { User, Class } from 'UserInfoModule';
import type { StoreList } from 'StoreListInfoModule';
import apis from '@/apis';
import { useRouter, useRoute } from 'vue-router';
import Modal from '@/components/comm/modal.vue';
import { AxiosError } from 'axios';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showLogConsole, showModal, hideModal, showConfirm } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { CustomerList, Customer } from 'CustomerInfoModule';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';
import { useUserStore } from '@/stores/user';

const userList = ref({} as CustomerList);
const currentQueryStr = ref('');

const selectCustomer = ref({} as Customer);

const storeList = ref({} as StoreList);
const upMemberList = ref({
  data: {} as User[],
});

const searchStore = reactive({
  title: '',
  code: '',
});
const store_title = ref('');

const searchDate = reactive({
  sDate: '',
  eDate: '',
});
const isChangeDate = ref(true);
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(userList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  reqUserList();
};

const convertUserStats = (status: string): string => {
  switch (status) {
    case 'Y':
      return '정상';
    case 'R':
      return '승인대기중';
    case 'P':
      return '이용정지';
    case 'E':
      return '이메일인증 대기중';
    case 'D':
      return '탈퇴';
    default:
      return '';
  }
};

const selDetailSearch = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
    { name: '추천인', value: 'recommander' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});

const router = useRouter();
const route = useRoute();
const showDetailSearchArea = reactive({
  checkType: true,
  searchStore: false,
  searchMC: false,
});

const checkedTypes = reactive({
  checkAll: true,
  checkPA: true,
  checkMC: true,
  checkCU: true,
  checkCM: true,
});

const checkedStatus = reactive({
  checkAll: true,
  checkY: true,
  checkP: true,
  checkD: true,
  checkR: true,
  checkE: true,
});

const onChangeStatus = () => {
  if (checkedStatus.checkY && checkedStatus.checkP && checkedStatus.checkD && checkedStatus.checkR) {
    checkedStatus.checkAll = true;
  } else {
    checkedStatus.checkAll = false;
  }
};

const onChangeStatusAll = () => {
  if (checkedStatus.checkAll) {
    checkedStatus.checkY = true;
    checkedStatus.checkP = true;
    checkedStatus.checkD = true;
    checkedStatus.checkR = true;
    checkedStatus.checkE = true;
  } else {
    checkedStatus.checkY = false;
    checkedStatus.checkP = false;
    checkedStatus.checkD = false;
    checkedStatus.checkR = false;
    checkedStatus.checkE = false;
  }
};

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  searchStore.title = title;
  searchStore.code = code;
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

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearch.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearch.placeholder = "검색할 회원의 전화번호를 입력해주세요. ('-' 제외)";
      break;
    case 'recommander':
      selDetailSearch.placeholder = '검색할 회원의 추천인을 입력해주세요.';
      break;
  }
};

const pageChange = (page: number) => {
  page_no.value = page;
  reqUserList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const clearSearchCondition = () => {
  currentQueryStr.value = '';
  useSearchStore().$reset();
  router.go(0);
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}`;

  if (searchStore.code) {
    searchInfo.value += `&store_title=${searchStore.title}`;
  }
  useSearchStore().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  let checkStatus = false;
  checkedStatus.checkY = false;
  checkedStatus.checkP = false;
  checkedStatus.checkD = false;
  checkedStatus.checkR = false;
  checkedStatus.checkE = false;

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
        case 'name':
        case 'user_id':
        case 'mobile':
        case 'recommander':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        case 'status':
          checkStatus = true;
          if (value === 'Y') {
            checkedStatus.checkY = true;
          } else if (value === 'P') {
            checkedStatus.checkP = true;
          } else if (value === 'D') {
            checkedStatus.checkD = true;
          } else if (value === 'R') {
            checkedStatus.checkR = true;
          } else if (value === 'E') {
            checkedStatus.checkE = true;
          }
          break;
        case 'store_code':
          searchStore.code = value;
          break;
        case 'store_title':
          searchStore.title = value;
          break;
        default:
          break;
      }
    }
  }

  if (checkStatus) {
    checkedStatus.checkAll = false;
  } else {
    checkedStatus.checkAll = true;
    checkedStatus.checkY = true;
    checkedStatus.checkP = true;
    checkedStatus.checkD = true;
    checkedStatus.checkR = true;
    checkedStatus.checkE = true;
  }
};
/** */

const reqUserList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';
  if (searchStore.code) {
    query = query.concat(`store_code=${searchStore.code}`);
  }
  //회원 상태 체크
  const status = [];
  if (!checkedStatus.checkAll) {
    if (checkedStatus.checkY) {
      status.push('status=Y');
    }
    if (checkedStatus.checkP) {
      status.push('status=P');
    }
    if (checkedStatus.checkD) {
      status.push('status=D');
    }
    if (checkedStatus.checkR) {
      status.push('status=R');
    }
    if (checkedStatus.checkE) {
      status.push('status=E');
    }
    if (query) {
      query = query.concat(`&${status.join('&')}`);
    } else {
      query = query.concat(`${status.join('&')}`);
    }
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

  if (query) {
    query = query.concat('&');
  }
  currentQueryStr.value = query;
  setSearchInfo(query);
  apis.customer.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      userList.value.datas = res.datas;
      userList.value.total = res.total;
    });
  });
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

const downloadExcel = () => {
  showConfirm('현재 조회된 고객 회원 목록을 다운로드 하시겠습니까?', () => {
    const now = new Date();
    apis.customer.user_list_excel(currentQueryStr.value).then(res => {
      apiResponseCheck(res, async () => {
        const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `고객 회원 목록-${now.getFullYear()}${now.getMonth() + 1}${now.getDate()}${now.getHours()}${now.getMinutes()}${now.getSeconds()}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      });
    });
  });
};

const showAllStore = (customer: Customer) => {
  selectCustomer.value = customer;
  showModal('allStoreModal');
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  if (getUserClassStr.value.includes('MC')) {
    if (useUserStore().user.store_code) {
      searchStore.code = useUserStore().user.store_code as string;
    } else {
      showAlert('개설된 상점이 없습니다.', 'warning', () => {
        if (window.history.length > 1) {
          router.back();
        } else {
          router.replace('/');
        }
      });
      return;
    }
  }

  setSearchPeriod('all');
  getSearchInfo();
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? reqUserList(false) : reqUserList();
});
</script>

<style scoped></style>
