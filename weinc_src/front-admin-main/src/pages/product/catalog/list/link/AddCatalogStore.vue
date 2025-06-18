<template>
  <div class="card">
    <div class="card-header py-2 text-black h4">연결 추가할 상점 선택</div>
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-lg-2 col-form-label">세부검색</label>
        <div class="col-lg-3">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-lg-none mt-1"></div>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getStoreList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStoreList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mStoreList.total > 0">총 : {{ mStoreList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th>선택</th>
          <th>상점명</th>
          <th>상점코드</th>
          <th>운영상태</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="s in mStoreList.datas" :key="JSON.stringify(s)">
          <td>
            <input type="radio" name="cb_add_product" v-bind:id="`cb_p_${s.code}`" :value="s.code" v-model="mSelStore" />
          </td>
          <td>
            {{ s.title }}
          </td>
          <td>{{ s.code }}</td>
          <td>{{ s.status === 'Y' ? '운영중' : s.status === 'R' ? '승인대기중' : '미운영' }}</td>
        </tr>
        <tr class="text-center" v-if="mStoreList.total === 0">
          <td colspan="4">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mStoreList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
    <div class="text-end">
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="addStoreToCatalog">선택상점추가</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import type { StoreList } from 'StoreListInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const catalogId = ref();

const selDetailSearch = reactive({
  items: [
    { name: '상점명', value: 'title' },
    { name: '상점코드', value: 'code' },
  ],
  selectedItem: 'title',
  q: '',
  placeholder: '검색할 상점의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'title':
      selDetailSearch.placeholder = '검색할 상점의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearch.placeholder = '검색할 상점의 코드를 입력해주세요.';
      break;
  }
};
// 상품 리스트
const mStoreList = ref({} as StoreList);
const mSelStore = ref('');

const allCheck = ref(false);
// checkbox
const allCheckedClick = () => {};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mStoreList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreList();
};

const getStoreList = (reset: boolean = true) => {
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

  apis.store.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
      mStoreList.value.total = res.total;
      mStoreList.value.datas = res.datas;
    });
  });
};

const addStoreToCatalog = () => {
  if (!mSelStore.value) {
    showAlert('선택한 상점이 없습니다.', 'warning');
    return;
  }

  showConfirm('선택한 상점을 카탈로그 열람관리목록에 추가하시겠습니까?', () => {
    apis.catalog.add_store_to_catalog(catalogId.value, mSelStore.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('카탈로그 열람관리목록에 추가되었습니다.', 'success');
        page_no.value = 1;
        mSelStore.value = '';
        // getStoreList();
        window.location.reload();
      });
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreList(false);
  window.scrollTo({ top: 100, left: 0 });
};

onMounted(() => {
  catalogId.value = history.state.id;
  limit.value = useCommonStore().getLimit;
  if (catalogId.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }

  page_no.value > 1 ? getStoreList(false) : getStoreList();
});
</script>

<style scoped></style>
