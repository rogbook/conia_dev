<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세', '상점 게시판 관리'] : ['상점 관리', '상점관리 상세']" :current="'이벤트 관리'" />
  <div class="card">
    <div class="card-header">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">{{ groupName }} 관리</div>
          <!-- <div class="form-control-borderless h4">게시판 제목 : [{{ groupName }}]</div> -->
          <span v-if="getUserClassStr.includes('CM')"><MobilePushLink :title="`${groupName}`" :storeGroup="storeGroup" :nextValue="`board/${groupId}`" :isStore="true" /></span>
        </div>
        <div class="col-auto">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="modStoreBoardGroup">저장</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card-body">
      <div class="row col mb-2 align-items-center">
        <label class="col-lg-1 col-form-label">메뉴 노출여부</label>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_menu_visible_y" type="radio" class="form-check-input" name="radio_menu_visible" value="Y" v-model="mStoreBoardGroup.menu_visible" @change="changeViewType" />
            <label class="form-check-label" for="radio_menu_visible_y">노출</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_menu_visible_n" type="radio" class="form-check-input" name="radio_menu_visible" value="N" v-model="mStoreBoardGroup.menu_visible" @change="changeViewType" />
            <label class="form-check-label" for="radio_menu_visible_n">비노출</label>
          </div>
        </div>
      </div>

      <div class="row col mb-2 align-items-center" v-if="mStoreBoardGroup.menu_visible === 'Y'">
        <label class="col-lg-1 col-form-label">노출타입</label>
        <div class="col-lg-3">
          <div class="tom-select-custom">
            <select class="form-select" v-model="mStoreBoardGroup.view_type" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option value="">노출타입을 선택해 주세요.</option>
              <option value="banner">배너</option>
              <option value="thumbnail">썸네일</option>
            </select>
          </div>
        </div>
      </div>

      <div class="row col mb-2 align-items-center">
        <label class="col-lg-1 col-form-label"
          >기간지난<br class="d-none d-md-block d-lg-none" />
          컨텐츠<br class="d-none d-md-block d-lg-none" />
          노출여부</label
        >
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_view_end_content_y" type="radio" class="form-check-input" name="radio_view_end_content" value="Y" v-model="mStoreBoardGroup.view_end_content" />
            <label class="form-check-label" for="radio_view_end_content_y">노출</label>
          </div>
        </div>
        <div class="col-auto">
          <div class="form-check form-check-inline">
            <input id="radio_view_end_content_n" type="radio" class="form-check-input" name="radio_view_end_content" value="N" v-model="mStoreBoardGroup.view_end_content" />
            <label class="form-check-label" for="radio_view_end_content_n">비노출</label>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="card mt-2">
    <div class="card-header">
      <div class="text-end">
        <router-link :to="{ path: `/store/detail/board/detail`, state: { code: storeCode, groupId: groupId } }">
          <button type="button" class="btn btn-sm btn-info">신규 {{ groupName }} 생성</button></router-link
        >
      </div>
    </div>
    <div class="card-body">
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2 align-items-center">
        <label for="idLabel" class="col-md-1 col-form-label">검색기간<br />(등록일)</label>
        <div class="col">
          <div class="row">
            <div class="col-lg-3">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange" v-model="searchCondition.date.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col-lg-3">
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
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange" v-model="searchCondition.date.eDate" />
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
      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-lg-1 col-form-label">세부검색</label>
        <div class="col-lg-2 mb-1">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col-lg-4">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getStoreBoardList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStoreBoardList">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mStoreBoardList.total > 0">총 : {{ mStoreBoardList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th>제목</th>
          <th style="width: 20%">이미지</th>
          <th style="width: 10%">이벤트 시작일/종료일</th>
          <th style="width: 10%">노출 시작일/종료일</th>
          <th style="width: 5%">우선순위</th>
          <th style="width: 10%">작성일</th>
          <th style="width: 5%">상위고정</th>
          <th style="width: 5%">상세</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(item, i) in mStoreBoardList.datas" :key="item.id">
          <td>{{ item.title }}</td>
          <td>
            <div class="avatar" v-if="item.image">
              <img class="avatar-img" :src="item.image" alt="Image Description" @click.prevent="openImgModal(item.image)" />
            </div>
            <div class="avatar" v-else>
              <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
            </div>
          </td>
          <td>{{ item.view_start_date ? dateTimeFormatConverter(item.start_date) : '-' }}<br />{{ item.view_end_date ? dateTimeFormatConverter(item.end_date) : '-' }}</td>
          <td>{{ item.view_start_date ? dateTimeFormatConverter(item.view_start_date) : '-' }}<br />{{ item.view_end_date ? dateTimeFormatConverter(item.view_end_date) : '-' }}</td>
          <td>{{ item.sort }}</td>
          <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
          <td>{{ item.pin === 'Y' ? '고정' : '-' }}</td>
          <td>
            <router-link
              :to="{
                path: `/store/detail/board/detail`,
                state: { code: storeCode, boardId: item.id, mStoreBoard: JSON.stringify(item), groupId: groupId, groupName: groupName, storeGroup: storeGroup },
              }">
              <button type="button" class="btn btn-sm btn-success">상세</button>
            </router-link>
          </td>
        </tr>
        <tr class="text-center" v-if="mStoreBoardList.total === 0">
          <td colspan="8">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mStoreBoardList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
  <OpenImgModal :id="'openImgModal'" :openImgUrl="openImgUrl" />
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import apis from '@/apis';
import Pagination from '@/components/comm/Pagination.vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { Board, BoardListInfo } from 'StoreBoardInfoModule';
import OpenImgModal from '@/components/modals/img/OpenImgModal.vue';
import type { BoardGroup } from 'StoreBoardGroupInfoModule';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore2 } from '@/stores/search2';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';

