<template>
  <PageNavigator :before_link="[]" :current="'상품공통정보관리'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">상품공통정보관리</div>
    </div>
    <div class="card-body">
      <div class="text-end mb-3">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="router.push('/setting/product/common/reg')">신규 공통정보 생성</button>
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered">
          <thead class="thead-light">
            <tr class="text-center">
              <th>상품공통정보명</th>
              <th>상품공통정보 내용</th>
              <th>상태</th>
              <th>생성일</th>
              <th>수정일</th>
              <th v-if="getUserClassStr.includes('CM')">사용자여부</th>
              <th>수정</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(c, i) in commonInfoList" :key="c.id">
              <td>{{ c.name }}</td>
              <td class="text-wrap">{{ conventContents(c.contents) }}</td>
              <td>{{ c.status === 'Y' ? '사용' : '사용안함' }}</td>
              <td>{{ dateTimeFormatConverter(c.reg_date) }}</td>
              <td>{{ dateTimeFormatConverter(c.mod_date) }}</td>
              <td v-if="getUserClassStr.includes('CM')">{{ !c.member_id ? '템플릿' : `${c.member.name} (${c.member.company?.name})` }}</td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/setting/product/common/detail`, state: { id: c.id } })">수정</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination -->
      <div class="d-flex justify-content-center justify-content-sm-end">
        <nav id="datatableWithPaginationPagination" aria-label="Activity pagination"></nav>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';
import type { ProdCommonInfo } from 'ProdCommonInfoListModule';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import { useUserStore } from '@/stores/user';

const router = useRouter();

const commonInfoList = ref([] as ProdCommonInfo[]);

const conventContents = (data: string): string => {
  const contents = data.replace(/<[^>]*>?/g, '');

  if (contents.length > 150) {
    return contents.slice(0, 150) + '...';
  } else {
    return contents;
  }
};

const getProdCommonInfo = () => {
  let query = '';
  if (getUserClassStr.value.includes('PA')) {
    query = query.concat(`?member_id=${useUserStore().user.id}`);
  }
  apis.common.get_prod_common_info_list(query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      commonInfoList.value = res;
    });
  });
};

onMounted(() => {
  getProdCommonInfo();
});
</script>

<style scoped></style>
