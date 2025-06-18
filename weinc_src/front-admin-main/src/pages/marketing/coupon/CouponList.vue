<template>
  <PageNavigator :before_link="[]" :current="'쿠폰관리'" />
  <div class="card">
    <div class="card-header py-2">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">쿠폰관리</div>
        </div>
        <div class="col-auto">
          <div class="text-end">
            <button
              type="submit"
              class="btn btn-info"
              @click.prevent="
                useSearchStore().$reset();
                router.push(`/marketing/coupon/reg`);
              "
              v-if="getUserClassStr.includes('CM') || getUserClassStr.includes('PA')">
              쿠폰생성
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body">
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
            <input type="text" class="form-control" id="q" v-model="selDetailSearch.q" :placeholder="selDetailSearch.placeholder" @keypress.enter.prevent="getCouponList" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-warning me-3" @click.prevent="clearSearchCondition">초기화</button>
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getCouponList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>
  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="couponList.total > 0">총 : {{ couponList.total }}개</span>
    </div>
    <div class="col-auto">
      <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
    </div>
  </div>

  <div class="table-responsive">
    <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table table-nowrap">
      <thead class="thead-light">
        <tr class="text-center">
          <th style="width: 5%">쿠폰번호</th>
          <th style="width: 5%">이미지</th>
          <th style="width: 20%">쿠폰명</th>
          <th>적용대상</th>
          <th style="width: 5%">할인율/할인금액</th>
          <th style="width: 10%">사용기간</th>
          <th style="width: 10%">상세</th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-for="(item, i) in couponList.datas" :key="item.id">
          <td>{{ item.id }}</td>
          <td>
            <div class="avatar" v-if="item.image">
              <img class="img-fluid" :src="item.image" alt="Image Description" @click.prevent="openImgModal(item.image)" />
            </div>
          </td>
          <td>{{ item.name }}</td>
          <td>
            <span v-if="item.target !== 'all'">
              <span v-if="item.product">
                {{ item.product.name }}
                <br />
                <span style="font-size: 0.7rem">
                  (상품코드 : &nbsp;<router-link :to="{ path: '/product/detail', state: { id: item.product.id } }">{{ item.product.code }}</router-link
                  >)
                </span>
              </span>
              <span v-else>
                <span v-if="!item.coupon_target.length"></span>
                <span v-else-if="item.coupon_target[0].product_id"
                  >{{ item.coupon_target[0].product.name }} <span v-if="item.coupon_target.length > 1">외 {{ item.coupon_target.length }}건</span></span
                >
                <span v-else-if="item.coupon_target[0].member_id"
                  >{{ item.coupon_target[0].member.company.name }} <span v-if="item.coupon_target.length > 1">외 {{ item.coupon_target.length }}건</span></span
                >
              </span>
            </span>
            <span v-if="item.target === 'all'">전체상품</span>
          </td>
          <td>
            <span v-if="item.percent">{{ item.percent }}%</span>
            <span v-else-if="item.amount">{{ item.amount.toLocaleString() }}원</span>
          </td>
          <td>
            <span v-if="item.begin_date && item.end_date">
              {{ dateTimeFormatConverter(item.begin_date) }} <br />
              {{ dateTimeFormatConverter(item.end_date) }}
            </span>
            <span v-else-if="item.expire_days">{{ item.expire_days }}일</span>
            <span v-else-if="item.begin_time && item.end_time"
              >{{ item.begin_time }} <br />
              {{ item.end_time }}</span
            >
          </td>
          <td>
            <button type="button" class="btn btn-sm btn-success" @click.prevent="router.push({ name: 'couponDetail', state: { id: item.id } })">상세보기</button>
          </td>
        </tr>
        <tr>
          <td colspan="7" class="text-center" v-if="couponList.total === 0">표시할 항목이 없습니다.</td>
        </tr>
      </tbody>
    </table>
    <div class="table-footer-area" v-if="couponList.total > 0">
      <div class="row" v-if="total_page > 1">
        <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
      </div>
    </div>
  </div>
  <OpenImgModal :id="'openImgModal'" :openImgUrl="openImgUrl" />
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref, watch } from 'vue';
import { getUserClassStr, dateTimeFormatConverter, showAlert, showLogConsole, apiResponseCheck, showModal, hideModal } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useRouter, useRoute } from 'vue-router';
import apis from '@/apis';
import type { CouponList } from 'CouponInfoModule';
import OpenImgModal from '@/components/modals/img/OpenImgModal.vue';
import Pagination from '@/components/comm/Pagination.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const router = useRouter();
const couponList = ref({} as CouponList);
const openImgUrl = ref('');
const openImgModal = (src: string) => {
  openImgUrl.value = src;
  showModal('openImgModal');
};

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(couponList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getCouponList();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getCouponList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const selDetailSearch = reactive({
  items: [{ name: '쿠폰명', value: 'name' }],
  selectedItem: 'name',
  q: '',
  placeholder: '검색할 쿠폰의 이름을 입력해주세요.',
});

const onChangeDetailSearch = () => {
  switch (selDetailSearch.selectedItem) {
    case 'name':
      selDetailSearch.placeholder = '검색할 쿠폰의 이름을 입력해주세요.';
      break;
  }
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string) => {
  searchInfo.value = `${query}page_no=${page_no.value}`;
  useSearchStore().setSearchInfo(searchInfo.value);
};
const getSearchInfo = () => {
  if (useSearchStore().getSearchInfo) {
    const paramsArray = JSON.parse(JSON.stringify(useSearchStore().getSearchInfo)).split('&');

    for (const param of paramsArray) {
      const [key, value] = param.split('=');

      switch (key) {
        case 'page_no':
          page_no.value = parseInt(value);
          break;
        case 'name':
          selDetailSearch.selectedItem = key;
          selDetailSearch.q = value;
          break;
        default:
          break;
      }
    }
  }
};
/** */

const getCouponList = (reset: boolean = true) => {
  if (reset) {
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

  setSearchInfo(query);

  apis.coupon.get_coupon_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      couponList.value.datas = res.datas;
      couponList.value.total = res.total;
    });
  });
};

const clearSearchCondition = () => {
  selDetailSearch.selectedItem = 'name';
  selDetailSearch.q = '';
  getCouponList();
};

onMounted(() => {
  getSearchInfo();
  limit.value = useCommonStore().getLimit;
  page_no.value > 1 ? getCouponList(false) : getCouponList();
});
</script>

<style scoped></style>
