<template>
  <PageNavigator :before_link="[]" :current="'회원조회'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">회원조회</div>
    </div>
    <div class="card-body">
      <!-- 조회대상 Radio -->
      <div class="row">
        <label for="idLabel" class="col-md-1 col-form-label form-label">조회대상</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_search_type_m" class="form-check-input" name="search_type" value="member" @change="searchTypeChange($event)" v-model="isSearchType" />
              <label class="form-check-label px-1" for="radio_search_type_m">회원분류</label>
            </div>
            <div class="col-auto form-check form-check-inline" v-if="false">
              <input type="radio" id="radio_search_type_s" class="form-check-input" name="search_type" value="store" @change="searchTypeChange($event)" v-model="isSearchType" />
              <label class="form-check-label px-1" for="radio_search_type_s">상점 이용자</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_search_type_c" class="form-check-input" name="search_type" value="conn" @change="searchTypeChange($event)" v-model="isSearchType" />
              <label class="form-check-label px-1" for="radio_search_type_c">하위회원</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 회원타입 Checkbox -->
      <div class="row" v-if="showDetailSearchArea.checkType">
        <label for="idLabel" class="col-md-1 col-form-label form-label">회원타입</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_all" class="form-check-input" name="search_class_type" value="all" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_pa" class="form-check-input" name="search_class_type" value="PA" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_pa">PA</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_pa_s" class="form-check-input" name="search_class_type" value="PA-S" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_pa_s">PA-S</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_CO" class="form-check-input" name="search_class_type" value="CO" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_CO">CO</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_mc" class="form-check-input" name="search_class_type" value="MC" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_mc">MC</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_mc-v" class="form-check-input" name="search_class_type" value="MC-V" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_mc-v">MC-V</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_cm" class="form-check-input" name="search_class_type" value="CM" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_cm">CM</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_type_none" class="form-check-input" name="search_class_type" value="NONE" v-model="checkedTypes" />
              <label class="form-check-label px-1" for="radio_type_none">미지정</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 상점선택 영역 -->
      <div class="row" v-if="showDetailSearchArea.searchStore">
        <label class="col-md-1 col-form-label">상점선택</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" :name="searchStore.code" id="storeModal" v-model="searchStore.title" placeholder="조회할 상점을 선택하세요." aria-label="조회할 상점을 선택하세요." :disabled="true" @click.prevent="showModal('findStoreModal')" />
          </div>
        </div>
      </div>
      <!-- 상위회원선택 영역 -->
      <div class="row" v-if="showDetailSearchArea.searchMC">
        <label class="col-md-1 col-form-label">상위회원선택</label>
        <div class="col-md-4">
          <div class="input-group">
            <input type="text" class="form-control" :name="searchUpMember.code" id="mcModal" v-model="searchUpMember.name" placeholder="조회할 상위회원을 선택하세요." aria-label="조회할 상위회원을 선택하세요." :readonly="true" @click.prevent="showModal('findMcModal')" />
          </div>
        </div>
      </div>
      <!-- 회원상태 Checkbox -->
      <div class="row">
        <label for="idLabel" class="col-md-1 col-form-label form-label">회원상태</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_all" class="form-check-input" name="search_type_status" value="all" v-model="checkedStatus.checkAll" @change="onChangeStatusAll" />
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
        <label for="idLabel" class="col-md-1 col-form-label">검색기간</label>
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
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 5%">회원타입</th>
          <th style="width: 5%">이름</th>
          <th>업체명 / 상점명</th>
          <th style="width: 10%">아이디</th>
          <th style="width: 10%">휴대전화</th>
          <th style="width: 10%">가입일시</th>
          <th style="width: 5%">상태</th>
          <th style="width: 5%">추천인</th>
          <th style="width: 10%">상세보기</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <tr class="text-center" v-for="(user, i) in userList.data" :key="user.id">
          <td>{{ getUserClass(user.classes) }}</td>
          <td>{{ user.name }}</td>
          <td>{{ getUserClass(user.classes).includes('MC') ? (user.store[0]?.title ? `[상점] ${user.store[0].title}` : `상점정보 없음`) : user.company?.name ? `[업체] ${user.company?.name}` : '사업자정보 없음' }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.mobile }}</td>
          <td>{{ dateTimeFormatConverter(user.reg_date) }}</td>
          <td>{{ convertUserStats(user.status) }}</td>
          <td>{{ user.recommend ? user.recommend : '-' }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/user/detail`, state: { id: user.id } })">상세보기</button>
          </td>
        </tr>
        <tr>
          <td colspan="9" class="text-center" v-if="userList.total == 0">표시할 항목이 없습니다.</td>
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
                <tr class="text-center" v-for="(store, i) in storeList.data.datas" :key="JSON.stringify(store)">
                  <td>{{ store.title }}</td>
                  <td>
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="setStore(store.title!, store.code!)">선택</button>
                  </td>
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

  <!-- 상위회원검색 Modal -->
  <!-- TODO: 파트너검색 관련 데이터 작업 해야함. -->
  <Modal :id="'findMcModal'" :title="'회원 검색'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">상위회원을 검색해주세요.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <div class="mb-6">
              <div class="row col align-items-center">
                <label class="col-md-1 col-form-label text-nowrap">회원검색</label>
                <div class="col-md-2"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="upMember_name" v-model="upMember_name" placeholder="검색할 상위 회원을 입력해주세요." @submit.stop.prevent="reqUpMemberList()" @keypress.enter.prevent="reqUpMemberList()" />
                    <button type="button" class="btn btn-outline-info" @click.prevent="reqUpMemberList()">검색</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Modal Search Form End -->
            <!-- Member List Table -->
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>이름</th>
                  <th>아이디</th>
                  <th>선택</th>
                </tr>
              </thead>
              <tbody>
                <!-- 회원 검색 결과 목록 테이블 -->
                <!-- TODO: 테이블 데이터 표시 및 검색결과 없을때 표시처리 -->
                <!-- -->
                <!--  <ProductListItem v-for="(item, index) in productList" :item="item" :key="index" />-->
                <tr class="text-center" v-for="(m, i) in upMemberList.data" :key="m.id">
                  <td>{{ m.name }}</td>
                  <td>{{ m.email }}</td>
                  <td>
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="setUpMember(`${m.name}/${m.email}`, m.id)">선택</button>
                  </td>
                </tr>
              </tbody>
            </table>
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
import { computed, onMounted, reactive, ref } from 'vue';
import type { User, Class } from 'UserInfoModule';
import type { StoreList } from 'StoreListInfoModule';
import apis from '@/apis';
import { useRouter, useRoute } from 'vue-router';
import Modal from '@/components/comm/modal.vue';
import { AxiosError } from 'axios';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const userList = ref({
  data: {} as User[],
  total: 0,
});

const storeList = ref({
  data: {} as StoreList,
});
const upMemberList = ref({
  data: {} as User[],
});

const searchStore = reactive({
  title: '',
  code: '',
});
const store_title = ref('');

const searchUpMember = reactive({
  name: '',
  code: '',
});

const upMember_name = ref('');

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

const selDetailSearch = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
    { name: '추천인', value: 'recommander' },
    { name: '회사명', value: 'company_name' },
    { name: '상점명', value: 'store_title' },
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

const checkedTypes = ref('all');

const checkedStatus = reactive({
  checkAll: true,
  checkY: true,
  checkP: true,
  checkD: true,
  checkR: true,
  checkE: true,
});

const isSearchType = ref('member');

const searchTypeChange = (event: any) => {
  const selected = event.target.value;
  switch (selected) {
    case 'member':
      showDetailSearchArea.checkType = true;
      showDetailSearchArea.searchStore = false;
      showDetailSearchArea.searchMC = false;
      checkedStatus.checkAll = true;
      break;
    case 'store':
      showDetailSearchArea.checkType = false;
      showDetailSearchArea.searchStore = true;
      showDetailSearchArea.searchMC = false;
      break;
    case 'conn':
      showDetailSearchArea.checkType = false;
      showDetailSearchArea.searchStore = false;
      showDetailSearchArea.searchMC = true;
      break;
  }
};

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

const setUpMember = (upmember: string, code: string | number) => {
  hideModal('findMcModal');
  searchUpMember.name = upmember;
  searchUpMember.code = `${code}`;
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
    case 'company_name':
      selDetailSearch.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
  }
};

const pageChange = (page: number) => {
  page_no.value = page;
  reqUserList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const clearSearchCondition = () => {
  useSearchStore().$reset();
  router.go(0);
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}`;
  if (searchUpMember.name) {
    searchInfo.value += `&parent_member_name=${searchUpMember.name}`;
  }
  useSearchStore().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  isSearchType.value = 'member';
  checkedTypes.value = 'all';

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
        case 'company_name':
        case 'store_title':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        case 'parent_member_id':
          showDetailSearchArea.searchMC = true;
          showDetailSearchArea.checkType = false;
          isSearchType.value = 'conn';
          searchUpMember.code = value;
          break;
        case 'parent_member_name':
          searchUpMember.name = value;
          break;
        case 'class_code':
          isSearchType.value = 'member';
          checkedTypes.value = value;
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
  // 회원 타입 검색
  if (showDetailSearchArea.checkType) {
    // 검색할 회원타입 체크
    if (checkedTypes.value !== 'all') {
      query = query.concat(`class_code=${checkedTypes.value}`);
    }
  }
  // 상점 회원 검색
  else if (showDetailSearchArea.searchStore) {
    if (searchStore.code) {
      query = query.concat(`store_code=${searchStore.code}`);
    }
  }
  // 상위회원에 대한 하위 회원 검색
  else {
    // TODO: 하위회원 검색
    if (searchUpMember.code) {
      query = query.concat(`parent_member_id=${searchUpMember.code}`);
    }
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
  setSearchInfo(query);
  apis.user.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      userList.value.data = res.datas;
      userList.value.total = res.total;
    });
  });
};

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
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

const reqUpMemberList = () => {
  if (!upMember_name.value) {
    // 검색어 입력 안함.
    showAlert('검색할 상위 회원의 이름을 입력해주세요.', 'warning');
  } else {
    //검색어 입력함.
    apis.user.get_list(`name=${upMember_name.value}&class`).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        upMemberList.value.data = res.datas;
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

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  setSearchPeriod('all');
  getSearchInfo();
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? reqUserList(false) : reqUserList();
});
</script>

<style scoped></style>
