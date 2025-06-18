<template>
  <input id="file-input" class="d-none" accept="image/*" ref="click" @change="uploadImage" type="file" />
  <input v-bind="{ ...$attrs }" v-show="!hidden" />
  <button type="button" @click.prevent="onClickUploadBtn" :class="props.btn.btnClass" v-if="btn" :disabled="isDisabled">{{ props.btn.btnName }}</button>
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
    default: false,
  },
  isDisabled: {
    type: Boolean,
    default: false,
  },
});
const emits = defineEmits(['upload']);

const file = ref<File | null>();

const click = ref();

const onClickUploadBtn = () => {
  click.value.click();
};
const uploadImage = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target && target.files) {
    file.value = target.files[0];
    const fileName = file.value.name;
    const fileExtension = fileName.split('.').pop();
    const fileSizeInBytes = file.value.size;
    const fileSizeInMB = fileSizeInBytes / (1024 * 1024);

    if (props.compType === 'favicon' && fileExtension !== 'ico') {
      showAlert("파비콘은 'ico' 파일만 업로드할 수 있습니다.", 'warning');
      return;
    }

    if (fileSizeInMB > 20) {
      showAlert('파일 크기가 20MB를 초과하여 업로드할 수 없습니다.', 'warning');
      return;
    }

    if (props.compType) {
      emits('upload', file.value, props.compType);
      target.value = '';
    } else {
      target.value = '';
      emits('upload', file.value);
    }
  }
};
</script>

<style scoped></style>
