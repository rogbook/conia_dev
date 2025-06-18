<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'팝업 관리'" />
  <div class="card">
    <div class="card-header">
      <div class="row justify-content-between align-items-center">
        <div class="form-control-borderless h2 col-auto mb-0">팝업 관리</div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-info" @click.prevent="showModal('addPopupModal')">신규 팝업 등록</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-md-1 col-form-label">검색</label>
        <div class="col-md-2 mb-1">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getStorePopupList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStorePopupList">검색</button>
      </div>
    </div>
  </div>
  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mStorePopupList.total > 0">총 : {{ mStorePopupList.total }}개</span>
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
          <th>내용</th>
          <th>이미지</th>
          <th>노출여부</th>
          <th>노출시작시간/노출종료시간</th>
          <th>우선순위</th>
          <th>등록일/수정일</th>
          <th>수정</th>
          <th>삭제</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(p, i) in mStorePopupList.datas" :key="p.id">
          <td>
            {{ p.title }}
          </td>
          <td>
            {{ p.contents }}
          </td>
          <td>
            <div class="avatar" v-if="p.img">
              <img class="avatar-img" :src="p.img" alt="Image Description" @click.prevent="openImgModal(p.img)" />
            </div>
            <div class="avatar" v-else>
              <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
            </div>
          </td>
          <td>
            {{ convertPopupStatus(p.status, p.view_start_date, p.view_end_date) }}
          </td>
          <td>{{ dateTimeFormatConverter(p.view_start_date) }}<br />{{ dateTimeFormatConverter(p.view_end_date) }}</td>
          <td>
            {{ p.sort }}
          </td>
          <td>{{ dateTimeFormatConverter(p.reg_date) }}<br />{{ dateTimeFormatConverter(p.mod_date) }}</td>
          <td>
            <button type="button" class="btn btn-sm btn-warning" @click.prevent="modPopup(i)">수정</button>
          </td>
          <td>
            <button type="button" class="btn btn-sm btn-danger" @click.prevent="deletePopup(i)">삭제</button>
          </td>
        </tr>
        <tr class="text-center" v-if="mStorePopupList.total === 0">
          <td colspan="9">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mStorePopupList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>

  <Modal :id="'addPopupModal'" :title="'팝업 등록/수정'" :xlarge="true">
    <template #body>
      <StoreEventDetail :storeCode="storeCode" :selectedPopup="selectPopup" @closePopupModal="closePopupModal" />
    </template>
  </Modal>

  <OpenImgModal :id="'openImgModal'" :openImgUrl="openImgUrl" />
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import Pagination from '@/components/comm/Pagination.vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import type { Popup, PopupListInfo } from 'StorePopupInfoModule';
import StoreEventDetail from '@/pages/store/list/detail/popup/modal/StoreEventDetail.vue';
import OpenImgModal from '@/components/modals/img/OpenImgModal.vue';
import Modal from '@/components/comm/modal.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const router = useRouter();
const storeCode = ref();
const selectPopup = ref({} as Popup | null);
const mStorePopupList = ref({} as PopupListInfo);

const selDetailSearch = reactive({
  items: [{ name: '제목', value: 'title' }],
  selectedItem: 'title',
  q: '',
  placeholder: '검색할 팝업의 제목을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'title':
      selDetailSearch.placeholder = '검색할 팝업의 제목을 입력해주세요.';
      break;
  }
};

const openImgUrl = ref('');
const openImgModal = (src: string) => {
  openImgUrl.value = src;
  showModal('openImgModal');
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mStorePopupList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStorePopupList();
};

const clearSearchCondition = () => {
  selDetailSearch.selectedItem = 'title';
  selDetailSearch.q = '';
  getStorePopupList();
};

const getStorePopupList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_store_popup_list(storeCode.value, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mStorePopupList.value.total = res.total;
      mStorePopupList.value.datas = res.datas;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStorePopupList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const closePopupModal = () => {
  hideModal('addPopupModal');
  selectPopup.value = null;
  getStorePopupList();
};

const modPopup = (idx: number) => {
  selectPopup.value = mStorePopupList.value.datas[idx];
  setTimeout(() => {
    showModal('addPopupModal');
  }, 100);
};

const deletePopup = (idx: number) => {
  const popup = mStorePopupList.value.datas[idx];
  showConfirm(`[${popup.title}] 팝업을 삭제하시겠습니까?`, () => {
    apis.store.delete_store_popup(storeCode.value, popup.id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('팝업이 삭제되었습니다.', 'success', () => {
          getStorePopupList();
        });
      });
    });
  });
};

const convertPopupStatus = (status: string, start: string, end: string): string => {
  if (status === 'N') return '비노출';
  if (status === 'Y') {
    const today = dateTimeFormatConverter(new Date());
    const s = dateTimeFormatConverter(start);
    const e = dateTimeFormatConverter(end);
    if (today >= s && today <= e) {
      return '노출';
    } else if (today < s && today <= e) {
      return '노출 (대기중)';
    } else if (today > s && today > e) {
      return '노출 (기간만료)';
    }
  }
  return '-';
};
onMounted(() => {
  selectPopup.value = null;
  const code = history.state.code;
  limit.value = useCommonStore().getLimit;
  if (code) {
    storeCode.value = code;
    page_no.value > 1 ? getStorePopupList(false) : getStorePopupList();
  } else {
    showAlert('비정상적인 접근입니다.');
    useRouter().back();
  }

  //@ts-ignore
  document.getElementById('addPopupModal').addEventListener('hide.bs.modal', function (event) {
    selectPopup.value = null;
  });
});
</script>

<style scoped></style>
