<template>
  <div class="banner-lg" v-bind:id="`${props.index}`">
    <div class="card mb-2">
      <div class="card-body">
        <div class="row align-items-center ms-3 me-4">
          <div class="col row">
            <div class="square form-control table-text-center py-5">배너(L)</div>
          </div>
          <div class="col-auto ms-4">
            <div class="row align-items-center">
              <button type="button" class="btn btn-sm btn-outline-info mb-2" @click.prevent="selectComp">설정</button>
              <button type="button" class="btn btn-sm btn-outline-danger" @click.prevent="deleteComp">삭제</button>
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer py-1" v-if="memo">
        <span>메모 : {{ memo }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  index: {
    required: true,
    type: String,
  },
  memo: {
    type: String,
    default: '',
  },
});
const emit = defineEmits(['deleteComp', 'selectComp']);
const deleteComp = () => {
  emit('deleteComp', props.index);
};

const selectComp = () => {
  emit('selectComp', props.index);
};
</script>

<style scoped></style>
