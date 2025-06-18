<script setup lang="ts">
import { onMounted } from 'vue';
import RootLayout from '@/layouts/rootLayout.vue';
import { useCommonStore } from '@/stores/common';
import Spinner from '@/components/comm/Spinner.vue';
import { useLoadingStore } from '@/stores/loading';
useCommonStore().init();
// 페이지 테마 모드 (default / dark)
localStorage.setItem('hs_theme', 'default');
</script>

<template>
  <root-layout>
    <Spinner v-if="useLoadingStore().getIsLoading" />
    <router-view :key="$route.fullPath" />
  </root-layout>
</template>

<style scoped></style>
