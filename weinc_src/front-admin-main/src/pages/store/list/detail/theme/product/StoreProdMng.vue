<template>
  <div class="row mb-4 align-items-center">
    <div class="col-auto">
      <h2 class="mb-0">[{{ props.themeName }}] 테마상품관리</h2>
    </div>
    <div class="col-auto" v-if="false">
      <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="openModal()">상단 레이아웃 관리</button>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <ThemeProduct :themeId="props.themeId" ref="themeProd" @openCategoryModal="openCategoryModal" @openBrandModal="openBrandModal" />
    </div>
    <hr class="px-0 ms-4 me-4" />
    <div class="col">
      <CurrentStoreProd @addProdToThemeDone="addProdToThemeDone" :themeId="props.themeId" ref="currentProd" @openCategoryAddModal="openCategoryAddModal" @openBrandAddModal="openBrandAddModal" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CurrentStoreProd from '@/pages/store/list/detail/theme/product/CurrentStoreProd.vue';
import ThemeProduct from '@/pages/store/list/detail/theme/product/ThemeProduct.vue';
import { showAlert, showModal, hideModal } from '@/utils/common-utils';

const emits = defineEmits(['openCategoryModal', 'openBrandModal', 'openCategoryAddModal', 'openBrandAddModal']);
const openCategoryModal = () => {
  emits('openCategoryModal');
};
const openBrandModal = () => {
  emits('openBrandModal');
};
const closeCategoryModal = (cateId: number, cateLabel: string) => {
  themeProd.value.closeCategoryModal(cateId, cateLabel);
};
const closeBrandModal = (brandId: number, brandName: string) => {
  themeProd.value.closeBrandModal(brandId, brandName);
};

const openCategoryAddModal = () => {
  emits('openCategoryAddModal');
};
const openBrandAddModal = () => {
  emits('openBrandAddModal');
};
const closeCategoryAddModal = (cateId: number, cateLabel: string) => {
  currentProd.value.closeCategoryAddModal(cateId, cateLabel);
};
const closeBrandAddModal = (brandId: number, brandName: string) => {
  currentProd.value.closeBrandAddModal(brandId, brandName);
};

const themeProd = ref();
const currentProd = ref();

const props = defineProps({
  themeName: {
    type: String,
    required: true,
  },
  themeId: {
    type: Number,
    required: true,
  },
});

const openModal = () => {
  showModal('setThemeLayoutModal');
};

const addProdToThemeDone = () => {
  themeProd.value.refreshThemeProdList();
};

const storeCode = ref();

defineExpose({ closeCategoryModal, closeBrandModal, closeCategoryAddModal, closeBrandAddModal });

onMounted(() => {
  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }
});
</script>

<style scoped>
hr {
  border: none;
  border-left: 1px solid hsla(200, 10%, 50%, 100);
  width: 1px;
}
</style>
