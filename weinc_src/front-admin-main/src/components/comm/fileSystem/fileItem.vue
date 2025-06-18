<template>
  <span class="file" @click.prevent=""><i class="bi bi-file-arrow-down-fill"></i> {{ item.name }}</span>
</template>

<script setup lang="ts">
import type { IItem } from '@/components/comm/types';

defineProps<{ item: IItem }>();
</script>

<style scoped>
.file {
  padding-left: 1rem;
}
</style>
