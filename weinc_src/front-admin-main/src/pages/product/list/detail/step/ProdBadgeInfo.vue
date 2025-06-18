<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품배지정보</h4>
          <small>상품에 표시될 배지를 설정합니다.(최대 3개)</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="saveClick">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="currentBadge">
        <label class="col-form-label mb-4" v-if="currentBadgeList.length > 0"><span class="text-danger">* </span>등록된 상품 배지를 삭제하려면 등록된 배지 상단의 'X'버튼을 눌러주세요.</label>
        <div class="row align-items-center">
          <div class="col-auto">현재 상품 배지</div>
          <div class="col-auto">
            <div class="py-3 d-flex flex-wrap">
              <span v-for="item in currentBadgeList" :key="item.id" class="mb-1 position-relative border border-1 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem">
                <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteBadge(item.id)"></button>
                <div>
                  <span class="badge" :style="{ 'background-color': `${item.color} !important` }">{{ item.name }}</span>
                </div>
              </span>
              <span
                v-for="(item, index) in previewBadgeList"
                :key="item.id"
                class="mb-1 position-relative border border-1 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex"
                style="width: 5rem; height: 5rem; border-color: #26a5b5 !important">
                <button type="button" v-show="item" class="btn btn-close position-absolute top-0 end-0" @click.prevent="() => onDeleteImgList(index)"></button>
                <div>
                  <span class="badge" :style="{ 'background-color': `${item.color} !important` }">{{ item.name }}</span>
                </div>
              </span>
              <div class="addPhoto" v-if="availableCount > 0">
                <span v-for="i in availableCount" :key="i" class="mb-1 position-relative border border-1 me-2 d-inline-block justify-content-center align-items-center overflow-hidden d-inline-flex" style="width: 5rem; height: 5rem; border-color: #26a5b5 !important">
                  <button type="button" @click.prevent="showModal('addBadgeModal')" class="btn btn-sm badge py-2"><i class="bi-plus-circle text-primary" style="font-size: 20px" /></button>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal :id="'addBadgeModal'" :title="'배지 선택'">
    <template #body>
      <BadgeList @addBadgeList="addBadgeList" :currentList="currentBadgeList" :previewList="previewBadgeList" />
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import BadgeList from '@/pages/product/list/detail/step/badge/BadgeList.vue';
import { computed, ref } from 'vue';
import type { BadgeInfo } from 'ProdBadgeInfo';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';

const props = defineProps<{ productId: number }>();
const emits = defineEmits(['saveFinish']);

const currentBadgeList = ref([] as BadgeInfo[]);
const previewBadgeList = ref([] as BadgeInfo[]);

const availableCount = computed(() => {
  return 3 - currentBadgeList.value.length - previewBadgeList.value.length;
});

const addBadgeList = (badges: BadgeInfo[]) => {
  let duplicateIdx: number[] = [];
  for (let i = 0; i < badges.length; i++) {
    currentBadgeList.value.map(item => {
      if (item.id === badges[i].id) {
        duplicateIdx.push(i);
      }
    });
  }

  for (const idx of duplicateIdx) {
    badges.splice(idx, 1);
  }

  hideModal('addBadgeModal');
  previewBadgeList.value = badges;
};

const getProdBadgeList = () => {
  apis.product.get_prod_link_badge_list(props.productId).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      currentBadgeList.value = res;
    });
  });
};

const onDeleteBadge = (id: number) => {
  showConfirm('기존 등록된 해당 상품 배지를 삭제하시겠습니까?', () => {
    apis.product.unlink_prod_badge(props.productId, [id]).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 배지가 삭제되었습니다.', 'success');
        getProdBadgeList();
      });
    });
  });
};

const onDeleteImgList = (index: number) => {
  // imageList.value.splice(index, 1);
  previewBadgeList.value.splice(index, 1);
};

const saveClick = () => {
  // if (previewBadgeList.value.length === 0) {
  //   showAlert('새로 추가할 상품 배지가 없습니다.', 'warning');
  //   return;
  // }

  //@ts-ignore
  const arrBadgeId: number[] = [];
  // @ts-ignore
  previewBadgeList.value.map(item => arrBadgeId.push(item.id));

  showConfirm('상품 배지 정보를 저장하시겠습니까?', () => {
    apis.product.link_prod_badge(props.productId, arrBadgeId).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 배지가 등록되었습니다.', 'success');
        previewBadgeList.value = [];
        getProdBadgeList();
        emits('saveFinish', 'badge');
      });
    });
  });
};

const onStepActive = () => {
  getProdBadgeList();
};

defineExpose({ onStepActive });
</script>

<style scoped>
hr {
  border: none;
  border-left: 1px solid hsla(200, 10%, 50%, 100);
  height: 100vh;
  width: 1px;
}
</style>
