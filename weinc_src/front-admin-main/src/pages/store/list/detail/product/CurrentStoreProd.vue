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
      <!-- 상품상태 -->
      <div class="row align-items-center">
        <div class="col-md-2 col-form-label">상품상태</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_status_all" class="form-check-input" name="search_sp_status" v-model="selDetailSearch.status" value="all" />
              <label class="form-check-label px-1" for="search_sp_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_status_y" class="form-check-input" name="search_sp_status" v-model="selDetailSearch.status" value="Y" />
              <label class="form-check-label px-1" for="search_sp_status_y">정상</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_status_p" class="form-check-input" name="search_sp_status" v-model="selDetailSearch.status" value="P" />
              <label class="form-check-label px-1" for="search_sp_status_p">판매종료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_status_s" class="form-check-input" name="search_sp_status" v-model="selDetailSearch.status" value="S" />
              <label class="form-check-label px-1" for="search_sp_status_s">품절</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_status_n" class="form-check-input" name="search_sp_status" v-model="selDetailSearch.status" value="N" />
              <label class="form-check-label px-1" for="search_sp_status_n">미승인</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 노출여부 -->
      <div class="row align-items-center">
        <div class="col-md-2 col-form-label">노출여부</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_view_yn_all" class="form-check-input" name="search_sp_view_yn" v-model="selDetailSearch.view_yn" value="all" />
              <label class="form-check-label px-1" for="search_sp_view_yn_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_view_yn_y" class="form-check-input" name="search_sp_view_yn" v-model="selDetailSearch.view_yn" value="Y" />
              <label class="form-check-label px-1" for="search_sp_view_yn_y">노출</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_sp_view_yn_n" class="form-check-input" name="search_sp_view_yn" v-model="selDetailSearch.view_yn" value="N" />
              <label class="form-check-label px-1" for="search_sp_view_yn_n">비노출</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 상품유형 radio -->
      <div class="row align-items-center mb-2">
        <div class="col-md-2 col-form-label">상품유형</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_all" class="form-check-input" name="prod_type" value="all" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_DP" class="form-check-input" name="prod_type" value="DP" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_DP">배송상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_OF" class="form-check-input" name="prod_type" value="UP-OF" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_OF">티켓상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_EC" class="form-check-input" name="prod_type" value="UP-EC" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_EC">E-쿠폰</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 카테고리/브랜드 선택 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">카테고리/브랜드</label>
        <div class="col-md-3 mb-1">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selDetailSearch.cateBrand" @change="onChangeCateBrand" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-text="'카테고리'" value="c"></option>
              <option v-text="'브랜드'" value="b"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
        <div class="col">
          <div class="input-group" v-if="selDetailSearch.cateBrand === 'c'">
            <input type="text" class="form-control" v-model="selDetailSearch.categoryLabel" placeholder="카테고리를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openCategoryModal">검색</button>
          </div>
          <div class="input-group" v-if="selDetailSearch.cateBrand === 'b'">
            <input type="text" class="form-control" v-model="selDetailSearch.brandName" placeholder="브랜드를 선택해주세요." aria-label="" disabled />
            <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('SelBrandModal')">검색</button>
          </div>
        </div>
      </div>
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-md-2 col-form-label">세부검색</label>
        <div class="col-md-3 mb-1">
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
      <div class="col-auto align-items-center mt-2" style="font-size: 0.7rem">
        <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
        <span class="ms-1 me-2">배송상품</span>
        <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
        <span class="ms-1 me-2">티켓상품</span>
        <span class="badge text-bg-success">E</span>
        <span class="ms-1">E-쿠폰</span>
      </div>
    </div>
    <div class="col-auto">
      <button type="button" class="btn btn-sm btn-danger col-auto" @click.prevent="removeProdToStore">선택상품삭제</button>
    </div>
  </div>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>
  <!-- TODO: 공급가 표시 여부 분기 처리 해야함 [CM,PA / MC] -->
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle">
      <thead class="thead-light">
        <tr class="text-center text-nowrap">
          <th>
            <input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
          </th>
          <th class="px-0">상품유형</th>
          <th>상품코드</th>
          <th>이미지</th>
          <th>상품명</th>
          <th>정상가</th>
          <th>판매가</th>
          <th>노출 / 상태</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(p, i) in mProductList.datas" :key="p.id">
          <td>
            <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${p.id}`" :value="p" v-model="mSelProductList" />
          </td>
          <td style="font-size: 0.6rem">
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
          <td style="font-size: 0.6rem">
            {{ p.product.code }}
          </td>
          <td>
            <div class="avatar" v-if="p.product.photos.length > 0">
              <img class="avatar-img" :src="p.product.photos[0].uri" alt="Image Description" />
            </div>
            <div class="avatar" v-if="p.product.photos.length === 0">
              <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
            </div>
          </td>
          <td class="px-0 text-wrap" style="font-size: 0.8rem">{{ p.product.name }}</td>
          <td class="text-end text-nowrap" style="font-size: 0.8rem">{{ getPriceInfo(p.product.options, p.variation, 'origin') }}</td>
          <td class="text-end text-nowrap" style="font-size: 0.8rem">{{ getPriceInfo(p.product.options, p.variation, 'sell') }}</td>
          <td class="text-nowrap" style="font-size: 0.7rem">{{ p.product.view_yn === 'Y' ? '노출' : '비노출' }} / {{ p.product.status === 'Y' ? '정상' : p.product.status === 'P' ? '판매중지' : p.product.status === 'S' ? '품절' : '미승인' }}</td>
        </tr>
        <tr class="text-center" v-if="mProductList.total === 0">
          <td colspan="9">검색 결과가 없습니다.</td>
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
  <Modal :id="'SelCategoryModal'" :title="'카테고리 선택'">
    <template #body>
      <SelectCategoryModal @closeModal="closeCategoryModal" ref="CategoryModal" />
    </template>
  </Modal>

  <!-- 브랜드 선택-->
  <Modal :id="'SelBrandModal'" :title="'브랜드 선택'">
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
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import Modal from '@/components/comm/modal.vue';
import SelectCategoryModal from '@/components/modals/product/SelectCategoryModal.vue';
import SelectBrandModal from '@/components/modals/product/SelectBrandModal.vue';

const storeCode = ref();
const CategoryModal = ref();
const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품의 이름을 입력해주세요.',
  type: 'all',
  cateBrand: 'c',
  categoryId: 0,
  categoryLabel: '',
  brandId: 0,
  brandName: '',
  status: 'all',
  view_yn: 'all',
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

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getProductList();
};

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

const getPriceInfo = (opts: Opt[], variation: number, type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
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
  showModal('SelCategoryModal');
  CategoryModal.value.openModal();
};

const closeCategoryModal = (cateId: number, cateLabel: string) => {
  hideModal('SelCategoryModal');
  selDetailSearch.categoryId = cateId;
  selDetailSearch.categoryLabel = cateLabel;
};

const closeBrandModal = (brandId: number, brandName: string) => {
  hideModal('SelBrandModal');
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
  selDetailSearch.status = 'all';
  selDetailSearch.view_yn = 'all';
  selCatalogSearch.selectedItem = 0;
  onChangeDetailSearch();
  getProductList();
};

const getProductList = (reset: boolean = true) => {
  if (reset) {
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

  if (selDetailSearch.status !== 'all') {
    query = query.concat(query ? `&status=${selDetailSearch.status}` : `status=${selDetailSearch.status}`);
  }

  if (selDetailSearch.view_yn !== 'all') {
    query = query.concat(query ? `&view_yn=${selDetailSearch.view_yn}` : `view_yn=${selDetailSearch.view_yn}`);
  }

  if (selCatalogSearch.selectedItem) {
    query = query.concat(query ? `&catalog_id=${selCatalogSearch.selectedItem}` : `catalog_id=${selCatalogSearch.selectedItem}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_store_prod_list(query, storeCode.value, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
    });
  });
};

const removeProdToStore = () => {
  if (mSelProductList.value.length === 0) {
    showAlert('선택한 상품이 없습니다.', 'warning');
    return;
  }

  //@ts-ignore
  const arrProdId: number[] = [];
  // @ts-ignore
  mSelProductList.value.map(item => arrProdId.push(item.product.id));
  showConfirm('선택한 상품을 상점에서 삭제하시겠습니까?', () => {
    apis.store.delete_prod_to_store(storeCode.value, arrProdId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상점에서 삭제되었습니다.', 'success');
        // page_no.value = 1;
        mSelProductList.value = [];
        page_no.value > 1 ? getProductList(false) : getProductList();
      });
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProductList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const refreshStoreProdList = () => {
  page_no.value > 1 ? getProductList(false) : getProductList();
};

onMounted(() => {
  storeCode.value = history.state.code;
  limit.value = useCommonStore().getLimit;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }
  page_no.value > 1 ? getProductList(false) : getProductList();
  getCatalogList();
});

defineExpose({ refreshStoreProdList });
</script>

<style scoped></style>
