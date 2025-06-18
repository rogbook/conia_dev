<template>
  <div class="row mb-4 align-items-center">
    <div class="col-auto">
      <h2 class="mb-0">[{{ props.themeName }}] 테마매장관리</h2>
    </div>
    <div class="col-auto" v-if="false">
      <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="openModal()">상단 레이아웃 관리</button>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <ThemeShop :themeId="props.themeId" ref="themeProd" />
    </div>
    <hr class="px-0 ms-4 me-4 d-none d-lg-block" />
    <div class="col">
      <CurrentStoreShop @addShopToThemeDone="addShopToThemeDone" :themeId="props.themeId" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CurrentStoreShop from '@/pages/store/list/detail/theme/shop/CurrentStoreShop.vue';
import ThemeShop from '@/pages/store/list/detail/theme/shop/ThemeShop.vue';
import { showAlert, showModal, hideModal } from '@/utils/common-utils';

const themeProd = ref();

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

const addShopToThemeDone = () => {
  themeProd.value.getThemeShopList();
};

const storeCode = ref();

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
