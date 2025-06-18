<template>
  <div class="mb-2">송장번호를 기입한 엑셀 파일을 업로드합니다.</div>

  <div class="row col mb-4 align-items-center">
    <div class="col-md-auto">
      <UploadExcel class="form-control" @upload="excelSelect" :btn="{ btnName: '엑셀 파일 선택', btnClass: 'btn btn-sm btn-info' }" />
    </div>
    <div class="col-md-auto mt-1" v-if="uploadFile">파일명 : {{ uploadFile.name }}</div>
  </div>

  <button type="button" class="btn btn-sm btn-danger" @click.prevent="uploadExcelInfo">송장번호 일괄등록 엑셀 업로드</button>
</template>

<script setup lang="ts">
import UploadExcel from '@/components/comm/UploadExcel.vue';
import { onMounted, ref } from 'vue';
import { apiResponseCheck, hideModal, showAlert, showConfirm } from '@/utils/common-utils';
import apis from '@/apis';

const uploadFile = ref(null as File | null);

const excelSelect = (file: File) => {
  console.log(file);
  uploadFile.value = file;
};

const uploadExcelInfo = () => {
  if (!uploadFile.value) {
    showAlert('업로드할 엑셀 파일을 선택해주세요', 'warning');
    return;
  }

  showConfirm('엑셀 파일을 업로드 하시겠습니까?', () => {
    apis.order.order_bulk_excel_ship_upload(uploadFile.value!).then(res => {
      apiResponseCheck(res, () => {
        console.log(res);
        showAlert(`엑셀 파일이 성공적으로 업로드 되었습니다.<br/>송장번호등록 성공건수 : ${res?.count}건`, 'success', () => {
          hideModal('shipExcelModal');
        });
      });
    });
  });
};

const clearInfo = () => {
  uploadFile.value = null;
};

defineExpose({ clearInfo });

onMounted(() => {
  //@ts-ignore
  document.getElementById('shipExcelModal').addEventListener('show.bs.modal', function (event) {
    clearInfo();
  });
});
</script>

<style scoped></style>
