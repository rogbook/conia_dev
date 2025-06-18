<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세'] : ['상점 관리', '상점관리 상세']" :current="'상품 관리'" />
  <div class="row mb-4">
    <h2>상품 관리</h2>
  </div>
  <div class="row mb-4">
    <h4>- {{ storeInfo.title }} [현재 {{ storeInfo.status === 'Y' ? '운영중' : storeInfo.status === 'R' ? '승인대기중' : '미운영' }}]</h4>
  </div>
  <div class="row">
    <div class="col">
      <CurrentStoreProd ref="currentStore" />
    </div>
    <hr class="px-0 ms-4 me-4 d-none d-lg-block" />
    <div class="col">
      <AddStoreProd @executeFunctionEvent="executeFunction" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import AddStoreProd from '@/pages/store/list/detail/product/AddStoreProd.vue';
import CurrentStoreProd from '@/pages/store/list/detail/product/CurrentStoreProd.vue';
import { apiResponseCheck, getUserClassStr, showAlert, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';

const storeCode = ref();
const currentStore = ref();
const storeInfo = reactive({
  title: '',
  status: '',
});

const executeFunction = () => {
  currentStore.value.refreshStoreProdList();
};

const getStoreInfo = () => {
  apis.store.get_store(storeCode.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      storeInfo.title = res.title;
      storeInfo.status = res.status;
    });
  });
};

onMounted(() => {
  storeCode.value = history.state.code;
  if (storeCode.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }

  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');
  getStoreInfo();
});
</script>

<style scoped>
hr {
  border: none;
  border-left: 1px solid hsla(200, 10%, 50%, 100);
  width: 1px;
}
</style>
