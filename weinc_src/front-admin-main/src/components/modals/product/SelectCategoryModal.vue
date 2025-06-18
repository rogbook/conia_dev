<template>
  <div class="card">
    <div class="card-body ps-8">
      <div class="label h2"><i class="bi bi-folder2-open" style="font-size: 22px"></i>[카테고리]</div>
      <div class="node">
        <SelectCategoryTreeView v-for="item in list" :key="item.id" :id="item.id" :label="item.label" :nodes="item.nodes" @closeModal="closeModal"> </SelectCategoryTreeView>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Nodes } from '@/pages/product/category/TreeView.vue';
import SelectCategoryTreeView from '@/components/modals/product/SelectCategoryTreeView.vue';
import { onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import { apiResponseCheck, showLogConsole } from '@/utils/common-utils';

const list = ref([] as Array<Nodes>);
const emits = defineEmits(['closeModal']);
const getCategoryList = () => {
  apis.common.getCategories().then(res => {
    apiResponseCheck(res, () => {
      list.value = [];
      showLogConsole(res);
      for (const c of res) {
        list.value.push({ id: c.id, label: c.name, depth: c.depth });
      }
    });
  });
};
const openModal = () => {
  getCategoryList();
};
const closeModal = (cateId: number, cateLabel: string) => {
  emits('closeModal', cateId, cateLabel);
};
defineExpose({ openModal });
</script>

<style scoped>
.node {
  margin-left: 20px;
}
</style>
