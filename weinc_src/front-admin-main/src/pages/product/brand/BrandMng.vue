<template>
  <PageNavigator :before_link="[]" :current="'브랜드 설정'" />
  <div class="card col-md-6">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">브랜드 설정</div>
    </div>
    <div class="card-body">
      <div class="row">
        <CardContainer :title="''" :columnType="IColumnType.DEFAULT" :noFooter="false">
          <template #header>
            <div class="input-group">
              <input v-model="search" type="text" class="form-control" :placeholder="'브랜드 검색'" @keypress.enter.prevent="onSearchAction" @change="onChangeAction" />
              <button type="button" @click.prevent="onSearchAction" class="btn w-25 btn-secondary">검색</button>
            </div>
          </template>
          <suspense>
            <InfinityScroll :search="search" :searchMode="searchMode" :to-show="30" :async-function="infFunc" @clickList="target => onChoice(target, true)" style="cursor: pointer" />
            <template #fallback>
              <p>Loading...</p>
            </template>
          </suspense>
          <template #footer>
            <div class="col text-end">
              <button type="button" class="btn btn-sm btn-primary" @click.prevent="openModal">신규등록</button>
            </div>
          </template>
        </CardContainer>
      </div>
    </div>
  </div>

  <Modal :id="'regNewBrandModal'" :title="'브랜드 신규 등록'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">브랜드를 신규 등록합니다.</div>

        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label text-md-center">브랜드명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control text-center col" v-model.trim="newValue" maxlength="45" placeholder="브랜드명을 입력해주세요." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="regNewBrand">등록</button>
    </template>
  </Modal>

  <Modal :id="'reqModBrandModal'" :title="'브랜드 정보 수정'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">브랜드 정보를 수정합니다.</div>

        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label text-md-center">브랜드명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control text-center col" v-model.trim="newValue" maxlength="45" placeholder="브랜드명을 입력해주세요." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="regModBrand">수정</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import InfinityScroll from '@/components/comm/infinite/infinityScroll.vue';
import CardContainer from '@/components/modals/card/CardContainer.vue';
import { IColumnType } from '@/components/modals/types';
import type { IDynamicKeyValue } from '@/components/types';
import { useCommonStore } from '@/stores/common';
import { ref, watch } from 'vue';
import Modal from '@/components/comm/modal.vue';
import { apiResponseCheck, showAlert, showConfirm, showModal, hideModal } from '@/utils/common-utils';
import apis from '@/apis';
import { AxiosError } from 'axios';
import PageNavigator from '@/components/title/PageNavigator.vue';

const newValue = ref('');
const originalValue = ref('');
/**
 need to use commonStore getter name properties with array
 this library link with commonStore only.
 */
const infFunc = useCommonStore().reqInfBrands;
const choose = ref<IDynamicKeyValue>({});

const searchMode = ref<boolean>(false);

const search = ref('');

const onChangeAction = () => {
  searchMode.value = !searchMode.value;
};
const onSearchAction = () => {
  if (search.value) {
    searchMode.value = true;
  } else {
    searchMode.value = false;
  }
};

const openModal = () => {
  newValue.value = '';
  showModal('regNewBrandModal');
};

const regNewBrand = () => {
  if (!newValue.value) {
    showAlert('브랜드명을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('브랜드를 등록하시겠습니까?', () => {
    apis.common.addBrand({ name: newValue.value }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('브랜드가 등록되었습니다.', 'success');
        window.document.location.reload();
      });
    });
  });
};

const onChoice = (target: IDynamicKeyValue, isChoice: boolean) => {
  choose.value = target;
  newValue.value = choose.value.name as string;
  originalValue.value = choose.value.name as string;
  showModal('reqModBrandModal');
};

const checkIsChange = () => {
  if (originalValue.value !== newValue.value) return true;
  showAlert('변경된 내용이 없습니다.', 'warning');
  return false;
};

const regModBrand = () => {
  if (!newValue.value) {
    showAlert('브랜드명을 입력해주세요.', 'warning');
    return;
  }
  if (!checkIsChange()) return;

  showConfirm('브랜드를 수정하시겠습니까?', () => {
    apis.common.modBrand(choose.value.id as number, { name: newValue.value }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('브랜드가 수정되었습니다.', 'success');
        window.document.location.reload();
      });
    });
  });
};
</script>

<style scoped></style>
