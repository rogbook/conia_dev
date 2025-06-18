<template>
  <div :class="columnType || 'col'">
    <div class="js-sticky-block card mb-3">
      <div class="card-header">
        <div class="card-title">{{ title }}</div>
        <slot name="header" />
      </div>
      <!-- Body -->
      <div class="card-body">
        <slot />
      </div>
      <!-- End Body -->
      <div class="card-footer py-2" v-if="!props.noFooter">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { IColumnType } from '@/components/modals/types';

const props = defineProps<{ title: string; columnHeight?: string; columnType?: IColumnType; noFooter: boolean }>();
</script>

<style scoped></style>
