<template>
  <div class="card">
    <div class="card-header py-3 text-black h4">상점에 추가할 상품</div>
    <div class="card-body">
      <!-- 카탈로그 선택 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">카탈로그 선택</label>
        <div class="col-md-4">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" id="sel_catalog" v-model="selCatalogSearch.selectedItem" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "placeholder": "카탈로그를 선택해주세요."}'>
              <option value="0" disabled v-if="selCatalogSearch.items.length > 0">카탈로그를 선택해주세요.</option>
              <option value="-1" disabled v-if="selCatalogSearch.items.length === 0">연결된 카탈로그가 없습니다.</option>
              <option v-for="detail in selCatalogSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.id"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
      </div>
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">세부검색</label>
        <div class="col-md-3">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true, "refreshOptions": true}'>
              <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getCatalogProdList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getCatalogProdList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="cProductList.total > 0">총 : {{ cProductList.total }}개</span>
    </div>
    <div class="col-auto">
      <!-- TODO: 선택상품 담기 Modal 구현해야함. -->
      <button type="button" class="btn btn-sm btn-info col-auto" v-if="false">선택상품담기</button>
    </div>
  </div>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto"></div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <!-- TODO: 공급가 표시 여부 분기 처리 해야함 [CM,PA / MC] -->
  <table class="table table-borderless table-thead-bordered table-align-middle card-table">
    <thead class="thead-light">
      <tr class="text-center">
        <th>상품코드</th>
        <th>이미지</th>
        <th>상품명</th>
        <th v-if="false">정상가</th>
        <th v-if="false">판매가</th>
        <th>선택</th>
      </tr>
    </thead>
    <tbody>
      <tr class="text-center" v-for="c in cProductList.datas" :key="c.id">
        <td>{{ c.product.code }}</td>
        <td>
          <div class="avatar" v-if="c.product.photos.length > 0">
            <img class="avatar-img" :src="c.product.photos[0].uri" alt="Image Description" />
          </div>
          <div class="avatar" v-if="c.product.photos.length === 0">
            <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
          </div>
        </td>
        <td>
          {{ c.product.name }}
        </td>
        <td v-if="false">{{ getPriceInfo(c.product.options, c.variation, 'origin') }}</td>
        <td v-if="false">{{ getPriceInfo(c.product.options, c.variation, 'sell') }}</td>
        <td>
          <button type="button" class="btn btn-sm btn-success" @click.prevent="selectProd(c.product.id, c.product.name)">선택</button>
        </td>
      </tr>
      <tr class="text-center" v-if="cProductList.total === 0">
        <td colspan="6">검색 결과가 없습니다.</td>
      </tr>
    </tbody>
  </table>
  <div class="table-footer-area" v-if="cProductList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
    <div class="text-end">
      <!--    <button type="button" class="btn btn-sm btn-primary" @click="showSelList">담은 상품 보기</button>-->
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import type { CatalogProductList, Option as Opt, Prod } from 'CatalogProductModule';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const props = defineProps<{ storeCode: string }>();
const emits = defineEmits(['selectedProd']);

const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품 이름을 입력해주세요.',
});

const selCatalogSearch = reactive({
  items: [],
  selectedItem: 0,
});

const getCatalogList = () => {
  apis.catalog.get_list(`store_code=${props.storeCode}&`, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      selCatalogSearch.items = res.datas;
      selCatalogSearch.selectedItem = 0;
      if (selCatalogSearch.items.length > 0) {
        // @ts-ignore
        selCatalogSearch.selectedItem = selCatalogSearch.items[0].id;
      } else {
        selCatalogSearch.selectedItem = -1;
        showAlert('연결된 카탈로그가 없습니다.', 'warning');
      }
    });
  });
};

const onChangeCatalog = () => {
  // if (selCatalogSearch.selectedItem <= 0 || selCatalogSearch.selectedItem === undefined) return;
  // getCatalogProdList();
};

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 상품의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearch.placeholder = '검색할 상품의 코드를 입력해주세요.';
      break;
  }
};

// 상품 리스트
const cProductList = ref({} as CatalogProductList);
// 선택 상품 리스트 (담은 상품)
const mSelProductList = ref([]);

const allCheck = ref(false);

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(cProductList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getCatalogProdList();
};

const getPriceInfo = (opts: Opt[], variation: number, type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return defaultOpt.supply_price.toLocaleString();
      case 'origin':
        return defaultOpt.origin_price.toLocaleString();
      case 'sell':
        return defaultOpt.selling_price + variation > 0 ? (defaultOpt.selling_price + variation).toLocaleString() : 0;
      default:
        return '-';
    }
  } else {
    return '-';
  }
};

const getCatalogProdList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  if (selCatalogSearch.selectedItem === undefined || selCatalogSearch.selectedItem <= 0) {
    showAlert('카탈로그를 선택해주세요.', 'warning');
    return;
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

  apis.catalog.get_catalog_prod(query, `${selCatalogSearch.selectedItem}`, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      if (res.total) {
        cProductList.value.datas = res.datas;
        cProductList.value.total = res.total;
      } else {
        cProductList.value.datas = [];
        cProductList.value.total = 0;
      }
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getCatalogProdList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const selectProd = (id: number, name: string) => {
  emits('selectedProd', id, name);
};

const modalOpened = () => {
  selCatalogSearch.selectedItem = 0;
  cProductList.value.datas = [];
  cProductList.value.total = 0;
  getCatalogList();
};

defineExpose({ modalOpened });

onMounted(() => {
  limit.value = useCommonStore().getLimit;
});
</script>

<style scoped></style>
