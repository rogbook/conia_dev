<template>
  <div class="card">
    <div class="card-header py-3 text-black h4">상점에 구성된 상품</div>
    <div class="card-body">
      <!-- 카탈로그 선택 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label text-nowrap">카탈로그 선택</label>
        <div class="col-md-6">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" id="sel_catalog" v-model="selCatalogSearch.selectedItem" autocomplete="off">
              <option :value="0">카탈로그를 선택해주세요.</option>
              <option v-for="detail in selCatalogSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.id"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
      </div>
      <!-- 상품유형 radio -->
      <div class="row align-items-center mb-2">
        <div class="col-md-2 col-form-label">상품유형</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_all_current" class="form-check-input" name="prod_type" value="all" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_all_current">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_DP_current" class="form-check-input" name="prod_type" value="DP" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_DP_current">배송상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_OF_current" class="form-check-input" name="prod_type" value="UP_OF" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_OF_current">티켓상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_EC_current" class="form-check-input" name="prod_type" value="UP-EC" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_EC_current">E-쿠폰</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 카테고리/브랜드 선택 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">카테고리/브랜드</label>
        <div class="col-md-3">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.cateBrand" @change="onChangeCateBrand" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-text="'카테고리'" value="c"></option>
              <option v-text="'브랜드'" value="b"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col">
          <div class="input-group" v-if="selDetailSearch.cateBrand === 'c'">
            <input type="text" class="form-control" v-model="selDetailSearch.categoryLabel" placeholder="카테고리를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openCategoryModal">검색</button>
          </div>
          <div class="input-group" v-if="selDetailSearch.cateBrand === 'b'">
            <input type="text" class="form-control" v-model="selDetailSearch.brandName" placeholder="브랜드를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openBrandModal">검색</button>
          </div>
        </div>
      </div>
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
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getProductList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProductList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
      <div class="col-auto align-items-center mt-2" style="font-size: 0.7rem">
        <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
        <span class="ms-1 me-2">배송상품</span>
        <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
        <span class="ms-1 me-2">티켓상품</span>
        <span class="badge text-bg-success">E</span>
        <span class="ms-1">E-쿠폰</span>
      </div>
    </div>
  </div>
  <div class="mb-2">
    <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectProducts" v-if="!isMod">체크선택</button>
  </div>
  <!-- TODO: 공급가 표시 여부 분기 처리 해야함 [CM,PA / MC] -->
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle card-table table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th v-if="!isMod">
            <input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
          </th>
          <th style="width: 5%">상품유형</th>
          <th>상품코드</th>
          <th>이미지</th>
          <th>상품명</th>
          <th width="15%">판매가</th>
          <th>선택</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(p, i) in mProductList.datas" :key="p.id">
          <td v-if="!isMod">
            <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${p.id}`" :value="p" v-model="mSelProductList" />
          </td>
          <td style="font-size: 0.7rem">
            <div v-if="p.product.type.startsWith('DP')">
              <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
            </div>
            <div v-else-if="p.product.type === 'UP-OF'">
              <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
            </div>
            <div v-else-if="p.product.type === 'UP-EC'">
              <span class="badge text-bg-success">E</span>
            </div>
          </td>
          <td>
            {{ p.product.code }}
          </td>
          <td>
            <img v-if="p.product.photos.length" :src="p.product.photos[0].uri" style="max-height: 2rem" />
            <img v-else src="@/assets/images/layers.png" style="max-height: 2rem" />
          </td>
          <td>{{ p.product.name }}</td>
          <td class="text-end">{{ getPriceInfo(p.product.options, 'sell', p.variation).toLocaleString() }}</td>
          <td>
            <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectProduct(p.product.id, p.product.name, p.product?.photos[0]?.uri)">선택</button>
          </td>
        </tr>
        <tr class="text-center" v-if="mProductList.total === 0">
          <td :colspan="isMod ? 6 : 7">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mProductList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>

  <!-- 카테고리 선택-->
  <Modal :id="'SelCategoryCurrentModal'" :title="'카테고리 선택'">
    <template #body>
      <SelectCategoryModal @closeModal="closeCategoryModal" ref="CategoryModal" />
    </template>
  </Modal>

  <!-- 브랜드 선택-->
  <Modal :id="'SelBrandCurrentModal'" :title="'브랜드 선택'">
    <template #body>
      <SelectBrandModal @closeModal="closeBrandModal" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import type { StoreProdList, Option as Opt } from 'StoreProdListInfoMOdule';
import { apiResponseCheck, showAlert, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';
import SelectCategoryModal from '@/components/modals/product/SelectCategoryModal.vue';
import SelectBrandModal from '@/components/modals/product/SelectBrandModal.vue';

const storeCode = ref();
const CategoryModal = ref();
const isMod = ref(false);
const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품 이름을 입력해주세요.',
  type: 'all',
  cateBrand: 'c',
  categoryId: 0,
  categoryLabel: '',
  brandId: 0,
  brandName: '',
});

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
const mProductList = ref({} as StoreProdList);
// 선택 상품 리스트 (담은 상품)
const mSelProductList = ref([]);

const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelProductList.value = [...mProductList.value.datas];
  } else {
    mSelProductList.value = [];
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));

const selCatalogSearch = reactive({
  items: [],
  selectedItem: 0,
});
const getCatalogList = () => {
  apis.catalog.get_list(`store_code=${storeCode.value}&`, 0, 100).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      selCatalogSearch.items = res.datas;
    });
  });
};

const getPriceInfo = (opts: Opt[], type: string, variation: number): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return defaultOpt.supply_price.toLocaleString() + '원';
      case 'origin':
        return defaultOpt.origin_price.toLocaleString() + '원';
      case 'sell':
        return (defaultOpt.selling_price + variation).toLocaleString() + '원';
      default:
        return '-';
    }
  } else {
    return '-';
  }
};

const onChangeCateBrand = () => {
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
};

const openCategoryModal = () => {
  showModal('SelCategoryCurrentModal');
  CategoryModal.value.openModal();
};

const openBrandModal = () => {
  showModal('SelBrandCurrentModal');
};

const closeCategoryModal = (cateId: number, cateLabel: string) => {
  hideModal('SelCategoryCurrentModal');
  selDetailSearch.categoryId = cateId;
  selDetailSearch.categoryLabel = cateLabel;
};

const closeBrandModal = (brandId: number, brandName: string) => {
  hideModal('SelBrandCurrentModal');
  selDetailSearch.brandId = brandId;
  selDetailSearch.brandName = brandName;
};

const clearSearchCondition = () => {
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  selDetailSearch.type = 'all';
  selDetailSearch.cateBrand = 'c';
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
  selCatalogSearch.selectedItem = 0;
  onChangeDetailSearch();
  getProductList();
};

const getProductList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }
  // 상품유형
  if (selDetailSearch.type !== 'all') {
    query = query.concat(query ? `&prd_type=${selDetailSearch.type}` : `prd_type=${selDetailSearch.type}`);
  }
  //카테고리 선택 체크
  if (selDetailSearch.categoryId) {
    query = query.concat(query ? `&category=${selDetailSearch.categoryId}&categoryLabel=${selDetailSearch.categoryLabel}` : `category=${selDetailSearch.categoryId}&categoryLabel=${selDetailSearch.categoryLabel}`);
  }
  //브랜드 선택 체크
  if (selDetailSearch.brandId) {
    query = query.concat(query ? `&cateBrand=${selDetailSearch.cateBrand}` : `cateBrand=${selDetailSearch.cateBrand}`);
    query = query.concat(query ? `&brand=${selDetailSearch.brandId}&brandName=${selDetailSearch.brandName}` : `brand=${selDetailSearch.brandId}&brandName=${selDetailSearch.brandName}`);
  }

  if (selCatalogSearch.selectedItem) {
    query = query.concat(query ? `&catalog_id=${selCatalogSearch.selectedItem}` : `catalog_id=${selCatalogSearch.selectedItem}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_store_prod_list(query, storeCode.value, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      allCheck.value = false;
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
      showLogConsole(res.datas);
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProductList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const emit = defineEmits(['passToProduct', 'passToProducts']);
const selectProduct = (id: number, name: string, photo: string | undefined) => {
  emit('passToProduct', id, name, photo);
};

const selectProducts = () => {
  if (!mSelProductList.value.length) {
    showAlert('선택된 상품이 없습니다.', 'warning');
    return;
  }
  emit('passToProducts', mSelProductList.value);
  mSelProductList.value = [];
};

const initialize = () => {
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  getProductList();
  getCatalogList();
};

const setMod = (flag: boolean = false) => {
  isMod.value = flag;
};

defineExpose({ initialize, setMod });

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('getProductListModal').addEventListener('show.bs.modal', function (event) {
    initialize();
  });

  //@ts-ignore
  document.getElementById('getProductListModal').addEventListener('hide.bs.modal', function (event) {
    mSelProductList.value = [];
  });
};

onMounted(() => {
  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    return;
  }
  setModalListener();
});
</script>

<style scoped></style>
