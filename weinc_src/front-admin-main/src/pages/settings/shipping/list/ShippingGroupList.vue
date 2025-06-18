<template>
  <PageNavigator :before_link="[]" :current="'배송그룹설정'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">배송그룹 관리</div>
    </div>
    <div class="card-body">
      <div class="text-end mb-3">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="router.push('/setting/shipping/add')">신규 배송그룹 생성</button>
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered">
          <thead class="thead-light">
            <tr class="text-center">
              <th>배송그룹명</th>
              <th v-if="getUserClassStr.includes('CM')">담당자(업체명)</th>
              <th>배송방법</th>
              <th>지불방법</th>
              <th>배송비(기본)</th>
              <th>배송비(추가)</th>
              <th>반품비</th>
              <th>교환비</th>
              <th>상세정보</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(s, i) in shippingList" :key="s.id">
              <td>{{ s.name }}</td>
              <td v-if="getUserClassStr.includes('CM')">{{ `${s.member.name} (${s.member?.company?.name})` }}</td>
              <td>{{ s.type }}</td>
              <td>{{ s.calc_type }}</td>
              <td class="text-end">{{ convertCost(s.shipping_costs, 'basic') }}</td>
              <td class="text-end">{{ convertCost(s.shipping_costs, 'add') }}</td>
              <td class="text-end">{{ s.change_cost.toLocaleString() }}원</td>
              <td class="text-end">{{ s.return_cost.toLocaleString() }}원</td>
              <td>
                <button type="button" class="btn btn-sm btn-info" @click.prevent="router.push({ path: `/setting/shipping/detail`, state: { id: s.id } })">상세보기</button>
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
import type { ShippingCost, ShippingInfo } from 'ShippingInfoModule';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { useRouter } from 'vue-router';
import { apiResponseCheck, getUserClassStr, showLogConsole } from '@/utils/common-utils';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const shippingList = ref([] as ShippingInfo[]);

const convertCost = (costs: ShippingCost[], category: string) => {
  if (costs.length > 0) {
    let cost = '없음';
    for (const c of costs) {
      if (c.category === category) {
        cost = c.cost.toLocaleString() + '원'.toString();
      }
    }
    return cost;
  } else {
    return '설정안함';
  }
};

const getShippingInfoList = () => {
  const query = !getUserClassStr.value.includes('CM') ? `member_id=${useUserStore().user.id}` : '';
  apis.shipping.get_shipping_info_list(query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      shippingList.value = res;
    });
  });
};

onMounted(() => {
  getShippingInfoList();
});
</script>

<style scoped></style>
