<template>
  <div>
    <div class="label">
      <div class="icon-area btn btn-sm border-0 p-0 me-1" @click.prevent="getCategoryList(props.id)">
        <i class="bi bi-folder2" style="font-size: 20px" v-if="!open && props.depth !== 4"></i>
        <i class="bi bi-folder2-open" v-if="open" style="font-size: 20px"></i>
        <span class="ms-2 text-black h5">{{ props.label }}</span>
      </div>

      <button type="button" class="btn btn-white btn-sm border-0 p-1" @click.prevent="reqModCategory">
        <i class="bi bi-info-circle text-warning" style="font-size: 16px"></i>
      </button>
      <button type="button" class="btn btn-white btn-sm border-0 p-1 ms-2" @click.prevent="regNewCategory()" v-if="open && props.depth !== 4 && checkPermission('write:category')">
        <i class="bi bi-plus-square text-primary" style="font-size: 16px"></i>
      </button>
    </div>
    <div class="node" v-if="open">
      <tree-view v-for="item in list" :key="item.id" :id="item.id" :depth="item.depth" :label="item.label" :nodes="item.nodes" @openModal="openModal" @openModModal="openModModal"> </tree-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, checkPermission, showLogConsole } from '@/utils/common-utils';

export interface Nodes {
  id: number;
  depth: number;
  label: string;
  nodes?: Array<Nodes>;
}

const props = defineProps<{ id: number; label: string; depth?: number; nodes?: Array<Nodes> }>();
const emits = defineEmits(['openModal', 'openModModal']);
const list = ref([] as Array<Nodes>);
const open = ref(false);
const endNode = ref(false);

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

const openModal = (pid?: number, pLabel?: string) => {
  emits('openModal', pid, pLabel);
};

const openModModal = (cateId: number, label: string) => {
  emits('openModModal', cateId, label);
};

const regNewCategory = () => {
  emits('openModal', props.id, props.label);
};

const reqModCategory = () => {
  emits('openModModal', props.id, props.label);
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
