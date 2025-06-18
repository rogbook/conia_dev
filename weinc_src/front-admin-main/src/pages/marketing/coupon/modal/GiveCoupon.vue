<template>
  <div>
    <div class="text-start mb-4">[{{ props.coupon_name }}] 쿠폰을 발급합니다.</div>
    <div class="card mb-1">
      <div class="card-body">
        <div class="row col align-items-center">
          <label class="col-md-2 col-form-label">쿠폰적용 대상선택</label>
          <div class="col">
            <div class="row form-control border-0">
              <div class="col-auto form-check form-check-inline">
                <input id="type_a" type="radio" class="form-check-input" name="type" value="all" v-model="publishCoupon.type" />
                <label class="form-check-label" for="type_a">모든회원 발급</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input id="type_b" type="radio" class="form-check-input" name="type" value="store" v-model="publishCoupon.type" />
                <label class="form-check-label" for="type_b">특정상점 발급</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <input id="type_c" type="radio" class="form-check-input" name="type" value="customer" v-model="publishCoupon.type" />
                <label class="form-check-label" for="type_c">특정회원 발급</label>
              </div>
              <div class="col-auto form-check form-check-inline">
                <div class="text-end">
                  <button type="submit" class="btn btn-sm btn-primary" @click.prevent="addCoupon">발급하기</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 특정상점 발급 선택시 -->
    <div v-if="publishCoupon.type === 'store'">
      <div class="card">
        <div class="card-body">
          <div class="row col">
            <label class="col-md-2 col-form-label">상점 검색</label>
            <div class="col-md-2">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="selDetailSearchStore.selectedItem" @change="onChangeDetailSearchStore" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option v-for="detail in selDetailSearchStore.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" id="q" v-model="selDetailSearchStore.q" :placeholder="selDetailSearchStore.placeholder" @keypress.enter.prevent="reqStoreList" />
              </div>
            </div>
          </div>
        </div>

        <div class="card-footer py-2">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="clearSearchCondition()">초기화</button>
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqStoreList">검색</button>
          </div>
        </div>
      </div>

      <span class="divider-center py-4">검색결과</span>

      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto">
          <span style="font-size: 0.8rem" class="text-danger ms-1">※ 공개몰은 선택 할 수 없습니다.</span>
        </div>
        <div class="col-auto">
          <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitDataStore" />
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
            <thead class="thead-light">
              <tr class="text-center">
                <th style="width: 5%"></th>
                <th style="width: 40%">상점명</th>
                <th>상점코드</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center" v-for="(item, i) in storeList.datas" :key="JSON.stringify(item)">
                <td>
                  <input v-if="item.type !== 'O'" class="form-check-input" type="radio" name="store" :id="'check' + item.code" :value="item.code" v-model="publishCoupon.store_code" />
                </td>
                <td>
                  <label class="form-check-label" :for="'check' + item.code">
                    {{ item.title }}
                  </label>
                </td>
                <td>
                  {{ item.code }}
                </td>
              </tr>
              <tr>
                <td colspan="3" class="text-center" v-if="storeList.total === 0">표시할 항목이 없습니다.</td>
              </tr>
            </tbody>
          </table>
          <div class="table-footer-area" v-if="storeList.total > 0">
            <div class="row" v-if="store_total_page > 1">
              <Pagination :currentPage="page_no" :totalPages="store_total_page" :pageChange="pageChange" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- End 특정상점 발급 선택시 -->

    <!-- 특정회원 발급 선택시 -->
    <div v-if="publishCoupon.type === 'customer'">
      <div class="card">
        <div class="card-body">
          <div class="row col">
            <label class="col-md-2 col-form-label">회원 검색</label>
            <div class="col-md-2">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="selDetailSearchUser.selectedItem" @change="onChangeDetailSearchUser" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option v-for="detail in selDetailSearchUser.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
                </select>
              </div>
              <!-- End Select -->
            </div>
            <div class="d-md-none mt-1"></div>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" id="q" v-model="selDetailSearchUser.q" :placeholder="selDetailSearchUser.placeholder" @keypress.enter.prevent="reqUserList" />
              </div>
            </div>
          </div>
        </div>

        <div class="card-footer py-2">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-warning me-2" @click.prevent="clearSearchCondition()">초기화</button>
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="reqUserList">검색</button>
          </div>
        </div>
      </div>

      <span class="divider-center py-4">검색결과</span>
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto"></div>
        <div class="col-auto">
          <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitDataUser" />
        </div>
      </div>

      <div class="card">
        <div class="table-responsive">
          <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
            <thead class="thead-light">
              <tr class="text-center">
                <th style="width: 5%">
                  <input class="form-check-input" type="checkbox" name="cb_add_product" id="cb_p_all" v-model="allCheck" @change="allCheckedClick" />
                </th>
                <th style="width: 40%">이름</th>
                <th>아이디</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center" v-for="(item, i) in userList.datas" :key="item.id">
                <td>
                  <input class="form-check-input" type="checkbox" name="customer" :id="'check' + item.id" :value="item.id" v-model="publishCoupon.customer_ids" />
                </td>
                <td>
                  <label class="form-check-label" :for="'check' + item.id">
                    {{ item.name }}
                  </label>
                </td>
                <td>
                  {{ item.email }}
                </td>
              </tr>
              <tr>
                <td colspan="3" class="text-center" v-if="userList.total === 0">표시할 항목이 없습니다.</td>
              </tr>
            </tbody>
          </table>
          <div class="table-footer-area" v-if="userList.total > 0">
            <div class="row" v-if="user_total_page > 1">
              <Pagination :currentPage="page_no" :totalPages="user_total_page" :pageChange="pageChange" />
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- End 특정회원 발급 선택시 -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { StoreList } from 'StoreListInfoModule';
import type { CustomerList } from 'CustomerInfoModule';
import type { ProductListInfo, Prod } from 'ProductListInfoModule';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import Pagination from '@/components/comm/Pagination.vue';
import { useCommonStore } from '@/stores/common';

