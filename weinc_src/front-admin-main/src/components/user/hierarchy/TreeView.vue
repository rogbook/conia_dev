<template>
  <div style="display: flex">
    <div class="icon-area p-0 me-1">
      <span v-if="props.isRoot" class="me-1">└</span>
      <i class="bi bi-person" style="font-size: 22px"></i>
      <span class="ms-2 text-black h5">
        {{ props.name }} <span style="font-size: 12px">( [업체] {{ props.company }} ) </span>
      </span>
    </div>
    <i class="bi bi-folder2" v-if="props.sub?.length && !isOpen" style="font-size: 22px; cursor: pointer" @click.prevent="isOpen = !isOpen"></i>
    <i class="bi bi-folder2-open" v-if="props.sub?.length && isOpen" style="font-size: 22px; cursor: pointer" @click.prevent="isOpen = !isOpen"></i>
  </div>
  <div class="ms-3" v-if="props.sub?.length && isOpen">
    <tree-view v-for="(item, i) in props.sub" :key="i" :name="item.name" :sub="item.sub" :company="item.company_name" :isRoot="true"> </tree-view>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, checkPermission, showLogConsole } from '@/utils/common-utils';

export interface Nodes {
  name: string;
  company: string;
  sub?: Array<Nodes>;
  isRoot: boolean;
}
const props = defineProps<{
  name: string;
  company: string;
  sub?: Array<Nodes>;
  isRoot: boolean;
}>();
const isOpen = ref(false);
</script>
