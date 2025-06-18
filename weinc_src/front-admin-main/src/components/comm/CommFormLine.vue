<template>
  <div class="row mb-4 align-items-center">
    <label class="col-sm-2 col-form-label form-label text-nowrap" :for="inputFor">{{ title }} </label>
    <div :class="['col-sm-' + width]">
      <div :class="slotParent">
        <slot />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
defineProps({
  title: {
    type: String,
    default: undefined,
  },
  width: {
    type: Number,
    default: 9,
  },
  slotParent: {
    type: String,
    default: 'input-group input-group-sm-vertical',
    required: false,
  },
  inputFor: {
    type: String,
    default: '',
    required: false,
  },
});
</script>

<style scoped></style>
