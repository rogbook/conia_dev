<template>
  <div class="card">
    <div class="card-header py-3 text-black h4">상점 - 추가 가능 매장</div>
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-lg-2 col-form-label">세부검색</label>
        <div class="col-lg-3 mb-1">
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getStoreShopList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getStoreShopList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mShopList.total > 0">총 : {{ mShopList.total }}개</span>
    </div>
    <div class="col-auto text-end">
      <button type="button" class="btn btn-sm btn-success col-auto mb-2" @click.prevent="addShopToTheme">선택매장추가</button>
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table">
      <thead class="thead-light">
        <tr class="text-center">
          <th>
            <input type="checkbox" class="form-check-input" name="cb_add_store" id="cb_s_all" v-model="allCheck" @change="allCheckedClick" />
          </th>
          <th>매장명</th>
          <th>이미지</th>
          <th>매장설명</th>
          <th>영업시간</th>
          <th>연락처</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="s in mShopList.datas" :key="s.id">
          <td>
            <input type="checkbox" class="form-check-input" name="cb_add_shop" v-bind:id="`cb_s_${s.id}`" :value="s" v-model="mSelShopList" />
          </td>
          <td>
            {{ s.name }}
          </td>
          <td>
            <img v-if="s.image" :src="s.image" style="max-height: 2rem" />
            <img v-else src="@/assets/images/layers.png" style="max-height: 2rem" />
          </td>
          <td>
            {{ s.description }}
          </td>
          <td>{{ s.work_time }}</td>
          <td>{{ s.tel }}</td>
        </tr>
        <tr class="text-center" v-if="mShopList.total === 0">
          <td colspan="6">검색 결과가 없습니다.</td>
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
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const props = defineProps({
  themeId: {
    type: Number,
    required: true,
  },
});
const storeCode = ref();

const emit = defineEmits(['addShopToThemeDone']);

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
// 상품 리스트
const mShopList = ref({} as StoreShopList);
// 선택 상품 리스트 (담은 상품)
const mSelShopList = ref([]);

const allCheck = ref(false);
// checkbox
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelShopList.value = [...mShopList.value.datas];
  } else {
    mSelShopList.value = [];
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mShopList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getStoreShopList();
};

const getStoreShopList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  allCheck.value = false;
  mSelShopList.value = [];
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
    });
  });
};

const addShopToTheme = () => {
  if (mSelShopList.value.length === 0) {
    showAlert('선택한 매장이 없습니다.', 'warning');
    return;
  }

  //@ts-ignore
  const arrShopId: number[] = [];
  // @ts-ignore
  mSelShopList.value.map(item => arrShopId.push(item.id));

  showConfirm('선택한 매장을 테마에 추가하시겠습니까?', () => {
    apis.store.add_link_theme_shop(storeCode.value, props.themeId, arrShopId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('테마에 추가되었습니다.', 'success');
        page_no.value = 1;
        mSelShopList.value = [];
        // getProductList();
        emit('addShopToThemeDone');
      });
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getStoreShopList(false);
};

onMounted(() => {
  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
  }
  getStoreShopList();
});
</script>

<style scoped></style>
