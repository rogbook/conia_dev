<template>
  <div class="column-2" v-bind:id="`${props.index}`">
    <div class="card mb-2">
      <div class="card-body">
        <div class="row align-items-center ms-4 me-4 g-2">
          <div class="col">
            <div class="row row-cols-2 g-2">
              <div>
                <div class="square form-control table-text-center py-3 px-1">아이템</div>
              </div>
              <div>
                <div class="square form-control table-text-center py-3 px-1">아이템</div>
              </div>
            </div>
          </div>
          <div class="col-12 col-lg-auto ms-lg-4">
            <div class="row align-items-center mx-auto">
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
