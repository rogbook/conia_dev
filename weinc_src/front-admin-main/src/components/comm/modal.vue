<template>
  <!-- TODO: Modal Ckeditor 관련 data-bs-focus=false 추가 / 이후 다른 모달에서 문제발생시 제거 -->
  <div class="modal fade" :id="id" data-bs-backdrop="static" tabindex="-1" role="dialog" :aria-labelledby="id" aria-hidden="true" :class="{ 'modal-xl': xlarge, 'modal-xl2': xlarge_big, 'modal-second': second, 'modal-third': third }">
    <div class="modal-dialog" :class="{ 'modal-fullscreen': xxlarge, 'modal-dialog-centered': centered }" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <slot name="header" />
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <slot name="body" />
        </div>
        <div class="modal-footer py-2">
          <slot name="footer" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: 'modal',
  },
  xlarge: {
    type: Boolean,
    default: false,
  },
  xlarge_big: {
    type: Boolean,
    default: false,
  },
  xxlarge: {
    type: Boolean,
    default: false,
  },
  cancelBtnHandler: {
    type: Function,
    required: false,
    default: () => {},
  },
  second: {
    type: Boolean,
    required: false,
  },
  third: {
    type: Boolean,
    required: false,
  },
  centered: {
    type: Boolean,
    required: false,
  },
  isEditorIn: {
    type: Boolean,
    required: false,
    default: false,
  },
});
</script>

<style scoped>
.modal-second {
  border: 1px black;
}
</style>
