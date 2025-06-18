<template>
  <ckeditor :editor="editorData.editor" v-model="editorData.editorData" :config="editorData.editorConfig" :disabled="props.disabled"></ckeditor>
</template>

<script setup lang="ts">
//@ts-ignore
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { reactive, watch } from 'vue';
import type { PropType } from 'vue';
import UploadAdapter from '@/utils/UploadAdapter';

const props = defineProps({
  editorData: {
    type: String,
    default: '',
  },
  removeItems: {
    type: Array as PropType<string[]>,
    default: [] as PropType<string[]>,
  },
  url: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['receiveData']);

watch(
  () => props.editorData,
  v => {
    editorData.editorData = v;
  },
);

const editorData = reactive({
  editor: ClassicEditor,
  editorData: props.editorData,
  editorConfig: {
    allowedContent: true,
    language: 'ko',
    toolbar: {
      items: ['heading', 'alignment', '|', 'bold', 'italic', 'fontSize', 'fontColor', 'fontFamily', 'fontBackgroundColor', '|', 'bulletedList', 'numberedList', '|', 'imageUpload', 'mediaEmbed', 'insertTable', 'link', '|', 'undo', 'redo'],
      removeItems: props.removeItems,
    },
    heading: {
      options: [
        { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
        { model: 'heading1', view: { name: 'h1', classes: 'conia-h1' }, title: 'Heading 1', class: 'ck-heading_heading1' },
        { model: 'heading2', view: { name: 'h2', classes: 'conia-h2' }, title: 'Heading 2', class: 'ck-heading_heading2' },
        { model: 'heading3', view: { name: 'h3', classes: 'conia-h3' }, title: 'Heading 3', class: 'ck-heading_heading3' },
        { model: 'heading4', view: { name: 'h4', classes: 'conia-h4' }, title: 'Heading 4', class: 'ck-heading_heading4' },
        { model: 'heading5', view: { name: 'h5', classes: 'conia-h5' }, title: 'Heading 5', class: 'ck-heading_heading5' },
        { model: 'heading6', view: { name: 'h6', classes: 'conia-h6' }, title: 'Heading 6', class: 'ck-heading_heading6' },
      ],
    },
    link: {
      decorators: {
        addClass: {
          mode: 'manual',
          label: '복제몰용 링크',
          attributes: {
            class: 'conia-el-link',
          },
        },
      },
    },
    mediaEmbed: {
      previewsInData: true,
    },
    extraPlugins: [
      //@ts-ignore
      function (editor) {
        //@ts-ignore
        editor.plugins.get('FileRepository').createUploadAdapter = loader => {
          if (props.url) return new UploadAdapter(loader, props.url);
          else return new UploadAdapter(loader);
        };
      },
    ],
  },
});

const saveClicked = () => {
  emit('receiveData', editorData.editorData);
};

const cancelEdit = () => {
  editorData.editorData = '';
};

const replaceEdit = (data: string) => {
  editorData.editorData = data;
};

defineExpose({ saveClicked, cancelEdit, replaceEdit });
</script>

<style>
.ck-editor__editable {
  min-height: 32vh !important;
  max-height: 75vh !important;
  overflow-y: scroll;
}
</style>
