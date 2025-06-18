<template>
  <PageNavigator :before_link="[]" :current="'정산내역 엑셀요청 목록'" />
  <div class="card col-10">
    <div class="card-header py-3">
      <div class="row align-items-center justify-content-between">
        <div class="col-auto">
          <div class="form-control-borderless h2 mb-0">정산내역 엑셀요청 목록</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="row mb-2 align-items-center justify-content-between">
        <div class="col-auto"></div>
        <div class="col-2">
          <!--          <PageLimitCustom v-if="limit" :limit="limit" @changeLimitData="changeLimitData" />-->
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-align-middle border card-table table-vertical-border-striped table-bordered table-nowrap">
          <thead class="thead-light">
            <tr class="text-center">
              <th>정산대상자</th>
              <th>정산기간</th>
              <th>요청일</th>
              <th>요청자</th>
              <th>요청상태</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in mReqList" :key="item.id">
              <td>{{ item.member.name }} (이메일: {{ item.member.email }}, 업체명 : {{ item.member.company?.name ? item.member.company.name : '없음' }})</td>
              <td>{{ item.s_reg_date }} ~ {{ item.e_reg_date }}</td>
              <td>{{ dateTimeFormatConverter(item.reg_date) }}</td>
              <td>{{ item.member1.name }}</td>
              <td>{{ item.file ? '' : convertStatus(item.status) }}<button class="btn btn-sm btn-info p-2" @click.prevent="downloadExcel(item.file)" v-if="item.file">다운로드</button></td>
            </tr>
            <tr v-if="mReqList.length === 0">
              <td colspan="5" class="text-center">표시할 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { apiResponseCheck, dateTimeFormatConverter } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';
import PageLimitCustom from '@/components/comm/PageLimitCustom.vue';
import Pagination from '@/components/comm/Pagination.vue';
import { onMounted, ref } from 'vue';
import apis from '@/apis';
import type { ReqSettlementExcel } from 'SettlementInfoModule';

const mReqList = ref([] as ReqSettlementExcel[]);

const convertStatus = (s: string): string => {
  switch (s) {
    case 'R':
      return '요청중';
    case 'Y':
      return '완료';
    case 'P':
      return '처리중';
    case 'E':
      return '데이터 없음';
    default:
      return '-';
  }
};

const downloadExcel = (file: string) => {
  location.href = file;
};

const getReqList = () => {
  apis.settlement.list_req_settlement_excel().then(res => {
    apiResponseCheck(res, () => {
      mReqList.value = res;
    });
  });
};

onMounted(() => {
  getReqList();
});
</script>

<style scoped></style>
