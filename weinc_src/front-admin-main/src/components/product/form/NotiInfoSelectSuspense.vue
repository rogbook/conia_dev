<template>
  <button class="btn btn-outline-secondary dropdown-toggle w-100" type="button" data-bs-toggle="dropdown" aria-expanded="false" :disabled="updateStatus">
    {{ btnName }}
  </button>
  <ul class="dropdown-menu w-100 overflow-auto" style="height: 50vh">
    <li>
      <a class="dropdown-item" @click.prevent="() => onClickOption('')">직접선택</a>
    </li>
    <li class="dropdown-item"><hr class="dropdown-divider" /></li>
    <li v-for="item in notiInfo" :key="JSON.stringify(item)">
      <a class="dropdown-item" @click.prevent="() => onClickOption(item)"> {{ item }}</a>
    </li>
  </ul>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import apis from '@/apis';

const btnName = ref<string>('');

const props = defineProps<{ defaultOptionTitle: string; updateStatus: boolean }>();

onMounted(() => {
  btnName.value = props.defaultOptionTitle;
});

const notiInfo = ref<string[]>(await apis.common.getNoticeInfo({ category: '' }));

const emits = defineEmits(['selectNotiOption']);

const onClickOption = (value: string) => {
  btnName.value = value || props.defaultOptionTitle;
  emits('selectNotiOption', value);
};
</script>

<style scoped></style>
