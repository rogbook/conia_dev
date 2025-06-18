<template>
  <PageNavigator :before_link="[]" :current="'카탈로그 관리'" />
  <div class="card mb-4">
    <div class="card-header py-2">
      <div class="row align-items-center">
        <div class="form-control-borderless h2 col mb-0">카탈로그 관리</div>
        <button type="button" class="btn btn-outline-dark col-auto" @click.prevent="showModal('makeCatalogModal')">카탈로그 생성</button>
      </div>
    </div>
    <div class="card-body py-2">
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-1 col-form-label">검색어</label>
        <div class="col-lg-2">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-lg-none mt-1"></div>
        <div class="col-lg-4">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getCatalogList" />
          </div>
        </div>
      </div>
      <!-- 날짜 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-1 col-form-label">등록일</label>
        <div class="col">
          <div class="row">
            <div class="col-lg-2">
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
            <div class="col-lg-2">
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
            <div class="d-lg-none mt-1"></div>
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
      <!-- 노출여부 Checkbox -->
      <div class="row mb-2">
        <label for="idLabel" class="col-lg-1 col-form-label form-label">노출여부</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="formInlineRadio1" type="radio" class="form-check-input" checked name="formInlineRadio" value="all" v-model="selDetailSearch.open" />
              <label class="form-check-label" for="formInlineRadio1">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="formInlineRadio2" type="radio" class="form-check-input" name="formInlineRadio" value="Y" v-model="selDetailSearch.open" />
              <label class="form-check-label" for="formInlineRadio2">노출</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="formInlineRadio3" type="radio" class="form-check-input" name="formInlineRadio" value="N" v-model="selDetailSearch.open" />
              <label class="form-check-label" for="formInlineRadio3">비노출</label>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getCatalogList">검색</button>
      </div>
    </div>
  </div>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="catalogData.total > 0">총 : {{ catalogData.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-nowrap table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 20%">카탈로그명</th>
          <th>카탈로그 설명</th>
          <th style="width: 5%">생성자</th>
          <th style="width: 10%">등록일/수정일</th>
          <th style="width: 5%">노출</th>
          <th style="width: 8%">관리</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(c, i) in catalogData.datas" :key="c.id">
          <td>{{ c.name }}</td>
          <td class="text-wrap">{{ c.description }}</td>
          <td>{{ c.member.name }}</td>
          <td>{{ c.reg_date.slice(0, 10) }} / {{ c.mod_date.slice(0, 10) }}</td>
          <td>
            {{ c.open === 'Y' ? '노출' : '비노출' }}
          </td>
          <td>
            <button type="button" class="btn btn-sm btn-white" @click.prevent="router.push({ name: 'productCatalogDetail', state: { catalog: JSON.stringify(c) } })">상세</button>
          </td>
        </tr>
        <tr v-if="catalogData.total === 0" class="text-center">
          <td colspan="6">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="table-footer-area" v-if="catalogData.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>

  <!-- 카탈로그 생성 Modal -->
  <Modal :id="'makeCatalogModal'" :title="'카탈로그 생성'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">카탈로그 기본정보</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <form class="mb-6">
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">카탈로그명</label>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" v-model.trim="newCatalog.name" maxlength="20" placeholder="카탈로그명을 입력해주세요. (최대 20자)" />
                  </div>
                </div>
              </div>
              <div class="row col mb-4 align-items-center">
                <label class="col-md-3 col-form-label text-nowrap">카탈로그설명</label>
                <div class="col">
                  <div class="input-group">
                    <textarea type="text" class="form-control" rows="5" v-model="newCatalog.description" maxlength="255" placeholder="카탈로그에 대한 설명을 입력해주세요." />
                  </div>
                </div>
              </div>
              <div class="row col mb-2" v-if="false">
                <label for="idLabel" class="col-md-2 col-form-label form-label">노출여부</label>
                <div class="col form-control border-0">
                  <div class="form-check form-check-inline">
                    <input id="formInlineRadio4" type="radio" class="form-check-input" checked name="formInlineRadio" value="Y" v-model="newCatalog.status" />
                    <label class="form-check-label" for="formInlineRadio4">노출</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input id="formInlineRadio5" type="radio" class="form-check-input" checked name="formInlineRadio" value="N" v-model="newCatalog.status" />
                    <label class="form-check-label" for="formInlineRadio5">비노출</label>
                  </div>
                </div>
              </div>
            </form>
            <!-- Modal Search Form End -->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="addCatalog">카탈로그 생성</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { onMounted, reactive, ref, computed, watch } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRouter, useRoute } from 'vue-router';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import type { CatalogDataList, Catalog } from 'CatalogProductModule';
import { useUserStore } from '@/stores/user';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const router = useRouter();
const route = useRoute();
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(catalogData.value.total / limit.value));
const isChangeDate = ref(true);
const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getCatalogList();
};

const newCatalog = ref({
  name: '',
  description: '',
  status: 'Y',
});

const searchDate = reactive({
  sDate: '',
  eDate: '',
});

const catalogData = ref({} as CatalogDataList);

const selDetailSearch = reactive({
  items: [{ name: '카탈로그명', value: 'name' }],
  selectedItem: 'name',
  q: '',
  open: 'all',
  placeholder: '검색할 카탈로그명을 입력해주세요.',
});

const pageChange = (page: number) => {
  page_no.value = page;
  getCatalogList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const addCatalog = () => {
  if (!newCatalog.value.name) {
    showAlert('카탈로그명을 입력해주세요.', 'warning');
    return;
  }

  if (!newCatalog.value.description) {
    showAlert('카탈로그 설명을 입력해주세요.', 'warning');
    return;
  }

  if (newCatalog.value.name && newCatalog.value.description) {
    showConfirm('카탈로그를 등록하시겠습니까?', () => {
      apis.catalog.add_catalog(newCatalog.value.name, newCatalog.value.description, useUserStore().user.id as number, newCatalog.value.status).then(res => {
        apiResponseCheck(
          res,
          () => {
            showAlert('카탈로그가 생성되었습니다.', 'success');
            hideModal('makeCatalogModal');
            getCatalogList();
          },
          (num?: number) => {
            if (num === 403) {
              hideModal('makeCatalogModal');
            }
          },
        );
      });
    });
  }
};

const clearSearchCondition = () => {
  setSearchPeriod('all');
  selDetailSearch.open = 'all';
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  getCatalogList();
};

const getCatalogList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  if (selDetailSearch.open !== 'all') {
    query = query.concat(query ? `&open=${selDetailSearch.open}` : `open=${selDetailSearch.open}`);
  }
  // 검색기간 시작날짜
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `s_reg_date=${searchDate.sDate}`);
  }
  // 검색기간 종료날짜
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `e_reg_date=${searchDate.eDate}`);
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

  setSearchInfo(query);

  apis.catalog.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      catalogData.value.datas = res.datas;
      catalogData.value.total = res.total;
    });
  });
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
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        case 'open':
          selDetailSearch.open = value;
          break;
        default:
          break;
      }
    }
  }
};
/** */

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 카탈로그명을 입력해주세요.';
      break;
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
  page_no.value > 1 ? getCatalogList(false) : getCatalogList();
});
</script>

<style scoped></style>
