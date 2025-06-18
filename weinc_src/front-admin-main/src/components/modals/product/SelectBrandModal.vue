<template>
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
          <InfinityScroll style="cursor: pointer" :search="search" :searchMode="searchMode" :to-show="30" :async-function="infFunc" @clickList="target => selectBrand(target, true)" />
          <template #fallback>
            <p>Loading...</p>
          </template>
        </suspense>
      </CardContainer>
    </div>
  </div>
</template>

<script setup lang="ts">
import InfinityScroll from '@/components/comm/infinite/infinityScroll.vue';
import CardContainer from '@/components/modals/card/CardContainer.vue';
import { IColumnType } from '@/components/modals/types';
import type { IDynamicKeyValue } from '@/components/types';
import { useCommonStore } from '@/stores/common';
import { ref, watch } from 'vue';

const emits = defineEmits(['closeModal']);
const infFunc = useCommonStore().reqInfBrands;
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

const selectBrand = (target: IDynamicKeyValue, isChoice: boolean) => {
  emits('closeModal', target.id, target.name);
};
</script>

<style scoped></style>