const router = useRouter();
const route = useRoute();
const isChangeDate = ref(true);
const storeCode = ref();
const mStoreBoardList = ref({} as BoardListInfo);
const mStoreBoardGroup = ref({} as BoardGroup);
const mOriginStoreBoardGroup = ref({} as BoardGroup);
const groupId = ref();
const groupName = ref('');
const storeGroup = ref();

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mStoreBoardList.value.total / limit.value));

const isView = (sDate: string, eDate: string) => {
  const viewSdate = new Date(sDate);
  const viewEdate = new Date(eDate);
  const nowDate = new Date();

  if (nowDate > viewSdate && nowDate < viewEdate) {
    return '진행중';
  } else {
    return '-';
  }
};

const changeViewType = () => {
  mStoreBoardGroup.value.view_type = '';
};

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreBoardList();
};

const openImgUrl = ref('');

const searchCondition = reactive({
  date: {
    sDate: '',
    eDate: '',
  },
});
const selDetailSearch = reactive({
  items: [{ name: '제목', value: 'title' }],
  selectedItem: 'title',
  q: '',
  placeholder: '검색할 이벤트의 제목을 입력해주세요.',
});

onMounted(() => {
  const code = history.state.code;
  limit.value = useCommonStore().getLimit;
  if (code) {
    storeCode.value = code;
    groupId.value = history.state.groupId;
    groupName.value = history.state.groupName;
    storeGroup.value = history.state.storeGroup;
    setSearchPeriod('all');
    getSearchInfo();
    getStoreBoardList();
    getStoreBoardGroupList();
  } else {
    showAlert('비정상적인 접근입니다.');
    useRouter().back();
  }
});

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreBoardList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'title':
      selDetailSearch.placeholder = '검색할 게시판의 제목을 입력해주세요.';
      break;
  }
};

const clearSearchCondition = () => {
  setSearchPeriod('all');
  selDetailSearch.selectedItem = 'title';
  selDetailSearch.q = '';
  getStoreBoardList();
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

const openImgModal = (src: string) => {
  openImgUrl.value = src;
  showModal('openImgModal');
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}`;
  useSearchStore2().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  if (useSearchStore2().getSearchInfo) {
    const paramsArray = JSON.parse(JSON.stringify(useSearchStore2().getSearchInfo)).split('&');

    for (const param of paramsArray) {
      const [key, value] = param.split('=');

      switch (key) {
        case 's_reg_date':
          searchCondition.date.sDate = value;
          break;
        case 'e_reg_date':
          searchCondition.date.eDate = value;
          break;
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        case 'title':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        default:
          break;
      }
    }
  }
};
/** */

const getStoreBoardList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  //검색기간
  if (searchCondition.date.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchCondition.date.sDate}` : `s_reg_date=${searchCondition.date.sDate}`);
  }
  //검색기간
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

  apis.store.get_store_board_list(storeCode.value, groupId.value, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mStoreBoardList.value.total = res.total;
      mStoreBoardList.value.datas = res.datas;
    });
  });
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

const getStoreBoardGroupList = () => {
  apis.store.get_store_board_group_list(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      for (let value of res.datas) {
        if (value.id === groupId.value) {
          mStoreBoardGroup.value.menu_visible = value.menu_visible;
          mStoreBoardGroup.value.view_type = value.view_type;
          mStoreBoardGroup.value.view_end_content = value.view_end_content;

          mOriginStoreBoardGroup.value.menu_visible = value.menu_visible;
          mOriginStoreBoardGroup.value.view_type = value.view_type;
          mOriginStoreBoardGroup.value.view_end_content = value.view_end_content;
          break;
        }
      }
    });
  });
};

const checkIsChange = () => {
  if (mStoreBoardGroup.value.menu_visible !== mOriginStoreBoardGroup.value.menu_visible) return true;
  if (mStoreBoardGroup.value.menu_visible === 'Y' && mStoreBoardGroup.value.view_type !== mOriginStoreBoardGroup.value.view_type) return true;
  if (mStoreBoardGroup.value.view_end_content !== mOriginStoreBoardGroup.value.view_end_content) return true;
  showAlert('변경된 내용이 없습니다.', 'warning');
  return false;
};

const modStoreBoardGroup = () => {
  if (mStoreBoardGroup.value.menu_visible === 'Y' && mStoreBoardGroup.value.view_type === '') {
    showAlert('노출타입을 선택해주세요.', 'warning');
    return;
  }
  if (!checkIsChange()) return;

  showConfirm('이벤트 설정값을 수정하시겠습니까?', () => {
    apis.store.mod_store_board_group(storeCode.value, groupId.value, mStoreBoardGroup.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('저장되었습니다.', 'success');
        getStoreBoardGroupList();
      });
    });
  });
};
</script>

<style scoped></style>
