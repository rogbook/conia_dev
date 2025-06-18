<template>
  <Modal :id="'selGroupModal'" :title="'변경이력 상세'" :xlarge="true">
    <template #body>
      <div class="card mb-1">
        <div class="card-body">
          <div class="row col align-items-center mb-3" v-for="(item, i) in logTitleArray" :key="i">
            <label class="col-md-1 col-form-label">{{ item }}</label>
            <div class="col">
              <div class="row align-items-center mb-2">
                <label class="col-md-1 col-form-label text-nowrap text-primary">변경전</label>
                <div class="col">
                  <div v-if="logBeforeArray[i].startsWith('<img class')" v-html="logBeforeArray[i]" class="form-control"></div>
                  <textarea v-else v-html="logBeforeArray[i]" class="form-control" disabled></textarea>
                </div>
              </div>
              <div class="row align-items-center mb-2">
                <label class="col-md-1 col-form-label text-nowrap text-success">변경후</label>
                <div class="col">
                  <div v-if="logAfterArray[i].startsWith('<img class')" v-html="logAfterArray[i]" class="form-control"></div>
                  <textarea v-else v-html="logAfterArray[i]" class="form-control" disabled></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { computed } from 'vue';

const props = defineProps<{
  logTitle?: string;
  logBefore?: string;
  logAfter?: string;
}>();

const logTitleArray = computed(() => props.logTitle?.split('///') || []);
const logBeforeArray = computed(() => props.logBefore?.split('///') || []);
const logAfterArray = computed(() => props.logAfter?.split('///') || []);
</script>
