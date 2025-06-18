<template>
  <PageNavigator :before_link="['카탈로그 관리']" :current="'카탈로그 관리 상세'" />
  <div class="card col-md-8">
    <div class="card-header py-2">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2 col mb-0">카탈로그 관리</div>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-success me-2" @click.prevent="router.push({ path: '/product/catalog/edit/', state: { id: catalogInfo.id } })">상품 연결 관리</button>
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="router.push({ path: '/product/catalog/view', state: { id: catalogInfo.id } })">상점 연결 관리</button>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 -->
    <div class="card-body">
      <div class="card">
        <div class="card-header">
          <span class="icon icon-xs icon-dark icon-circle" style="width: 0.5rem; height: 0.5rem"></span>
          카탈로그 정보
        </div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">카탈로그명</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="카탈로그명을 입력해주세요." v-model.trim="catalogInfo.name" maxlength="20" />
              </div>
            </div>
          </div>
          <div class="row col mb-4 align-items-center">
            <label class="col-md-2 col-form-label text-nowrap">카탈로그 설명</label>
            <div class="col">
              <div class="input-group">
                <textarea type="text" class="form-control" rows="5" v-model="catalogInfo.description" maxlength="255" placeholder="카탈로그에 대한 설명을 입력해주세요." />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">노출설정</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_y" type="radio" class="form-check-input" name="radio_catalog_open" value="Y" v-model="catalogInfo.open" />
                <label class="form-check-label" for="radio_open_y">노출</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_n" type="radio" class="form-check-input" name="radio_catalog_open" value="N" v-model="catalogInfo.open" />
                <label class="form-check-label" for="radio_open_n">비노출</label>
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer py-2 text-end">
          <div class="row align-items-center justify-content-end">
            <div class="col-auto">
              <button type="button" class="btn btn-sm btn-primary" @click.prevent="modCatalog">저장</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 END -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import type { Catalog } from 'CatalogProductModule';
import PageNavigator from '@/components/title/PageNavigator.vue';
import apis from '@/apis';

const router = useRouter();
const catalogInfo = ref({} as Catalog);
const originCatalogInfo = ref({} as Catalog);

const modCatalog = () => {
  const modData = {} as any;

  if (catalogInfo.value.name !== originCatalogInfo.value.name) {
    modData['name'] = catalogInfo.value.name;
  }

  if (catalogInfo.value.description !== originCatalogInfo.value.description) {
    modData['description'] = catalogInfo.value.description;
  }

  if (catalogInfo.value.open !== originCatalogInfo.value.open) {
    modData['open'] = catalogInfo.value.open;
  }

  if (Object.keys(modData).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('카탈로그 정보를 변경하시겠습니까?', () => {
    apis.catalog.mod_catalog(catalogInfo.value.id, modData).then(res => {
      apiResponseCheck(res, () => {
        showAlert('카탈로그 정보가 변경되었습니다.', 'success', () => {
          refreshCatalogInfo(modData);
        });
      });
    });
  });
};

const refreshCatalogInfo = (data: { name?: string; description?: string; open?: string }) => {
  if (data.name) {
    originCatalogInfo.value.name = data.name;
  }

  if (data.description) {
    originCatalogInfo.value.description = data.description;
  }

  if (data.open) {
    originCatalogInfo.value.open = data.open;
  }
};

onMounted(() => {
  const catalog = history.state.catalog;
  if (catalog) {
    catalogInfo.value = JSON.parse(catalog);
    originCatalogInfo.value = JSON.parse(catalog);
  } else {
    showAlert('잘못된 접근입니다.', 'warning', () => {
      if (window.history.length > 1) {
        router.back();
      } else {
        router.replace('/');
      }
    });
  }
});
</script>

<style scoped></style>
