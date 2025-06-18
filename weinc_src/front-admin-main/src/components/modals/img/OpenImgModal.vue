<template>
  <div class="modal" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content bg-transparent">
        <div class="modal-header">
          <button type="button" class="btn-close btn-close-white" style="font-size: 1.3rem; font-weight: bold" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <img class="img-fluid d-block mx-auto" :src="props.openImgUrl" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  openImgUrl: string;
}>();
</script>
