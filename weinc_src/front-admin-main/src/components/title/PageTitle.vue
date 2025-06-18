<template>
  <div class="col-12 border py-md-6 px-md-4 mb-md-6 py-3 px-3 mb-3">
    <p class="fs-2">{{ title }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ title: string }>();
</script>

<style scoped></style>
