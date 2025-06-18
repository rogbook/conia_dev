<template>
  <div class="card">
    <div class="card-header py-2 text-black h4">상품그룹에 추가할 상품</div>
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getProductList" />
          </div>
        </div>
      </div>
      <!-- 검색기간 Datepicker -->
      <div class="row mb-2">
        <label for="idLabel" class="col-md-2 col-form-label">등록일 기간</label>
        <div class="col">
          <div class="row mb-2">
            <div class="col">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="addStartDatepicker"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#addStartDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="addStartDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange()" v-model="searchDate.sDate" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">-</span>
            <div class="col">
              <!-- Form Group -->
              <div class="form-group">
                <div
                  id="addEndDatepicker"
                  class="js-flatpickr flatpickr-custom input-group"
                  data-hs-flatpickr-options='{
                    "appendTo": "#addEndDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="addEndDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange()" v-model="searchDate.eDate" />
                </div>
              </div>
            </div>
          </div>
          <div class="d-md-none mt-1"></div>
          <div class="row">
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">일주일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">1개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('3month')">3개월</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('6month')">6개월</button>
              <button type="button" class="btn btn-outline-info mb-1" @click.prevent="setSearchPeriod('all')">전체</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProductList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
    </div>
    <div class="col-auto">
      <!-- TODO: 선택상품 담기 Modal 구현해야함. -->
      <button type="button" class="btn btn-sm btn-info col-auto" v-if="false">선택상품담기</button>
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-borderless table-thead-bordered table-align-middle table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th></th>
          <th class="text-nowrap">상품유형</th>
          <th>상품코드</th>
          <th>이미지</th>
          <th>상품명</th>
          <th>공급가</th>
          <th>정상가</th>
          <th>판매가</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="p in mProductList.datas" :key="p.id">
          <td>
            <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${p.code}`" :value="p" v-model="mSelProductList" />
          </td>
          <td class="text-nowrap" style="font-size: 0.8rem">{{ p.type === 'G' ? '그룹' : p.type.startsWith('DP') ? '배송' : '미배송' }}</td>
          <td style="font-size: 0.8rem">
            <router-link :to="{ path: `/product/detail`, state: { id: p.id } }" style="font-size: 0.7rem">{{ p.code }}</router-link>
          </td>
          <td>
            <div class="avatar" v-if="p.photos.length > 0">
              <img class="avatar-img" :src="p.photos[0].uri" alt="Image Description" />
            </div>
            <div class="avatar" v-if="p.photos.length === 0">
              <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
            </div>
          </td>
          <td>{{ p.name }}</td>
          <td>{{ getPriceInfo(p.options, 'supply') }}</td>
          <td>{{ getPriceInfo(p.options, 'origin') }}</td>
          <td>{{ getPriceInfo(p.options, 'sell') }}</td>
        </tr>
        <tr class="text-center" v-if="mProductList.total === 0">
          <td colspan="8">검색 결과가 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="table-footer-area" v-if="mProductList.total > 0">
    <div class="row" v-if="total_page > 1">
      <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
    </div>
    <div class="text-end">
      <!--    <button type="button" class="btn btn-sm btn-primary" @click="showSelList">담은 상품 보기</button>-->
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="addProdToGroup">선택상품추가</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import Pagination from '@/components/comm/Pagination.vue';
import apis from '@/apis';
import type { ProductListInfo, Option as Opt } from 'ProductListInfoModule';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';

const props = defineProps<{ productId: number; paId: number }>();
const emits = defineEmits(['refresh']);
const isChangeDate = ref(true);
const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품의 이름을 입력해주세요.',
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
const mProductList = ref({} as ProductListInfo);
// 선택 상품 리스트 (담은 상품)
const mSelProductList = ref([]);

const allCheck = ref(false);
// checkbox
const allCheckedClick = () => {
  // allCheck.value ? mProductList.value.list.map(item => checkList.value.add(item)) : mProductList.value.list.map(item => checkList.value.delete(item));
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));

const getPriceInfo = (opts: Opt[], type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
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

const getProductList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  query = query.concat(query ? `&member_id=${props.paId}&prod_only=Y` : `member_id=${props.paId}&prod_only=Y`);

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  //검색기간
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `s_reg_date=${searchDate.sDate}`);
  }
  //검색기간
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `e_reg_date=${searchDate.eDate}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.product.getProducts(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
    });
  });
};

const addProdToGroup = () => {
  if (mSelProductList.value.length === 0) {
    showAlert('선택한 상품이 없습니다.', 'warning');
    return;
  }

  //@ts-ignore
  const arrProdId: number[] = [];
  // @ts-ignore
  mSelProductList.value.map(item => arrProdId.push(item.id));
  showConfirm('선택한 상품을 상품그룹에 추가하시겠습니까?', () => {
    apis.product.addProdToGroup(props.productId, arrProdId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품그룹에 추가되었습니다.', 'success');
        page_no.value = 1;
        mSelProductList.value = [];
        getProductList();
        emits('refresh');
      });
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProductList(false);
};

const searchDate = reactive({
  sDate: '',
  eDate: '',
});
const setSearchPeriod = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#addStartDatepickerInput'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#addEndDatepickerInput'), {});
  switch (period) {
    case 'today':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(today, true, 'Y-m-d');
      break;
    case 'week':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 7), true, 'Y-m-d');
      break;
    case 'month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 30), true, 'Y-m-d');
      break;
    case '3month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 90), true, 'Y-m-d');
      break;
    case '6month':
      // @ts-ignore
      efp.setDate(today, true, 'Y-m-d');
      // @ts-ignore
      sfp.setDate(new Date(today.getTime() - 1000 * 60 * 60 * 24 * 180), true, 'Y-m-d');
      break;
    default:
      searchDate.sDate = '';
      searchDate.eDate = '';
      break;
  }
  isChangeDate.value = true;
};
const sDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        sfp.setDate(new Date(eDate), true, 'Y-m-d');
      });
    }
  }
};
const eDateChange = () => {
  if (!isChangeDate.value) return;
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});

  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('검색 종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning', () => {
        // @ts-ignore
        efp.setDate(new Date(sDate), true, 'Y-m-d');
      });
    }
  }
};

watch(
  () => props.paId,
  p => {
    if (p) {
      getProductList();
    }
  },
);

onMounted(() => {
  setSearchPeriod('all');
  if (props.paId) {
    getProductList();
  }
});
</script>

<style scoped></style>
