<template>
  <PageNavigator :before_link="[]" :current="'FAQ 관리'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">FAQ 관리</div>
    </div>
    <div class="card-body">
      <div class="row align-items-center mb-4">
        <div class="tab-area col-md-auto">
          <button type="button" class="btn btn-sm btn-outline-info" :class="{ active: currentTab === 'admin' }" @click.prevent="getFaqList('admin')">관리자</button>
          <button type="button" class="btn btn-sm btn-outline-info ms-2 me-2" :class="{ active: currentTab === 'partner' }" @click.prevent="getFaqList('partner')">파트너</button>
          <button type="button" class="btn btn-sm btn-outline-info" :class="{ active: currentTab === 'customer' }" @click.prevent="getFaqList('customer')">일반회원</button>
        </div>
        <div class="col-md mt-2 text-end">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="router.push('/setting/community/faq/reg')">FAQ 등록</button>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-align-middle border card-table table-vertical-border-striped table-bordered">
          <thead class="thead-light">
            <tr class="text-center">
              <th style="width: 8%">질문분류</th>
              <th style="width: 20%">제목</th>
              <th style="width: 30%">내용</th>
              <th>대상</th>
              <th>표시대상 상점</th>
              <th>등록일</th>
              <th>상세</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in faqList" :key="item.id">
              <td>{{ item.category }}</td>
              <td>{{ item.title }}</td>
              <td>{{ conventContents(item.contents) }}</td>
              <td>{{ item.target === 'admin' ? '관리자' : item.target === 'partner' ? '파트너' : '일반회원' }}</td>
              <td>{{ !item.store_code ? '없음' : item.store?.title }}</td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/setting/community/faq/detail`, state: { id: item.id } })">상세</button>
              </td>
            </tr>
            <tr v-if="faqList.length === 0">
              <td colspan="7" class="text-center">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { computed, onMounted, ref } from 'vue';
import type { FaqInfo } from 'BoardInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';

const faqList = ref([] as FaqInfo[]);

const router = useRouter();

const currentTab = ref('admin');

// const page_no = ref(1);
// const offset = computed(() => (page_no.value - 1) * limit.value);
// const limit = ref(10);
// const total_page = computed(() => Math.ceil(faqList.value.total / limit.value));

const getFaqList = (target: string = '') => {
  let query = '';
  if (target) {
    currentTab.value = target;
    query = query.concat(`target=${target}&`);
  }
  apis.community.get_faq_list(query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      faqList.value = res;
    });
  });
};

const conventContents = (data: string): string => {
  const contents = data.replace(/<[^>]*>?/g, '');

  if (contents.length > 150) {
    return contents.slice(0, 150) + '...';
  } else {
    return contents;
  }
};

onMounted(() => {
  getFaqList('admin');
});
</script>

<style scoped></style>
