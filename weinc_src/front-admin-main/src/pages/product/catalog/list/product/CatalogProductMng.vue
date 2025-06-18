<template>
  <PageNavigator :before_link="['카탈로그관리']" :current="'카탈로그 상품관리'" />
  <div class="row mb-4">
    <h2>카탈로그 상품관리</h2>
  </div>
  <div class="row mb-4">
    <h4>카탈로그명 : {{ catalogInfo.name }} (공개여부 : {{ catalogInfo.open }})</h4>
  </div>
  <div class="row">
    <div class="col">
      <CurrentCatalogProd ref="currentCatalog" />
    </div>
    <hr class="px-0 ms-2 me-2 d-none d-lg-block" />
    <div class="d-md-none mt-3"></div>
    <div class="col">
      <AddCatalogProd @executeFunctionEvent="executeFunction" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import AddCatalogProd from '@/pages/product/catalog/list/product/AddCatalogProd.vue';
import CurrentCatalogProd from '@/pages/product/catalog/list/product/CurrentCatalogProd.vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';
import PageNavigator from '@/components/title/PageNavigator.vue';

const catalogId = ref();
const currentCatalog = ref();
const catalogInfo = reactive({
  name: '',
  status: '',
  open: '',
});

const executeFunction = () => {
  currentCatalog.value.refreshCatalogProdList();
};

const getCatalogInfo = () => {
  apis.catalog.get_catalog_info(catalogId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      catalogInfo.name = res.name;
      catalogInfo.status = res.status;
      catalogInfo.open = res.open;
    });
  });
};

onMounted(() => {
  catalogId.value = history.state.id;
  if (catalogId.value === undefined) {
    showAlert('일시적인 오류가 발생하였습니다. 잠시 후 다시 시도해주세요.', 'error');
    useRouter().back();
  }

  // @ts-ignore
  // HSCore.components.HSFlatpickr.init('.js-flatpickr');

  getCatalogInfo();
});
</script>

<style scoped>
hr {
  border: none;
  border-left: 1px solid hsla(200, 10%, 50%, 100);
  width: 1px;
}
</style>
