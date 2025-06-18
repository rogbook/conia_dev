<template>
  <div>
    <PageNavigator :before_link="[]" :current="'상품리뷰관리'" />
    <div class="card">
      <div class="card-header">
        <div class="row align-items-center justify-content-between">
          <div class="col-auto">
            <div class="form-control-borderless h2 mb-0">상품리뷰관리</div>
          </div>
        </div>
      </div>

      <div class="card-body">
        <div class="row mb-2 align-items-center justify-content-between">
          <div class="col-auto"></div>
          <div class="col-auto">
            <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />
          </div>
        </div>

        <div class="table-responsive datatable-custom position-relative">
          <table class="table table-lg table-borderless table-thead-bordered table-align-middle card-table table-nowrap">
            <thead class="thead-light">
              <tr class="text-center">
                <th>내용</th>
                <th>상품</th>
                <th>리뷰사진</th>
                <th>작성일시</th>
                <th>작성자</th>
                <th v-if="getUserClassStr.includes('CM')">리뷰삭제</th>
              </tr>
            </thead>
            <tbody>
              <tr class="text-center" v-for="(item, i) in mProdReviewList.datas" :key="item.id">
                <td>{{ item?.contents }}</td>
                <td class="text-center text-wrap p-0">
                  <div class="card-body">
                    <div class="row align-items-center">
                      <div class="col-auto">
                        <img :src="item.product.photos[0].uri" style="width: 50px" />
                      </div>
                      <div class="col text-start">
                        <div class="mb-1">
                          <b>{{ item.product.name }}</b>
                        </div>
                        <div class="" style="font-size: 0.8rem" v-if="!getUserClassStr.includes('MC')">
                          (상품코드 : &nbsp;<router-link :to="{ path: '/product/detail', state: { id: item.product.id } }">{{ item.product.code }}</router-link
                          >)
                        </div>
                        <div class="" style="font-size: 0.8rem" v-else>(상품코드 : &nbsp;{{ item.product.code }})</div>
                      </div>
                    </div>
                  </div>
                </td>
                <td>
                  <img v-if="item.photos[0]" :src="item.photos[0]?.uri" style="width: 50px" />
                </td>
                <td class="text-wrap">
                  {{ dateTimeFormatConverter(item.reg_date) }}
                </td>
                <td>
                  {{ MaskedName(item.customer.name) }}
                </td>
                <td v-if="getUserClassStr.includes('CM')">
                  <!-- TODO: MC가 상품 목록을 검색 시 상품 요청 신청?? -->
                  <button type="button" @click.prevent="deleteReview(item.id)" class="btn btn-sm btn-danger">삭제</button>
                </td>
              </tr>
              <tr v-if="mProdReviewList.total === 0">
                <td class="text-center" colspan="6">표시할 항목이 없습니다.</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="table-footer-area" v-if="mProdReviewList.total > 0">
          <div class="row" v-if="total_page > 1">
            <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
          </div>
        </div>
      </div>
    </div>

    <!-- <div class="row mb-2 align-items-center justify-content-between">
      <div class="col-auto">
        <span v-if="mProdReviewList.total > 0">총 : {{ mProdReviewList.total }}개</span>
      </div>
    </div> -->
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apis from '@/apis';
import Pagination from '@/components/comm/Pagination.vue';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, getUserClassStr, showConfirm, showLogConsole } from '@/utils/common-utils';
import type { ProdReviewList } from 'ProdReviewInfo';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  getPrdReviewList();
});

const mProdReviewList = ref({} as ProdReviewList);
const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(mProdReviewList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getPrdReviewList();
};

const getPrdReviewList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  let query = '';

  if (getUserClassStr.value.includes('PA')) {
    query = query.concat(`member_id=${useUserStore().user.id}`);
  }
  if (getUserClassStr.value.includes('MC')) {
    query = query.concat(query ? `&store_code=${useUserStore().user.store_code}` : `store_code=${useUserStore().user.store_code}`);
  }
  if (query) {
    query = query.concat('&');
  }

  apis.product.getProdReviewList(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mProdReviewList.value.total = res.total;
      mProdReviewList.value.datas = res.datas;
    });
  });
};

const deleteReview = (id: number) => {
  showConfirm('해당 리뷰를 삭제하시겠습니까?', () => {
    apis.product.delProdReview(id).then(res => {
      apiResponseCheck(res, () => {
        showAlert('리뷰가 삭제되었습니다.');
        getPrdReviewList();
      });
    });
  });
};

const MaskedName = (name: string) => {
  const maskedPart = '*'.repeat(name.length - 1);
  return name[0] + maskedPart;
};

const pageChange = (page: number) => {
  page_no.value = page;
  getPrdReviewList(false);
  window.scrollTo({ top: 100, left: 0 });
};
</script>

<style scoped></style>
