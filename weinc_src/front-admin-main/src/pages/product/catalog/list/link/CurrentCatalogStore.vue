<template>
  <div class="card">
    <div class="card-header py-2 text-black h4">연결된 상점 목록</div>
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getCatalogStoreList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getCatalogStoreList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto"></div>
    <div class="col-auto">
      <button type="button" class="btn btn-sm btn-danger col-auto" @click.prevent="removeStoreToCatalog">선택상점제외</button>
    </div>
  </div>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="cStoreList.total > 0">총 : {{ cStoreList.total }}개</span>
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
        <tr class="text-center" v-for="s in cStoreList.datas" :key="s.id">
          <td>
            <input type="radio" name="cb_add_product" v-bind:id="`cb_p_${s.store.code}`" :value="s.store.code" v-model="mSelStore" />
          </td>
          <td>{{ s.store.title }}</td>
          <td>{{ s.store.code }}</td>
          <td>{{ s.store.status === 'Y' ? '운영중' : s.store.status === 'R' ? '승인대기중' : '미운영' }}</td>
        </tr>
        <tr class="text-center" v-if="cStoreList.total === 0">
          <td colspan="4">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="row" v-if="total_page > 1">
    <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChangeC" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import type { CatalogStoreList, Store } from 'CatalogStoreModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
const catalogId = ref();

const cStoreList = ref({} as CatalogStoreList);
// 선택 상품 리스트 (담은 상품)
const mSelStore = ref('');

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(cStoreList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getCatalogStoreList();
};

const selDetailSearch = reactive({
  items: [
    { name: '상점명', value: 'store_name' },
    { name: '상점코드', value: 'store_code' },
  ],
  selectedItem: 'store_name',
  q: '',
  placeholder: '검색할 상점의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'store_name':
      selDetailSearch.placeholder = '검색할 상점의 이름을 입력해주세요.';
      break;
    case 'store_code':
      selDetailSearch.placeholder = '검색할 상점의 코드를 입력해주세요.';
      break;
  }
};

const getCatalogStoreList = (reset: boolean = true) => {
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

  apis.catalog.get_catalog_store(query, catalogId.value, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      if (res.total) {
        cStoreList.value.datas = res.datas;
        cStoreList.value.total = res.total;
      } else {
        cStoreList.value.datas = [];
        cStoreList.value.total = 0;
      }
    });
  });
};

const removeStoreToCatalog = () => {
  if (!mSelStore.value) {
    showAlert('선택한 상점이 없습니다.', 'warning');
    return;
  }

  showConfirm('선택한 상점을 카탈로그 열람관리목록에서 삭제하시겠습니까?', () => {
    apis.catalog.delete_store_to_catalog(catalogId.value, mSelStore.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('카탈로그 열람관리목록에서 삭제되었습니다.', 'success');
        page_no.value = 1;
        mSelStore.value = '';
        getCatalogStoreList();
      });
    });
  });
};

const pageChangeC = (page: number) => {
  page_no.value = page;
  getCatalogStoreList(false);
  window.scrollTo({ top: 100, left: 0 });
};

onMounted(() => {
  catalogId.value = history.state.id;
  limit.value = useCommonStore().getLimit;
  if (catalogId.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }
  page_no.value > 1 ? getCatalogStoreList(false) : getCatalogStoreList();
});
</script>

<style scoped></style>
