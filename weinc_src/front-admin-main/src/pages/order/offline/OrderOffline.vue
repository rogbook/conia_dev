<template>
  <PageNavigator :before_link="[]" :current="'오프라인 매출관리'" />
  <div class="card col-md-9 mb-4">
    <div class="card-header py-2">
      <div class="row align-items-center justify-content-between">
        <div class="col-md-auto">
          <div class="form-control-borderless h2 mb-0">오프라인 매출관리</div>
        </div>
        <div class="col-md-auto" v-if="checkPermission('write:revenue_offline')">
          <button type="button" class="btn btn-sm btn-info" data-bs-toggle="modal" data-bs-target="#excelUploadModal">오프라인 매출등록</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-sm-2 col-md-1 col-form-label">[검색기간]</label>
        <div class="col-sm col-md col-lg">
          <div class="row">
            <div class="col-sm-6 col-md-3 mb-1">
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
            <span class="col-auto align-items-center mb-1">-</span>
            <div class="col-sm-6 col-md-3 mb-1">
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
            <div class="col-sm col-md col-lg">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('yesterday')">전일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-1 col-form-label">[세부검색]</label>
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getOfflineList" />
          </div>
        </div>
      </div>
      <!-- End 세부검색어 입력 -->
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getOfflineList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center col-9 py-4">조회결과</span>
  <div class="row col-sm-9 col-md-9 mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="offlineList.total > 0">총 : {{ offlineList.total }}개</span>
      <span v-if="offlineList.total > 0" class="ms-2 me-2">/</span>
      <span v-if="offlineList.total > 0">합계 : {{ offlineList.total_sum.toLocaleString() }}원</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive-md col-sm-9 col-md-9">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th>코드</th>
          <th>금액</th>
          <th>매출일자</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(item, i) in offlineList.data" :key="item.id">
          <td>{{ item.code }}</td>
          <td>{{ item.amount.toLocaleString() }}원</td>
          <td>{{ item.sales_date.replace('T', ' ') }}</td>
        </tr>
        <tr>
          <td colspan="3" class="text-center" v-if="offlineList.total === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="offlineList.total > 0">
      <div class="row" v-if="total_page > 1">
        <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
      </div>
    </div>
  </div>

  <!-- 카탈로그 생성 Modal -->
  <Modal :id="'excelUploadModal'" :title="'오프라인 매출내역 엑셀 업로드'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">카탈로그 기본정보</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <div class="row col mb-4 align-items-center">
              <label class="col-md-3 col-form-label text-nowrap">식별코드</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control" v-model.trim="uploadCode" maxlength="100" placeholder="식별코드를 입력해주세요. (최대 100자)" />
                </div>
              </div>
            </div>
            <div class="row col mb-4 align-items-center">
              <label class="col-md-3 col-form-label text-nowrap">엑셀 파일 선택</label>
              <div class="col-md-auto">
                <UploadExcel class="form-control" @upload="excelSelect" :btn="{ btnName: '엑셀 파일 선택', btnClass: 'btn btn-sm btn-info' }" />
              </div>
              <div class="col-md-auto" v-if="uploadFile">파일명 : {{ uploadFile.name }}</div>
            </div>
            <!-- Modal Search Form End -->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="uploadExcelInfo">엑셀 업로드</button>
    </template>
  </Modal>
</template>
<script setup lang="ts">
import PageNavigator from '@/components/title/PageNavigator.vue';
import { onMounted, ref, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, checkPermission, showAlert, showConfirm } from '@/utils/common-utils';
import UploadExcel from '@/components/comm/UploadExcel.vue';
import apis from '@/apis';
import type { OfflineList } from 'OfflineInfoModule';
import Modal from '@/components/comm/modal.vue';
import { useCommonStore } from '@/stores/common';
import Pagination from '@/components/comm/Pagination.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';

const router = useRouter();
const route = useRoute();
const isChangeDate = ref(true);
const offlineList = ref({} as OfflineList);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(offlineList.value.total / limit.value));

const uploadCode = ref('');
const uploadFile = ref(null as File | null);

const searchCondition = reactive({
  date: {
    sDate: '',
    eDate: '',
  },
});

const selDetailSearch = reactive({
  items: [{ name: '코드', value: 'code' }],
  selectedItem: 'code',
  q: '',
  placeholder: '검색할 코드를 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'code':
      selDetailSearch.placeholder = '검색할 코드를 입력해주세요.';
      break;
  }
};

const getOfflineList = (reset: boolean = true) => {
  const date1 = new Date(searchCondition.date.sDate);
  const date2 = new Date(searchCondition.date.eDate);
  const timeDiff = Math.abs(date2.getTime() - date1.getTime());
  const diffMonths = Math.ceil(timeDiff / (1000 * 3600 * 24 * 31));
  if (diffMonths > 6) {
    showAlert('검색기간은 6개월 이하로만 조회가 가능합니다.', 'warning');
    setSearchPeriod('today');
    return;
  }

  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  //검색기간
  if (searchCondition.date.sDate) {
    query = query.concat(query ? `&s_sales_date=${searchCondition.date.sDate}` : `s_sales_date=${searchCondition.date.sDate}`);
  }
  //검색기간
  if (searchCondition.date.eDate) {
    query = query.concat(query ? `&e_sales_date=${searchCondition.date.eDate}` : `e_sales_date=${searchCondition.date.eDate}`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    if (query) {
      query = query.concat(`&${detail}`);
    } else {
      query = query.concat(`${detail}`);
    }
  }

  if (query) {
    query = query.concat('&');
  }

  apis.revenue.get_revenue_offline(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      offlineList.value.data = res.data;
      offlineList.value.total = res.total;
      offlineList.value.total_sum = res.total_sum;
    });
  });
};

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getOfflineList();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getOfflineList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const clearSearchCondition = () => {
  selDetailSearch.selectedItem = 'code';
  selDetailSearch.q = '';
  setSearchPeriod('today');
  getOfflineList();
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
      return;
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
      return;
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
    case 'yesterday':
      // @ts-ignore
      efp.setDate(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1), true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1), true, 'Y-m-d');
      break;
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

const excelSelect = (file: File) => {
  console.log(file);
  uploadFile.value = file;
};

const uploadExcelInfo = () => {
  if (!uploadCode.value) {
    showAlert('식별 코드를 입력해주세요.', 'warning');
    return;
  }

  if (!uploadFile.value) {
    showAlert('업로드할 엑셀 파일을 선택해주세요', 'warning');
    return;
  }

  showConfirm('엑셀 파일을 업로드 하시겠습니까?', () => {
    apis.revenue.add_revenue_offline(uploadCode.value, uploadFile.value!).then(res => {
      apiResponseCheck(res, () => {
        showAlert('엑셀 파일이 성공적으로 업로드 되었습니다.', 'success', () => {
          //@ts-ignore
          window.$('#excelUploadModal').modal('toggle');
        });
        getOfflineList();
      });
    });
  });
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('excelUploadModal').addEventListener('show.bs.modal', function (event) {
    uploadCode.value = '';
    uploadFile.value = null;
  });

  //@ts-ignore
  document.getElementById('excelUploadModal').addEventListener('hide.bs.modal', function (event) {
    uploadCode.value = '';
    uploadFile.value = null;
  });
  setSearchPeriod('today');

  //매출현황에서 진입시
  if (history.state.orderDate) {
    searchCondition.date.sDate = history.state.orderDate;
    searchCondition.date.eDate = history.state.orderDate;
  }

  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? getOfflineList(false) : getOfflineList();
});
</script>
<style scoped></style>
