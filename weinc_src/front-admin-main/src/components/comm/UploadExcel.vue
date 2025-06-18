<template>
  <input id="file-input-excel" class="d-none" accept="multipart/form-data" ref="click" @change="uploadFile" type="file" />
  <button type="button" @click.prevent="onClickUploadBtn" :class="props.btn?.btnClass" v-if="btn">{{ props.btn.btnName }}</button>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { PropType } from 'vue';
import { showAlert } from '@/utils/common-utils';

interface IBtnModel {
  btnName: string;
  btnClass: string;
}
const props = defineProps({
  btn: {
    type: Object as PropType<IBtnModel>,
    required: true,
  },
  compType: {
    type: String,
  },
  hidden: {
    default: true,
  },
});
const emits = defineEmits(['upload']);

const file = ref<File | null>();

const click = ref();

const onClickUploadBtn = () => {
  click.value.click();
};
const uploadFile = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target && target.files) {
    file.value = target.files[0];
    const fileName = file.value.name;
    const fileExtension = fileName.split('.').pop();
    const fileSizeInBytes = file.value.size;
    const fileSizeInMB = fileSizeInBytes / (1024 * 1024);

    if (fileExtension !== 'xlsx') {
      showAlert('확장자가 [.xlsx]인 엑셀 파일만 업로드 할 수 있습니다.', 'warning');
      //@ts-ignore
      click.value.value = '';
      return;
    }
    emits('upload', file.value);
    click.value.value = '';
  }
};
</script>

<style scoped></style>
