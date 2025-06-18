<template>
  <div class="row mb-4 align-items-center">
    <label class="col-md-1 col-form-label">검색유형</label>
    <div class="col-md-4">
      <div class="row form-control border-0">
        <div class="col-auto form-check form-check-inline">
          <input id="searchMethod_prod" type="radio" class="form-check-input" name="searchMethod" value="prod" v-model="searchMethod" @change="changeSearchType" />
          <label class="form-check-label" for="searchMethod_prod">상품</label>
        </div>
        <div class="col-auto form-check form-check-inline">
          <input id="searchMethod_shop" type="radio" class="form-check-input" name="searchMethod" value="shop" v-model="searchMethod" />
          <label class="form-check-label" for="searchMethod_shop">업체</label>
        </div>
      </div>
    </div>
  </div>
  <div v-if="searchMethod === 'prod'">
    <div class="card">
      <div class="card-body">
        <!-- Modal Search Form -->
        <div class="row col mb-2">
          <label class="col-md-2 col-form-label">공급자(PA)</label>
          <div class="col-md-4">
            <div class="input-group">
              <input type="text" class="form-control" v-model="paInfo.name" placeholder="공급자(PA)를 선택해주세요." aria-label="" disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('selPaModal')" v-if="paInfo.noPa">검색</button>
            </div>
          </div>
        </div>

        <div class="row col mb-2">
          <label class="col-md-2 col-form-label">세부검색</label>
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
          <div class="col-md-5">
            <div class="input-group">
              <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getProducts" />
            </div>
          </div>
        </div>

        <!-- 카테고리/브랜드 선택 -->
        <div class="row col mb-2">
          <label class="col-md-2 col-form-label">카테고리/브랜드</label>
          <div class="col-md-2">
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
          <div class="col-md-5">
            <div class="input-group" v-if="selDetailSearch.cateBrand === 'c'">
              <input type="text" class="form-control" v-model="selDetailSearch.categoryLabel" placeholder="카테고리를 선택해주세요." aria-label="" disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="selCate">검색</button>
            </div>
            <div class="input-group" v-if="selDetailSearch.cateBrand === 'b'">
              <input type="text" class="form-control" v-model="selDetailSearch.brandName" placeholder="브랜드를 선택해주세요." aria-label="" disabled />
              <button type="button" class="btn btn-outline-secondary" @click.prevent="showModal('SelBrandModal')">검색</button>
            </div>
          </div>
        </div>
        <!-- Modal Search Form End -->
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
        <!-- <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" /> -->
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="selectCheckedProd()">체크 선택</button>
      </div>
    </div>

    <!-- prod List Table -->
    <div class="card">
      <div class="table-responsive">
        <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th><input type="checkbox" class="form-check-input" name="cb_add_product" id="cb_p_all" v-model="allCheckProd" @change="allCheckedClickProd" /></th>
              <th>상품코드</th>
              <th>이미지</th>
              <th>상품명</th>
              <th>공급자(PA)</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="item in mProductList.datas" :key="item.id">
              <td>
                <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${item.code}`" :value="item" v-model="mSelProductList" />
              </td>
              <td>
                {{ item?.code }}
              </td>
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
              <td>
                <span class="d-block h5 mb-0">{{ item.member?.company?.name }}</span>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="table-footer-area" v-if="mProductList.total > 0">
          <div class="row" v-if="total_page > 1">
            <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="card">
      <div class="card-body">
        <div class="row align-items-center mb-2">
          <label class="col-md-2 col-form-label">회원타입</label>
          <div class="col form-control border-0">
            <div class="row form-control border-0">
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="radio_type_pa" class="form-check-input" name="search_class_type" value="PA" v-model="checkedTypes" />
                <label class="form-check-label px-1" for="radio_type_pa">PA</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input type="radio" id="radio_type_pa-s" class="form-check-input" name="search_class_type" value="PA-S" v-model="checkedTypes" />
                <label class="form-check-label px-1" for="radio_type_pa-s">PA-S</label>
              </div>
            </div>
          </div>
        </div>
        <div class="row col mb-4">
          <label class="col-md-2 col-form-label">회원검색</label>
          <div class="col-md-2">
            <div class="tom-select-custom">
              <select class="form-select" v-model="selDetailSearch2.selectedItem" @change="onChangeDetailSearch2" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                <option v-for="detail in selDetailSearch2.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
              </select>
            </div>
          </div>
          <div class="d-md-none mt-1"></div>
          <div class="col">
            <div class="input-group">
              <input type="text" class="form-control" id="q" v-model="selDetailSearch2.q" :placeholder="selDetailSearch2.placeholder" />
              <button type="button" class="btn btn-outline-dark col-md-2" @click.prevent="searchUser">검색</button>
            </div>
          </div>
        </div>
      </div>

      <!-- <div class="card-footer py-2">
        <div class="text-end">
          <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="getProducts">검색</button>
        </div>
      </div> -->
    </div>
    <span class="divider-center py-4">검색결과</span>
    <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto">
        <span v-if="searchUserList.data.length > 0">총 : {{ searchUserList.total }}개</span>
      </div>
      <div class="col-auto">
        <!-- <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" /> -->
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="selectPa()">체크 선택</button>
      </div>
    </div>
    <div class="table-responsive">
      <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
        <thead class="thead-light">
          <tr class="text-center">
            <th><input type="checkbox" class="form-check-input" name="cb_add_pa" id="cb_pa_all" v-model="allCheckPa" @change="allCheckedClickPa" /></th>
            <th>회원타입</th>
            <th>사업자명</th>
            <th>이름</th>
            <th>아이디</th>
            <th>휴대전화</th>
          </tr>
        </thead>
        <tbody>
          <tr class="text-center" v-for="(user, i) in searchUserList.data" :key="user.id" style="overflow: scroll">
            <td>
              <input type="checkbox" class="form-check-input" name="cb_add_pa" v-bind:id="`cb_pa_${user.id}`" :value="user" v-model="mSelPaList" />
            </td>
            <td>{{ getUserClass(user.classes) }}</td>
            <td>{{ user?.company?.name ? user?.company?.name : '사업자정보 없음' }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.mobile }}</td>
          </tr>
          <tr>
            <td colspan="6" class="text-center" v-if="searchUserList.data.length === 0">표시할 항목이 없습니다.</td>
          </tr>
        </tbody>
      </table>
      <div class="table-footer-area" v-if="searchUserList.total > 0">
        <div class="row" v-if="user_total_page > 1">
          <Pagination :currentPage="user_page_no" :totalPages="user_total_page" :pageChange="user_pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref } from 'vue';
import type { ProductListInfo, Prod } from 'ProductListInfoModule';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm, showModal } from '@/utils/common-utils';
import Pagination from '@/components/comm/Pagination.vue';
import { useCommonStore } from '@/stores/common';
import type { Class, User } from 'UserInfoModule';

const emits = defineEmits(['selectCheckedProd', 'selectCheckedPa', 'openCateMoal']);

const changeSearchType = () => {
  allCheckPa.value = false;
  allCheckProd.value = false;
  mSelPaList.value = [];
  mSelProductList.value = [];
};

const mSelProductList = ref([]);
const allCheckProd = ref(false);
const allCheckedClickProd = () => {
  if (allCheckProd.value) {
    //@ts-ignore
    mSelProductList.value = [...mProductList.value.datas];
  } else {
    mSelProductList.value = [];
  }
};

const setPaInfo = (id: number, name: string) => {
  paInfo.id = id;
  paInfo.name = name;
};
const setCate = (cateId: number, cateLabel: string) => {
  selDetailSearch.categoryId = cateId;
  selDetailSearch.categoryLabel = cateLabel;
};
const setBrand = (brandId: number, brandName: string) => {
  selDetailSearch.brandId = brandId;
  selDetailSearch.brandName = brandName;
};
defineExpose({ setPaInfo, setCate, setBrand });

const mProductList = ref({} as ProductListInfo);
const searchMethod = ref('prod');
const paInfo = reactive({
  id: 0,
  name: '',
  noPa: true,
});

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProductList.value.total / limit.value));

// PA 회원 목록 페이지네이션
const user_page_no = ref(1);
const user_offset = computed(() => (user_page_no.value - 1) * user_limit.value);
const user_limit = ref(10);
const user_total_page = computed(() => Math.ceil(searchUserList.value.total / user_limit.value));
const user_pageChange = (page: number) => {
  user_page_no.value = page;
  searchUser(false);
};

const selCate = () => {
  emits('openCateMoal');
};

const selDetailSearch = reactive({
  items: [
    { name: '상품명', value: 'name' },
    { name: '상품코드', value: 'code' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 상품의 이름을 입력해주세요.',
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

const pageChange = (page: number) => {
  page_no.value = page;
  getProducts(false);
};

const selectCheckedProd = () => {
  if (mSelProductList.value.length === 0) {
    showAlert('상품을 선택해주세요.', 'warning');
    return;
  }

  emits('selectCheckedProd', mSelProductList.value);
  mSelProductList.value = [];
};

const clearSearchCondition = () => {
  paInfo.id = 0;
  paInfo.name = '';
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  selDetailSearch.cateBrand = 'c';
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
  searchMethod.value = 'prod';
  getProducts();
  searchUser();
};

const onChangeCateBrand = () => {
  selDetailSearch.categoryId = 0;
  selDetailSearch.categoryLabel = '';
  selDetailSearch.brandId = 0;
  selDetailSearch.brandName = '';
};

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getProducts();
};

const getProducts = (init: boolean = true) => {
  allCheckProd.value = false;
  mSelProductList.value = [];
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  if (paInfo.name) {
    query = query.concat(`member_id=${paInfo.id}`);
  }

  // 세부검색어 체크
  if (selDetailSearch.q) {
    const detail = `${selDetailSearch.selectedItem}=${selDetailSearch.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
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

  if (query) {
    query = query.concat('&');
  }

  apis.product.getProducts(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      mProductList.value.total = res.total;
      mProductList.value.datas = res.datas;
    });
  });
};

