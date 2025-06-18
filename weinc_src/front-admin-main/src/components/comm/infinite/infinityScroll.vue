<template>
  <ul class="list-group list-group-flush overflow-auto" ref="listEl" style="height: 50vh">
    <li @click="() => emits('clickList', d)" :key="JSON.stringify(d)" v-for="d in dataList" class="list-group-item list-group-item-action d-flex justify-content-between align-items-start">{{ d.name }}</li>
    <p v-show="fetchData || searchEnd">잠시만 기다려주세요..</p>
  </ul>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useInfiniteScroll } from '@vueuse/core';

const props = defineProps<{ asyncFunction: (scrollInfo: { limit: number; offset: number; name: string }) => Promise<unknown[]>; toShow: number; search: string; searchMode: boolean }>();

const listEl = ref<HTMLInputElement | null>();

const dataList = ref();

const fetchData = ref<boolean | null>(null);

const searchEnd = ref(false);

const emits = defineEmits(['clickList']);

// 특정 검색 후 초기화
watch(
  () => props.searchMode,
  sm => {
    fetchData.value = null;
    searchEnd.value = false;
    initSearch();
  },
);

// 첫 로드시 검색 초기화
onMounted(() => {
  initSearch();
});

// 초기화
const initSearch = async () => {
  dataList.value = await props.asyncFunction({ limit: props.toShow, offset: 0, name: props.search });
};

// 검색
const getOnScroll = async () => {
  fetchData.value = true;
  // throttling
  await new Promise(res => setTimeout(res, 400));
  const newData = await props.asyncFunction({ limit: props.toShow, offset: dataList.value.length, name: props.searchMode ? props.search : props.search });
  if (newData.length === props.toShow) {
    dataList.value.push(...newData);
    fetchData.value = null;
  }
  searchEnd.value = true;
};

useInfiniteScroll(
  listEl,
  async () => {
    fetchData.value || (await getOnScroll());
  },
  { distance: 10 },
);
</script>

<style scoped></style>
