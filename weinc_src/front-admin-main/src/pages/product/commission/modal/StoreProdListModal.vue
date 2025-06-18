<template>
  <div>
    <div class="card">
      <div class="card-body">
        <!-- 세부검색어 입력 -->
        <div class="row col">
          <label class="col-1 col-form-label">세부검색</label>
          <div class="col-2">
            <!-- Select -->
            <div class="tom-select-custom">
              <select class="form-select" v-model="selDetailSearch.selectedItem" @change="onChangeDetailSearch" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                <option v-for="detail in selDetailSearch.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
              </select>
            </div>
            <!-- End Select -->
          </div>
          <div class="col-md-4">
            <div class="input-group">
              <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getProducts" />
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer py-2">
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearQuery">초기화</button>

          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProducts">검색</button>
        </div>
      </div>
    </div>

    <span class="divider-center py-4">검색결과</span>
    <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto">
        <span v-if="mProductList.total > 0">총 : {{ mProductList.total }}개</span>
      </div>
    </div>
    <div class="card">
      <div class="table-responsive datatable-custom position-relative">
        <table class="table table-lg table-borderless table-thead-bordered table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>상품코드</th>
              <th>이미지</th>
              <th>상품명</th>
              <th>정상가</th>
              <th>판매가</th>
              <th>선택</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in mProductList.datas" :key="item.id">
              <td>{{ item.product.code }}</td>
              <td>
                <div class="avatar" v-if="item.product.photos?.length > 0">
                  <img class="avatar-img" :src="item.product.photos[0].uri" alt="Image Description" />
                </div>
                <div class="avatar" v-if="item.product.photos?.length === 0">
                  <img class="avatar-img" src="@/assets/images/layers.png" alt="Image Description" />
                </div>
              </td>
              <td>
                <span class="d-block h5 mb-0">{{ item.product.name }}</span>
              </td>

              <td class="text-end" style="font-size: 0.8rem">{{ getPriceInfo(item.product.options, item.variation, 'origin') }}</td>
              <td class="text-end" style="font-size: 0.8rem">{{ getPriceInfo(item.product.options, item.variation, 'sell') }}</td>
              <td>
                <button type="button" @click.prevent="selectProd(item.product)" class="btn btn-info btn-sm">선택</button>
              </td>
            </tr>
            <tr class="text-center" v-if="mProductList.datas?.length === 0">
              <td colspan="6">검색 결과가 없습니다.</td>
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
import { computed, onMounted, type PropType, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import apis from '@/apis';
import Pagination from '@/components/comm/Pagination.vue';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, showLogConsole } from '@/utils/common-utils';
import type { Option as Opt } from 'CatalogProductModule';
import type { StoreProdList, Product } from 'StoreProdListInfoMOdule';

interface StoreInfo {
  code: string;
  title: string;
}

const props = defineProps<{ storeCode: string; storeTitle: string }>();

const emits = defineEmits(['selectProd']);

// 상품 리스트
const mProductList = ref({} as StoreProdList);

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
        return '설정필요';
    }
  } else {
    return '설정필요';
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));

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

const getProducts = (init: boolean = true) => {
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

  apis.store.get_store_prod_list(query, storeInfo.code, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
    });
  });
};

const pageChange = (page: number) => {
  page_no.value = page;
  getProducts(false);
};

const user = useUserStore().user;

const storeInfo = reactive({
  code: '',
  title: '',
});
const clearQuery = () => {
  storeInfo.code = props.storeCode;
  storeInfo.title = props.storeTitle;

  selDetailSearch.q = '';

  getProducts();
};

const selectProd = (prod: Product) => {
  emits('selectProd', prod.id, prod.name);
};

const modalOpened = () => {
  clearQuery();
};

defineExpose({ modalOpened });

onMounted(() => {});
</script>

<style scoped></style>