const props = defineProps<{
  coupon_id: number;
  coupon_name?: string;
}>();
const emits = defineEmits(['closeModal']);

const userList = ref({} as CustomerList);
const storeList = ref({} as StoreList);

interface PublishCoupon {
  type: string;
  store_code: string;
  customer_ids: number[];
}
const publishCoupon = ref<PublishCoupon>({
  type: 'all',
  store_code: '',
  customer_ids: [],
});

const allCheck = ref(false);
const allCheckedClick = () => {
  if (allCheck.value) {
    publishCoupon.value.customer_ids = userList.value.datas.map(el => el.id);
  } else {
    publishCoupon.value.customer_ids = [];
  }
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const store_total_page = computed(() => Math.ceil(storeList.value.total / limit.value));
const user_total_page = computed(() => Math.ceil(userList.value.total / limit.value));

const changeLimitDataStore = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  reqStoreList();
};

const changeLimitDataUser = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  reqUserList();
};

watch(
  () => publishCoupon.value.type,
  () => {
    clearSearchCondition();
  },
);

const clearSearchCondition = () => {
  publishCoupon.value.store_code = '';
  publishCoupon.value.customer_ids = [];
  selDetailSearchStore.selectedItem = 'title';
  selDetailSearchUser.selectedItem = 'name';
  selDetailSearchStore.q = '';
  selDetailSearchUser.q = '';

  if (publishCoupon.value.type === 'store') {
    reqStoreList();
  } else if (publishCoupon.value.type === 'customer') {
    reqUserList();
  }
};

const pageChange = (page: number) => {
  page_no.value = page;
  if (publishCoupon.value.type === 'store') {
    publishCoupon.value.store_code = '';
    reqStoreList(false);
  } else if (publishCoupon.value.type === 'customer') {
    reqUserList(false);
  }
};

const selDetailSearchStore = reactive({
  items: [
    { name: '상점명', value: 'title' },
    { name: '상점코드', value: 'code' },
  ],
  selectedItem: 'title',
  q: '',
  placeholder: '검색할 상점의 이름을 입력해주세요.',
});

const onChangeDetailSearchStore = () => {
  switch (selDetailSearchStore.selectedItem) {
    case 'title':
      selDetailSearchStore.placeholder = '검색할 상점의 이름을 입력해주세요.';
      break;
    case 'code':
      selDetailSearchStore.placeholder = '검색할 상점의 코드를 입력해주세요.';
      break;
  }
};

const selDetailSearchUser = reactive({
  items: [
    { name: '이름', value: 'name' },
    { name: '아이디', value: 'user_id' },
    { name: '전화번호', value: 'mobile' },
  ],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 회원의 이름을 입력해주세요.',
});

const onChangeDetailSearchUser = () => {
  switch (selDetailSearchUser.selectedItem) {
    case 'name':
      selDetailSearchUser.placeholder = '검색할 회원의 이름을 입력해주세요.';
      break;
    case 'user_id':
      selDetailSearchUser.placeholder = '검색할 회원의 아이디(이메일)을 입력해주세요.';
      break;
    case 'mobile':
      selDetailSearchUser.placeholder = "검색할 회원의 전화번호를 입력해주세요. ('-' 제외)";
      break;
  }
};

const setStoreCode = (store_code: string) => {
  publishCoupon.value.store_code = store_code;
};
const setCustomer = (customer_id: number, event: any) => {
  if (event.target.checked) {
    publishCoupon.value.customer_ids.push(customer_id);
  } else {
    const index = publishCoupon.value.customer_ids.indexOf(customer_id);
    if (index !== -1) {
      publishCoupon.value.customer_ids.splice(index, 1);
    }
  }
};

const reqUserList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  // 세부검색어 체크
  if (selDetailSearchUser.q) {
    const detail = `${selDetailSearchUser.selectedItem}=${selDetailSearchUser.q}`;
    query = query.concat(`&${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.customer.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      allCheck.value = false;
      userList.value.datas = res.datas;
      userList.value.total = res.total;
    });
  });
};

const reqStoreList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  // 세부검색어 체크
  if (selDetailSearchStore.q) {
    const detail = `${selDetailSearchStore.selectedItem}=${selDetailSearchStore.q}`;
    query = query.concat(query ? `&${detail}` : `${detail}`);
  }

  if (query) {
    query = query.concat('&');
  }

  apis.store.get_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      storeList.value.total = res.total;
      storeList.value.datas = res.datas;
    });
  });
};
const addCoupon = () => {
  if (!checkValidation()) return;

  showConfirm('쿠폰을 발급하시겠습니까?', () => {
    apis.coupon.add_coupon(props.coupon_id, publishCoupon.value).then(res => {
      apiResponseCheck(
        res,
        () => {
          showLogConsole(res);
          if (res.msg == 'success') {
            showAlert(`${res.count}개의 쿠폰이 정상적으로 발급 되었습니다.`, 'success');
            emits('closeModal');
          }
        },
        (num?: number) => {
          if (num === 403) {
            emits('closeModal');
          }
        },
      );
    });
  });
};

const checkValidation = () => {
  if (publishCoupon.value.type == 'store' && !publishCoupon.value.store_code) {
    showAlert('발급할 상점을 선택해 주세요.', 'warning');
    return;
  }
  if (publishCoupon.value.type == 'customer' && !publishCoupon.value.customer_ids.length) {
    showAlert('발급할 회원을 선택해 주세요.', 'warning');
    return;
  }
  return true;
};
</script>
