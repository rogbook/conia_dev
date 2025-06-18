<template>
  <div class="mb-4"><b>[상품준비중]</b>인 상태의 상품 목록을 엑셀다운로드 합니다.</div>
  <button type="button" class="btn btn-sm btn-info" @click.prevent="excelShipDown">송장번호 일괄등록용 엑셀다운로드</button>
</template>

<script setup lang="ts">
import apis from '@/apis';
import { apiResponseCheck } from '@/utils/common-utils';

const excelShipDown = () => {
  const now = new Date();
  apis.order.order_bulk_excel_ship_down().then(res => {
    apiResponseCheck(res, async () => {
      const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `송장번호 일괄등록용-${now.getFullYear()}${now.getMonth() + 1}${now.getDate()}${now.getHours()}${now.getMinutes()}${now.getSeconds()}.xlsx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    });
  });
};
</script>

<style scoped></style>
