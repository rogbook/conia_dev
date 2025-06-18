<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품설명 정보</h4>
          <small>상점에 노출될 상품의 설명 정보를 등록할 수 있습니다.</small><br />
          <span style="font-size: 0.7rem" class="text-danger">등록 이미지 최적화 가로 사이즈 - (가로 873px)</span>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="onRegExplainInfo">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body h-100">
      <CKEditorCustom @receiveData="receiveData" :remove-items="[]" ref="ckeditorCustom" :editorData="editorValue" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import apis from '@/apis';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
const props = defineProps<{ productId: number; contents: string | null }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

const editorValue = ref('');
const ckeditorCustom = ref();

const receiveData = (contents: string) => {
  apis.product.updateBaseInfo(props.productId, { contents: contents }).then(res => {
    apiResponseCheck(res, () => {
      showAlert('상품 설명 정보가 저장되었습니다.', 'success');
      emits('changedProdInfo');
      emits('saveFinish', 'explain');
    });
  });
};

const onRegExplainInfo = () => {
  showConfirm('상품설명 정보를 저장하시겠습니까?', () => {
    ckeditorCustom.value.saveClicked();
  });
};

watch(
  () => props.contents,
  contents => {
    editorValue.value = JSON.parse(JSON.stringify(contents));
  },
);

const onStepActive = () => {
  if (props.productId) {
    if (props.contents) {
      editorValue.value = JSON.parse(JSON.stringify(props.contents));
    }
  }
};

defineExpose({ onStepActive });
</script>

<style scoped></style>
