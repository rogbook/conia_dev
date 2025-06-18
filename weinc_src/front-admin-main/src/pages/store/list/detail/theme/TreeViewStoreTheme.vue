<template>
  <div class="list-group-flush py-2 row align-items-center">
    <div class="col-md-1 justify-content-center">
      <i class="bi bi-caret-right-fill" v-if="props.sub?.length && !isOpen" @click.prevent="isOpen = !isOpen"></i>
      <i class="bi bi-caret-down-fill" v-if="props.sub?.length && isOpen" @click.prevent="isOpen = !isOpen"></i>
    </div>
    <div class="list-group-item col-auto">
      <span v-if="props.isRoot" class="me-1">└</span>
      <span @click.prevent="isOpen = !isOpen">
        {{ props.name }} <span style="font-size: 0.5rem">( 표시순번 : {{ props.sort }} ) </span>
      </span>
      <button type="button" class="btn badge bg-info ms-2 me-2" @click.prevent="selectTheme(props.theme)">설정</button>
      <button type="button" class="btn btn-white btn-sm border-0 p-0" @click.prevent="addThemeModal(props.theme.id, props.theme.name)" v-if="!props.isRoot">
        <i class="bi bi-plus-square text-primary" style="font-size: 14px"></i>
      </button>
    </div>
  </div>
  <div v-if="props.sub?.length && isOpen">
    <tree-view-store-theme v-for="item in props.sub" :key="item.id" :name="item.name" :sub="item.sub" :sort="item.sort" :isRoot="true" :theme="item" @selectTheme="selectTheme"> </tree-view-store-theme>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import type { Theme } from 'ThemeInfoModule';
import { showModal } from '@/utils/common-utils';

const emits = defineEmits(['selectTheme', 'addThemeModal']);
const selectTheme = (t: Theme) => {
  console.log('selTheme');
  emits(`selectTheme`, t);
};

const addThemeModal = (id: number, name: string) => {
  emits(`addThemeModal`, id, name);
};

export interface Nodes {
  name: string;
  sort: number;
  sub?: Array<Nodes>;
  isRoot: boolean;
  theme: Theme;
}
const props = defineProps<{
  name: string;
  sort: number;
  sub?: Array<Nodes>;
  isRoot: boolean;
  theme: Theme;
}>();
const isOpen = ref(false);
</script>
