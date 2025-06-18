<template>
  <div>
    <div class="card">
      <div class="card-body">
        <!-- 검색기간 Datepicker -->
        <div class="row mb-2 align-items-center">
          <label for="idLabel" class="col-md-1 col-form-label text-nowrap">검색기간<br />(상품등록일)</label>
          <div class="col">
            <div class="row">
              <div class="col-md-3">
                <!-- Form Group -->
                <div class="form-group">
                  <div
                    id="startDatepicker"
                    class="js-flatpickr flatpickr-custom input-group"
                    data-hs-flatpickr-options='{
                    "appendTo": "#startDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                    <div class="input-group-prepend input-group-text" data-bs-toggle>
                      <i class="bi-calendar-week"></i>
                    </div>
                    <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." @change="sDateChange()" v-model="searchDate.sDate" />
                  </div>
                </div>
              </div>
              <span class="col-auto align-items-center">-</span>
              <div class="col-md-3">
                <!-- Form Group -->
                <div class="form-group">
                  <div
                    id="endDatepicker"
                    class="js-flatpickr flatpickr-custom input-group"
                    data-hs-flatpickr-options='{
                    "appendTo": "#endDatepicker",
                    "defaultDate": "today",
                    "dateFormat": "Y-m-d",
                    "wrap": true
                  }'>
                    <div class="input-group-prepend input-group-text" data-bs-toggle>
                      <i class="bi-calendar-week"></i>
                    </div>
                    <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." @change="eDateChange()" v-model="searchDate.eDate" />
                  </div>
                </div>
              </div>
              <div class="d-md-none mt-1"></div>
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
        <!-- 세부검색어 입력 -->
        <div class="row col">
          <label class="col-md-1 col-form-label">세부검색</label>
          <div class="col-md-2">
            <!-- Select -->
            <div class="tom-select-custom">
              <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
              </select>
            </div>
            <!-- End Select -->
          </div>
          <div class="d-md-none mt-1"></div>
          <div class="col-md-4">
            <div class="input-group">
              <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getProducts" />
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer py-2">
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>

          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProducts">검색</button>
        </div>
      </div>
    </div>

    <span class="divider-center py-4">검색결과</span>
    <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto">
        <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
      </div>
      <div class="col-auto">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqSelProd">상품 선택 완료</button>
      </div>
    </div>
    <div class="card">
      <div class="table-responsive datatable-custom position-relative">
        <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>
                <input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
              </th>
              <th>상품코드</th>
              <th>이미지</th>
              <th>상품명</th>
              <th>정상가</th>
              <th>판매가</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="item in mProductList.datas" :key="item.id">
              <td>
                <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${item.code}`" :value="item" v-model="mSelProductList" />
              </td>
              <td>{{ item?.code }}</td>
              <td>
                <div class="avatar" v-if="item.photos.length > 0">
                  <img class="avatar-img" :src="item.photos[0].uri" alt="Image Description" />
                </div>
                <div class="avatar" v-if="item.photos.length === 0">
                  <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
                </div>
              </td>
              <td>
                <span class="d-block h5 mb-0">{{ item.name }}</span>
              </td>
              <td class="text-end">{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'origin') }}</td>
              <td class="text-end">{{ getPriceInfo(JSON.parse(JSON.stringify(item.options)), 'sell') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="mProductList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import type { ProductListInfo } from 'ProductListInfoModule';
import Pagination from '@/components/comm/Pagination.vue';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';
import type { Option as Opt } from 'CatalogProductModule';

const mProductList = ref({} as ProductListInfo);

const mSelProductList = ref([]);
const isChangeDate = ref(true);
const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    //@ts-ignore
    mSelProductList.value = [...mProductList.value.datas];
  } else {
    mSelProductList.value = [];
  }
};

const emits = defineEmits(['selectedProd']);

const getPriceInfo = (opts: Opt[], type: string): string | number => {
  const defaultOpt = opts.find(item => item.default_yn === 'Y' && item.status === 'Y');
  if (defaultOpt) {
    switch (type) {
      case 'supply':
        return defaultOpt.supply_price.toLocaleString() + '원';
      case 'origin':
        return defaultOpt.origin_price.toLocaleString() + '원';
      case 'sell':
        return defaultOpt.selling_price.toLocaleString() + '원';
      default:
        return '-';
    }
  } else {
    return '설정필요';
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));

const searchDate = reactive({
  sDate: '',
  eDate: '',
});

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

const getProducts = (reset: boolean = true) => {
  mSelProductList.value = [];
  if (reset) {
    page_no.value = 1;
  }

  let query = '';

  //검색기간
  if (searchDate.sDate) {
    query = query.concat(query ? `&s_reg_date=${searchDate.sDate}` : `s_reg_date=${searchDate.sDate}`);
  }
  //검색기간
  if (searchDate.eDate) {
    query = query.concat(query ? `&e_reg_date=${searchDate.eDate}` : `e_reg_date=${searchDate.eDate}`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
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

const pageChange = (page: number) => {
  page_no.value = page;
  getProducts(false);
};

const setSearchPeriod = (period: string) => {
  isChangeDate.value = false;
  const today = new Date();
  // @ts-ignore
  const sfp = flatpickr(document.querySelector('#startDatepickerInput'), {});
  // @ts-ignore
  const efp = flatpickr(document.querySelector('#endDatepickerInput'), {});
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

const reqSelProd = () => {
  if (mSelProductList.value.length === 0) {
    showAlert('상품을 선택해주세요.', 'warning');
    return;
  }

  emits('selectedProd', mSelProductList.value);
  mSelProductList.value = [];
};

const clearSearchCondition = () => {
  setSearchPeriod('all');
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  getProducts();
};

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  setSearchPeriod('all');
  page_no.value > 1 ? getProducts(false) : getProducts();

  //@ts-ignore
  document.getElementById('selProdModal').addEventListener('hide.bs.modal', function (event) {
    setSearchPeriod('all');
    selDetailSearch.selectedItem = 'name';
    selDetailSearch.q = '';
    mSelProductList.value = [];
    allCheck.value = false;
  });
});
</script>

<style scoped></style>
