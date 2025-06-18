<template>
  <div class="card">
    <div class="card-header py-3 text-black h4">테마에 추가된 상품</div>
    <div class="card-body">
      <!-- 상품상태 -->
      <div class="row align-items-center">
        <div class="col-md-2 col-form-label">상품상태</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_status_all" class="form-check-input" name="search_tp_status" v-model="selDetailSearch.status" value="all" />
              <label class="form-check-label px-1" for="search_tp_status_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_status_y" class="form-check-input" name="search_tp_status" v-model="selDetailSearch.status" value="Y" />
              <label class="form-check-label px-1" for="search_tp_status_y">정상</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_status_p" class="form-check-input" name="search_tp_status" v-model="selDetailSearch.status" value="P" />
              <label class="form-check-label px-1" for="search_tp_status_p">판매종료</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_status_s" class="form-check-input" name="search_tp_status" v-model="selDetailSearch.status" value="S" />
              <label class="form-check-label px-1" for="search_tp_status_s">품절</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_status_n" class="form-check-input" name="search_tp_status" v-model="selDetailSearch.status" value="N" />
              <label class="form-check-label px-1" for="search_tp_status_n">미승인</label>
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
              <input type="radio" id="search_tp_view_yn_all" class="form-check-input" name="search_tp_view_yn" v-model="selDetailSearch.view_yn" value="all" />
              <label class="form-check-label px-1" for="search_tp_view_yn_all">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_view_yn_y" class="form-check-input" name="search_tp_view_yn" v-model="selDetailSearch.view_yn" value="Y" />
              <label class="form-check-label px-1" for="search_tp_view_yn_y">노출</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="search_tp_view_yn_n" class="form-check-input" name="search_tp_view_yn" v-model="selDetailSearch.view_yn" value="N" />
              <label class="form-check-label px-1" for="search_tp_view_yn_n">비노출</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 상품유형 radio -->
      <div class="row align-items-center mb-2">
        <div class="col-lg-2 col-form-label">상품유형</div>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_all_c" class="form-check-input" name="prod_type_t" value="all" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_all_c">전체</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_DP_c" class="form-check-input" name="prod_type_t" value="DP" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_DP_c">배송상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_OF_c" class="form-check-input" name="prod_type_t" value="UP_OF" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_OF_c">티켓상품</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input type="radio" id="radio_prod_type_UP_EC_c" class="form-check-input" name="prod_type" value="UP-EC" v-model="selDetailSearch.type" />
              <label class="form-check-label px-1" for="radio_prod_type_UP_EC_c">E-쿠폰</label>
            </div>
          </div>
        </div>
      </div>
      <!-- 카테고리/브랜드 선택 -->
      <div class="row col mb-2">
        <label class="col-lg-2 col-form-label">카테고리/브랜드</label>
        <div class="col-lg-3 mb-1">
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
            <button type="button" class="btn btn-outline-secondary" @click.prevent="openBrandModal">검색</button>
          </div>
        </div>
      </div>
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-lg-2 col-form-label">세부검색</label>
        <div class="col-lg-3 mb-1">
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getThemeProductList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getThemeProductList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto"></div>
    <div class="col-auto">
      <button type="button" class="btn btn-sm btn-danger col-auto" @click.prevent="deleteProdToTheme">선택상품삭제</button>
    </div>
  </div>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="cProductList.total > 0">총 : {{ cProductList.total }}개</span>
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
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <!-- TODO: 공급가 표시 여부 분기 처리 해야함 [CM,PA / MC] -->
  <table class="table table-borderless table-thead-bordered table-align-middle card-table">
    <thead class="thead-light">
      <tr class="text-center text-nowrap">
        <th>
          <input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
        </th>
        <th>상품유형</th>
        <th>상품코드</th>
        <th>이미지</th>
        <th>상품명</th>
        <th style="width: 12%">정상가</th>
        <th style="width: 12%">판매가</th>
        <th>노출 / 상태</th>
      </tr>
    </thead>
    <tbody>
      <tr class="text-center" v-for="c in cProductList.datas" :key="c.id">
        <td>
          <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${c.code}`" :value="c" v-model="mSelProductList" />
        </td>
        <td style="font-size: 0.7rem">
          <div v-if="c?.type.startsWith('DP')">
            <span class="badge" :style="{ 'background-color': `#9b00ff !important` }">배</span>
          </div>
          <div v-else-if="c?.type === 'UP-OF'">
            <span class="badge" :style="{ 'background-color': `#ff6b00 !important` }">티</span>
          </div>
          <div v-else-if="c?.type === 'UP-EC'">
            <span class="badge text-bg-success">E</span>
          </div>
        </td>
        <td style="font-size: 0.7rem">{{ c.code }}</td>
        <td>
          <img v-if="c.photos.length > 0" :src="c.photos[0].uri" style="max-height: 2rem" />
          <img v-else src="@/assets/images/layers.png" style="max-height: 2rem" />
        </td>
        <td>
          {{ c.name }}
        </td>
        <td>{{ getPriceInfo(c.options, 'origin').toLocaleString() }}원</td>
        <td>{{ getPriceInfo(c.options, 'sell').toLocaleString() }}원</td>
        <td class="text-nowrap" style="font-size: 0.7rem">{{ c.view_yn === 'Y' ? '노출' : '비노출' }} / {{ c.status === 'Y' ? '정상' : c.status === 'P' ? '판매중지' : c.status === 'S' ? '품절' : '미승인' }}</td>
      </tr>
      <tr class="text-center" v-if="cProductList.total === 0">
        <td colspan="8">검색 결과가 없습니다.</td>
      </tr>
    </tbody>
  </table>
  <div class="table-footer-area" v-if="cProductList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRoute, useRouter } from 'vue-router';
