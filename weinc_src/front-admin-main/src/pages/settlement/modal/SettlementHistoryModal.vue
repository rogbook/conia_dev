<template>
  <div class="card">
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle card-table">
          <thead class="thead-light">
            <tr class="text-center">
              <th>순번</th>
              <th>정산기준금액</th>
              <th>대상</th>
              <th>정산금액</th>
              <th>비율/고정금액</th>
              <th>정산일자</th>
              <th>정산유형</th>
              <th>지급유형</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(h, i) in mHistories.datas" :key="(h, i)">
              <td>{{ h.sequence }}</td>
              <td class="text-end">{{ h.target_amount.toLocaleString() }}원</td>
              <td>{{ h.member.name === '마스터' ? '(주)코니아랩' : h.member.name }} {{ h.member.email === 'master@aconic.co.kr' ? '' : `(${h.member.email})` }}</td>
              <td class="text-end">{{ h.amount.toLocaleString() }}원</td>
              <td>
                {{ h.commission_type === 'P' ? `${h.commission_value}%` : h.commission_value ? `${h.commission_value.toLocaleString()}원` : '-' }}
              </td>
              <td>{{ dateTimeFormatConverter(h.reg_date) }}</td>
              <td>
                {{ convertType(h.type) }}
              </td>
              <td>
                {{ convertPayment(h.payment) }}
              </td>
            </tr>
            <tr>
              <td colspan="3"></td>
              <td class="text-danger text-end">합계 : {{ totalAmount().toLocaleString() }}원</td>
              <td colspan="4"></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import type { Histories, History, Member } from 'SettlementInfoModule';
import apis from '@/apis';
import { apiResponseCheck, dateTimeFormatConverter } from '@/utils/common-utils';

const props = defineProps<{ target: number; kind: string }>();

const mHistories = ref({} as Histories);

const openModal = (id: number, kind: string) => {
  apis.settlement.get_settlement_history(id, kind).then(res => {
    apiResponseCheck(res, () => {
      mHistories.value = res;
      console.log(res);
    });
  });
};

const totalAmount = (): number => {
  let total = 0;
  mHistories.value.datas?.map(item => {
    total += item.amount;
  });
  return total;
};

const convertType = (t: string): string => {
  switch (t) {
    case 'PG':
      return 'PG 수수료';
    case 'SC':
      return '중개수수료';
    case 'S':
      return '공급가';
    case 'MC':
      return '수수료';
    case 'MCC':
      return '중개수수료';
    case 'C':
      return '수수료';
    default:
      return '';
  }
};

const convertPayment = (p: string | null): string => {
  switch (p) {
    case 'S':
      return '분리지급';
    case 'D':
      return '이익차감';
    default:
      return '';
  }
};

defineExpose({ openModal });

const clearInfo = () => {
  mHistories.value = {} as Histories;
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('settlementHistoryModal').addEventListener('hide.bs.modal', function (event) {
    clearInfo();
  });

  //@ts-ignore
  document.getElementById('settlementHistoryModal').addEventListener('show.bs.modal', function (event) {});
});
</script>

<style scoped></style>
