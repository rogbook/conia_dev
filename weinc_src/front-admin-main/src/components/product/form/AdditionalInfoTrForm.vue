<template>
  <tr class="row">
    <td class="col-5">
      <div class="input-group">
        <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" :disabled="updateStatus">직접선택</button>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" href="#">직접선택</a></li>
          <!--        <li><a class="dropdown-item" href="#">Another action</a></li>-->
          <!--        <li><a class="dropdown-item" href="#">Something else here</a></li>-->
          <!--        <li><hr class="dropdown-divider" /></li>-->
          <!--        <li><a class="dropdown-item" href="#">Separated link</a></li>-->
        </ul>
        <input
          :value="category"
          @change="
            e => {
              emits('changeChild', { value: e.target.value, target: 'category', index });
            }
          "
          placeholder="제조사"
          class="form-control"
          :disabled="updateStatus" />
      </div>
    </td>
    <td class="col-5">
      <div class="input-group">
        <input
          :value="contents"
          @change="
            e => {
              emits('changeChild', { value: e.target.value, target: 'contents', index });
            }
          "
          class="form-control"
          placeholder="내용"
          :disabled="updateStatus" />
        <small class="form-text m-">0/255</small>
      </div>
    </td>
    <td class="col-2">
      <button type="button" @click.prevent="" class="btn" :disabled="updateStatus">
        <i class="bi bi-dash-circle-fill" style="vertical-align: center"></i>
      </button>
    </td>
  </tr>
</template>

<script setup lang="ts">
const emits = defineEmits(['changeChild']);
const props = defineProps<{ category: string; contents: string; index: number; updateStatus: boolean }>();
</script>

<style scoped></style>
