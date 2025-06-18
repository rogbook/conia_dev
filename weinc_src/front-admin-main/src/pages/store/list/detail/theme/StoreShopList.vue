<template>
  <div class="card">
    <div class="card-header py-3 text-black h4">상점에 존재하는 매장</div>
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">세부검색</label>
        <div class="col-md-3">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getShopList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getShopList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mShopList.total > 0">총 : {{ mShopList.total }}개</span>
    </div>
  </div>
  <!-- TODO: 공급가 표시 여부 분기 처리 해야함 [CM,PA / MC] -->
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th>매장명</th>
          <th>이미지</th>
          <th>운영자</th>
          <th>운영자 이메일</th>
          <th>선택</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(s, i) in mShopList.datas" :key="s.id">
          <td>
            {{ s.name }}
          </td>
          <td>
            <img v-if="s.image" :src="s.image" style="max-height: 2rem" />
            <img v-else src="@/assets/images/layers.png" style="max-height: 2rem" />
          </td>
          <td>{{ s.member.name }}</td>
          <td>{{ s.member.email }}</td>
          <td>
            <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectProduct(s.id, s.name, s.image)">선택</button>
          </td>
        </tr>
        <tr class="text-center" v-if="mShopList.total === 0">
          <td colspan="5">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mShopList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import type { StoreShopList, Shop } from 'StoreShopListModule';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';

const storeCode = ref();

const selDetailSearch = reactive({
  items: [{ name: '매장명', value: 'name' }],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 매장의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 매장의 이름을 입력해주세요.';
      break;
  }
};
// 매장 리스트
const mShopList = ref({} as StoreShopList);
// 선택 매장 리스트 (담은 매장)
const mSelShopList = ref([]);

const allCheck = ref(false);
// checkbox
const allCheckedClick = () => {
  // allCheck.value ? mProductList.value.list.map(item => checkList.value.add(item)) : mProductList.value.list.map(item => checkList.value.delete(item));
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mShopList.value.total / limit.value));

const getShopList = (init: boolean = true) => {
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

  apis.store.get_store_shop(storeCode.value, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      allCheck.value = false;
      mShopList.value.total = res.total;
      mShopList.value.datas = res.datas;
      showLogConsole(res.datas);
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getShopList(false);
};

const emit = defineEmits(['passToShop']);
const selectProduct = (id: number, name: string, photo: string) => {
  emit('passToShop', id, name, photo);
};

onMounted(() => {
  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    return;
  }
  getShopList();
});
</script>

<style scoped></style>