import type { ThemeProductList, Option as Opt } from 'ThemeProductListInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

const emits = defineEmits(['openCategoryModal', 'openBrandModal']);
const openCategoryModal = () => {
  emits('openCategoryModal');
};
const openBrandModal = () => {
  emits('openBrandModal');
};
const closeCategoryModal = (cateId: number, cateLabel: string) => {
  selDetailSearch.categoryId = cateId;
  selDetailSearch.categoryLabel = cateLabel;
};
const closeBrandModal = (brandId: number, brandName: string) => {
  selDetailSearch.brandId = brandId;
  selDetailSearch.brandName = brandName;
};

const storeCode = ref();
const props = defineProps({
  themeId: {
    type: Number,
    required: true,
  },
});

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
const cProductList = ref({} as ThemeProductList);
// 선택 상품 리스트 (담은 상품)
const mSelProductList = ref([]);

const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelProductList.value = [...cProductList.value.datas];
  } else {
    mSelProductList.value = [];
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(cProductList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getThemeProductList();
};

const getPriceInfo = (opts: Opt[], type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return defaultOpt.supply_price.toLocaleString();
      case 'origin':
        return defaultOpt.origin_price.toLocaleString();
      case 'sell':
        return defaultOpt.selling_price.toLocaleString();
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
  getThemeProductList();
};

const getThemeProductList = (reset: boolean = true) => {
  if (reset) {
    page_no.value = 1;
  }

  allCheck.value = false;
  mSelProductList.value = [];

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

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_theme_prod_list(storeCode.value, props.themeId, query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
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

const refreshThemeProdList = () => {
  page_no.value > 1 ? getThemeProductList(false) : clearSearchCondition();
};

defineExpose({ refreshThemeProdList, closeCategoryModal, closeBrandModal });

const deleteProdToTheme = () => {
  if (mSelProductList.value.length === 0) {
    showAlert('선택한 상품이 없습니다.', 'warning');
    return;
  }

  //@ts-ignore
  const arrProdId: number[] = [];
  // @ts-ignore
  mSelProductList.value.map(item => arrProdId.push(item.id));
  showConfirm('선택한 상품을 테마에서 삭제하시겠습니까?', () => {
    apis.store.delete_prod_to_theme(storeCode.value, props.themeId, arrProdId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('테마에서 삭제되었습니다.', 'success');
        // page_no.value = 1;
        mSelProductList.value = [];
        page_no.value > 1 ? getThemeProductList(false) : clearSearchCondition();
      });
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getThemeProductList(false);
};

const setModalListener = () => {
  //@ts-ignore
  document.getElementById('setThemeProductModal').addEventListener('show.bs.modal', function (event) {
    page_no.value > 1 ? getThemeProductList(false) : clearSearchCondition();
  });

  //@ts-ignore
  document.getElementById('setThemeProductModal').addEventListener('hide.bs.modal', function (event) {});
};

onMounted(() => {
  storeCode.value = history.state.code;
  limit.value = useCommonStore().getLimit;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
  }
  setModalListener();
});
</script>

<style scoped></style>
