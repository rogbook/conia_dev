<template>
  <div>
    <div class="icon-area btn btn-sm border-0 p-0 me-1" @click.prevent="getCategoryList(props.id)">
      <i class="bi bi-folder2" style="font-size: 20px" v-if="!open && props.depth !== 4"></i>
      <i class="bi bi-folder2-open" v-if="open" style="font-size: 20px"></i>
      <span class="ms-2 text-black h5">{{ props.label }}</span>
    </div>
    <button type="button" class="btn badge bg-info ms-2" @click.prevent="selectCategory(props.id, props.label)">선택</button>
    <div class="node" v-if="open">
      <SelectCategoryTreeView v-for="item in list" :key="item.id" :id="item.id" :depth="item.depth" :label="item.label" :nodes="item.nodes" @closeModal="closeModal"> </SelectCategoryTreeView>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import SelectCategoryTreeView from '@/components/modals/product/SelectCategoryTreeView.vue';
import { apiResponseCheck, checkPermission, showLogConsole } from '@/utils/common-utils';

export interface Nodes {
  id: number;
  depth: number;
  label: string;
  nodes?: Array<Nodes>;
}

const props = defineProps<{ id: number; label: string; depth?: number; nodes?: Array<Nodes> }>();
const emits = defineEmits(['closeModal']);
const list = ref([] as Array<Nodes>);
const open = ref(false);
const endNode = ref(false);

const selectCategory = (cateId: number, cateLabel: string) => {
  emits('closeModal', cateId, cateLabel);
};
const closeModal = (cateId: number, cateLabel: string) => {
  emits('closeModal', cateId, cateLabel);
};

const getCategoryList = (id: number) => {
  if (props.depth === 4 || endNode.value) {
    return;
  }
  if (list.value.length > 0) {
    open.value = !open.value;
    return;
  }
  apis.common.getCategories({ pid: id }).then(res => {
    apiResponseCheck(res, () => {
      for (const c of res) {
        showLogConsole(res);
        list.value.push({ id: c.id, label: c.name, depth: c.depth });
      }
      open.value = true;
      if (list.value.length === 0) {
        endNode.value = true;
      }
    });
  });
};

onMounted(() => {});
</script>

<style scoped>
.label {
  display: flex;
  align-items: center;
}

.node {
  margin-left: 20px;
}
</style>
