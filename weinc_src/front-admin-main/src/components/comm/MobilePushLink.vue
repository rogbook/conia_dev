<template>
  <button type="button" class="btn btn-xs btn-soft-danger" @click.prevent="showModal('selGroupModal')">모바일 푸쉬 링크</button>

  <!-- 상점검색 Modal -->
  <Modal :id="'selGroupModal'" :title="'모바일 푸쉬 링크 생성'">
    <template #body>
      <div class="text-start mb-4">{{ props.title }} 링크를 생성합니다</div>
      <div class="card mb-1">
        <div class="card-body">
          <div class="row col align-items-center">
            <label class="col-1 col-form-label text-nowrap">그룹지정</label>
            <div class="col-2"></div>
            <div class="col">
              <!-- <div class="input-group" v-if="isStore">

              </div> -->
              <div class="input-group">
                <input ref="copyTarget" type="hidden" />
                <input v-if="group !== 'none'" type="text" class="form-control" :value="group" disabled />
                <select v-else-if="isStore" class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' v-model="group" disabled>
                  <option value="none">그룹 없음</option>
                </select>
                <select v-else class="form-select" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}' v-model="group">
                  <option value="none">그룹 없음</option>
                  <option :value="item" v-for="(item, i) in storeGroupList" :key="i">{{ item }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <button type="button" class="btn btn-primary" @click.prevent="copyLink">생성</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref, watch } from 'vue';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';

const props = withDefaults(
  defineProps<{
    title: string;
    storeGroup?: string;
    nextValue: string;
    isStore?: boolean;
  }>(),
  {
    title: '',
    storeGroup: 'none',
    nextValue: '',
    isStore: false,
  },
);

const storeGroupList = ref();
const group = ref();
const copyTarget = ref();

const getStoreGroupList = () => {
  apis.store.get_store_group_list().then(res => {
    apiResponseCheck(res, () => {
      storeGroupList.value = res;
    });
  });
};

const copyLink = () => {
  copyTarget.value.setAttribute('type', 'text');

  if (group.value !== 'none') {
    copyTarget.value.value = `https://service.coniaworld.com?from=app&group=${group.value}&next=${props.nextValue}`;
  } else {
    copyTarget.value.value = `https://service.coniaworld.com?from=app&next=${props.nextValue}`;
  }
  copyTarget.value.select();
  document.execCommand('copy');
  copyTarget.value.setAttribute('type', 'hidden');
  showAlert('링크가 생성되었습니다.', 'success');
  hideModal('selGroupModal');
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('selGroupModal').addEventListener('show.bs.modal', function (event) {
    group.value = props.storeGroup;
    if (props.storeGroup === 'none') {
      getStoreGroupList();
    }
  });
});
</script>