//

const mSelPaList = ref([]);
const allCheckPa = ref(false);
const allCheckedClickPa = () => {
  if (allCheckPa.value) {
    //@ts-ignore
    mSelPaList.value = [...searchUserList.value.data];
  } else {
    mSelPaList.value = [];
  }
};

const checkedTypes = ref('PA');
const selDetailSearch2 = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
    { name: '회사명', value: 'company_name' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});
const onChangeDetailSearch2 = () => {
  switch (selDetailSearch2.selectedItem) {
    case 'name':
      selDetailSearch2.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearch2.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearch2.placeholder = "검색할 회원의 전화번호를 입력해주세요. ('-' 제외)";
      break;
    case 'compnay_name':
      selDetailSearch2.placeholder = '검색할 회원의 회사명을 입력해주세요.';
      break;
  }
};

const searchUserList = ref({
  data: [] as User[],
  total: 0,
});

const getUserClass = (classes: Class[]): string => {
  const types = [];
  if (classes) {
    for (const c of classes) {
      types.push(c.class_code);
    }
  }
  return types.length == 0 ? '-' : types.join(',');
};

const searchUser = (reset: boolean = true) => {
  if (reset) {
    user_page_no.value = 1;
  }

  allCheckPa.value = false;
  mSelPaList.value = [];

  let query = `class_code=${checkedTypes.value}&status=Y&`;
  // 세부검색어 체크
  if (selDetailSearch2.q) {
    const detail = `${selDetailSearch2.selectedItem}=${selDetailSearch2.q}`;
    if (query) {
      query = query.concat(`&${detail}&`);
    } else {
      query = query.concat(`${detail}&`);
    }
  }
  apis.user.get_list(query, user_offset.value, user_limit.value).then(res => {
    apiResponseCheck(res, () => {
      searchUserList.value.total = res.total;
      searchUserList.value.data = res.datas;
    });
  });
};
const selectPa = () => {
  if (mSelPaList.value.length === 0) {
    showAlert('업체를 선택해주세요.', 'warning');
    return;
  }
  emits('selectCheckedPa', mSelPaList.value);
  mSelPaList.value = [];
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('selProdModal').addEventListener('show.bs.modal', function (event) {
    limit.value = useCommonStore().getLimit;
    user_limit.value = useCommonStore().getLimit;
    clearSearchCondition();
  });
  //@ts-ignore
  document.getElementById('selProdModal').addEventListener('hide.bs.modal', function (event) {
    // clearSearchCondition();
  });
});
</script>
