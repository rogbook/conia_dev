<template>
  <div class="card">
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col">
        <label class="col-1 col-form-label">검색</label>
        <div class="col-2">
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
  </div>
  <table class="table table-borderless table-thead-bordered table-align-middle card-table">
    <thead class="thead-light">
      <tr class="text-center">
        <th>상점명</th>
        <th>상점코드</th>
        <th>운영상태</th>
        <th>선택</th>
      </tr>
    </thead>
    <tbody>
      <tr class="text-center" v-for="(s, i) in mStoreList.datas" :key="JSON.stringify(s)">
        <td>
          {{ s.title }}
        </td>
        <td>{{ s.code }}</td>
        <td>{{ s.status === 'Y' ? '운영중' : s.status === 'R' ? '승인대기중' : '미운영' }}</td>
        <td>
          <button type="button" class="btn btn-sm btn-info" @click.prevent="selectStore(s)">{{ '선택' }}</button>
        </td>
      </tr>
      <tr class="text-center" v-if="mStoreList.total === 0">
        <td colspan="4">검색 결과가 없습니다.</td>
      </tr>
    </tbody>
  </table>
  <div class="table-footer-area" v-if="mStoreList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import type { StoreList, Store } from 'StoreListInfoModule';
import apis from '@/apis';
import Pagination from '@/components/comm/Pagination.vue';
import { useRouter } from 'vue-router';
import { apiResponseCheck, getUserClassStr, showLogConsole } from '@/utils/common-utils';

const emits = defineEmits(['selectStore']);

const router = useRouter();
const mStoreList = ref({} as StoreList);

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

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mStoreList.value.total / limit.value));

const getStoreList = (init: boolean = true) => {
  if (init) {
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
      mStoreList.value.total = res.total;
      mStoreList.value.datas = res.datas;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreList(false);
};

const selectStore = (store: Store) => {
  emits('selectStore', store.code, store.title);
};

const modalOpened = () => {
  getStoreList();
};

defineExpose({ modalOpened });

onMounted(() => {
  getStoreList();
});
</script>

<style scoped></style>
