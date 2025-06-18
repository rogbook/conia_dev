<template>
  <select class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' v-model="setLimitData" @change="changeLimitData">
    <option value="10">10개씩 보기</option>
    <option value="20">20개씩 보기</option>
    <option value="50">50개씩 보기</option>
  </select>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';

const props = defineProps<{
  limit: number | string;
}>();
const emits = defineEmits(['changeLimitData']);

watch(
  () => props.limit,
  () => {
    setLimitData.value = props.limit;
  },
);

const setLimitData = ref();

const changeLimitData = () => {
  emits('changeLimitData', setLimitData.value);
};

onMounted(() => {
  setLimitData.value = props.limit;
});
</script>
