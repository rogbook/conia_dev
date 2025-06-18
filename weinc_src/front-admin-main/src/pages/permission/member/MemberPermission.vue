<template>
  <PageNavigator :before_link="[]" :current="'개별권한설정'" />
  <div class="card mb-4">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">개별권한설정 - 회원조회</div>
    </div>
    <div class="card-body">
      <!-- 회원타입 Checkbox -->
      <div class="row">
        <label for="idLabel" class="col-md-1 col-form-label form-label">회원타입</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_type_all" class="form-check-input" name="search_type" v-model="checkedTypes.checkAll" @change="onChangeTypeAll" />
              <label class="form-check-label px-1" for="radio_type_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_type_pa" class="form-check-input" name="search_type" v-model="checkedTypes.checkPA" @change="onChangeType" />
              <label class="form-check-label px-1" for="radio_type_pa">PA</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_type_mc" class="form-check-input" name="search_type" v-model="checkedTypes.checkMC" @change="onChangeType" />
              <label class="form-check-label px-1" for="radio_type_mc">MC</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_type_cm" class="form-check-input" name="search_type" v-model="checkedTypes.checkCM" @change="onChangeType" />
              <label class="form-check-label px-1" for="radio_type_cm">CM</label>
            </div>
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
              <input type="checkbox" id="radio_status_y" class="form-check-input" name="search_type" value="y" v-model="checkedStatus.checkY" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_y">정상</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_p" class="form-check-input" name="search_type" value="p" v-model="checkedStatus.checkP" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_p">이용정지</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="checkbox" id="radio_status_n" class="form-check-input" name="search_type" value="n" v-model="checkedStatus.checkN" @change="onChangeStatus" />
              <label class="form-check-label px-1" for="radio_status_n">탈퇴</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 가입기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label">가입기간</label>
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="searchDate.sDate" @change="sDateChange()" />
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="searchDate.eDate" @change="eDateChange()" />
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
          <th style="width: 10%">회원타입</th>
          <th>이름</th>
          <th>아이디</th>
          <th>휴대전화</th>
          <th>가입일시</th>
          <th style="width: 10%">상태</th>
          <th style="width: 10%">권한설정</th>
        </tr>
      </thead>
      <tbody>
        <!-- 회원 검색 결과 목록 테이블 -->
        <tr class="text-center" v-for="(user, i) in userList.data" :key="user.id">
          <td>{{ getUserClass(user.classes) }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.mobile }}</td>
          <td>{{ dateTimeFormatConverter(user.reg_date) }}</td>
          <td>{{ user.status === 'Y' ? '정상' : user.status === 'P' ? '이용정지' : '탈퇴' }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/permission/member/detail`, state: { id: user.id } })">설정</button>
          </td>
        </tr>
        <tr>
          <td colspan="7" class="text-center" v-if="userList.data.length === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- Pagination -->
  <div class="table-footer-area" v-if="userList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
  <!-- End Pagination -->
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { User, Class } from 'UserInfoModule';
import apis from '@/apis';
import { useRouter } from 'vue-router';
import { AxiosError } from 'axios';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const userList = ref({
  data: {} as User[],
  total: 0,
});

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
    { name: '회사명', value: 'company_name' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});

const router = useRouter();

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
  checkN: true,
});

const onChangeType = () => {
  checkedTypes.checkAll = checkedTypes.checkMC && checkedTypes.checkPA && checkedTypes.checkCU && checkedTypes.checkCM;
};

const onChangeTypeAll = () => {
  if (checkedTypes.checkAll) {
    checkedTypes.checkPA = true;
    checkedTypes.checkMC = true;
    checkedTypes.checkCU = true;
    checkedTypes.checkCM = true;
  } else {
    checkedTypes.checkPA = false;
    checkedTypes.checkMC = false;
    checkedTypes.checkCU = false;
    checkedTypes.checkCM = false;
  }
};

const onChangeStatus = () => {
  checkedStatus.checkAll = checkedStatus.checkY && checkedStatus.checkP && checkedStatus.checkN;
};

const onChangeStatusAll = () => {
  if (checkedStatus.checkAll) {
    checkedStatus.checkY = true;
    checkedStatus.checkP = true;
    checkedStatus.checkN = true;
  } else {
    checkedStatus.checkY = false;
    checkedStatus.checkP = false;
    checkedStatus.checkN = false;
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
    case 'company_name':
      selDetailSearch.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
  }
};

const clearSearchCondition = () => {
  router.go(0);
};

const reqUserList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';
  // 검색할 회원타입 체크
  if (!checkedTypes.checkAll) {
    const classes = [];
    if (checkedTypes.checkPA) {
      classes.push('class_code=PA');
    }
    if (checkedTypes.checkMC) {
      classes.push('class_code=MC');
    }
    if (checkedTypes.checkCU) {
      // classes.push('class_code=CU');
    }
    if (checkedTypes.checkCM) {
      classes.push('class_code=CM');
    }
    query = query.concat(`${classes.join('&')}`);
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
    if (checkedStatus.checkN) {
      status.push('status=N');
    }
    query = query.concat(query ? `&${status.join('&')}` : `${status.join('&')}`);
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

  apis.user.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res.datas);
      userList.value.data = res.datas;
      userList.value.total = res.total;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  reqUserList(false);
  window.scrollTo({ top: 100, left: 0 });
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
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? reqUserList(false) : reqUserList();
});
</script>

<style scoped></style>
