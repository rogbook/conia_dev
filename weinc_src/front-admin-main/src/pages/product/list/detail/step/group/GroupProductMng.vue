<template>
  <div class="row">
    <div class="col">
      <CurrentGroupProd :productId="props.productId" :paId="props.paId" />
    </div>
    <hr class="px-0 ms-4 me-4" />
    <div class="col">
      <AddGroupProd :productId="props.productId" :paId="props.paId" @refresh="refreshProdGroup" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import CurrentGroupProd from '@/pages/product/list/detail/step/group/CurrentGroupProd.vue';
import AddGroupProd from '@/pages/product/list/detail/step/group/AddGroupProd.vue';

const props = defineProps<{ productId: number; paId: number }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);

const refreshProdGroup = () => {};

const onStepActive = () => {};

defineExpose({ onStepActive });

onMounted(() => {
  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
});
</script>

<style scoped>
hr {
  border: none;
  border-left: 1px solid hsla(200, 10%, 50%, 100);
  width: 1px;
}
</style>
