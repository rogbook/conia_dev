<template>
  <PageNavigator :before_link="[]" :current="'공지사항'" />
  <div class="card">
    <div class="card-header">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">공지사항 목록</div>
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

      <div class="table-responsive">
        <table class="table table-align-middle border card-table table-vertical-border-striped table-bordered table-nowrap">
          <thead class="thead-light">
            <tr class="text-center">
              <th>제목</th>
              <th>대상</th>
              <th>표시대상 상점</th>
              <th>등록일</th>
              <th>작성자</th>
              <th>상세</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in noticeList.datas" :key="item.id">
              <td>{{ item.title }}</td>
              <td>{{ convertPartner(item.target) }}</td>
              <td>{{ !item.store_code ? '없음' : item.store?.title }}</td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.member?.name }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/community/notice/detail`, state: { id: item.id } })">상세</button>
              </td>
            </tr>
            <tr v-if="noticeList.total === 0">
              <td colspan="6" class="text-center">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="table-footer-area" v-if="noticeList.total > 0">
        <div class="row" v-if="total_page > 1">
          <Pagination :currentPage="page_no" :totalPages="total_page" :pageChange="pageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { computed, onMounted, ref } from 'vue';
import type { NoticeInfoList } from 'BoardInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showLogConsole, getUserClassStr, convertPartner } from '@/utils/common-utils';
import { useUserStore } from '@/stores/user';
import Pagination from '@/components/comm/Pagination.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import { useCommonStore } from '@/stores/common';
import { useSearchStore } from '@/stores/search';

const router = useRouter();
const route = useRoute();
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const currentTarget = computed(() => {
  return !userClass.value ? 'customer' : userClass.value.includes('CM') ? 'admin' : 'partner';
});

const noticeList = ref({} as NoticeInfoList);
const currentTab = ref('admin');

const page_no = ref(1);
const offset = computed(() => (page_no.value - 1) * limit.value);
const limit = ref(10);
const total_page = computed(() => Math.ceil(noticeList.value.total / limit.value));

const changeLimitData = (setLimitNum: number) => {
  page_no.value = 1;
  limit.value = setLimitNum;
  useCommonStore().setLimit(setLimitNum);
  getNoticeList();
};

const pageChange = (page: number) => {
  page_no.value = page;
  getNoticeList(false);
  window.scrollTo({ top: 100, left: 0 });
};

const conventContents = (data: string): string => {
  const contents = data.replace(/<[^>]*>?/g, '');

  if (contents.length > 150) {
    return contents.slice(0, 150) + '...';
  } else {
    return contents;
  }
};

/** 검색조건 pinia 유지 관련 */
const searchInfo = ref('');
const setSearchInfo = (query: string = '') => {
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
        default:
          break;
      }
    }
  }
};
/** */

const getNoticeList = (init: boolean = true) => {
  if (init) {
    page_no.value = 1;
  }
  if (!currentTarget.value) {
    return;
  }
  let query = `target=${currentTarget.value}&`;

  if (currentTarget.value === 'partner') {
    query = query.concat(`sub_target=${getUserClassStr.value}&`);
  }

  setSearchInfo();

  apis.community.get_notice_list(query, offset.value, limit.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      noticeList.value.datas = res.datas;
      noticeList.value.total = res.total;
    });
  });
};

onMounted(() => {
  limit.value = useCommonStore().getLimit;
  getSearchInfo();
  getNoticeList();
});
</script>

<style scoped></style>
