<template>
  <Modal :cancel-btn-handler="resetAllState" :id="modalId" :title="modalName + ' 검색'" :xlarge="true">
    <template #body>
      <div class="row">
        <CardContainer :title="modalName + ' 선택'" :columnType="IColumnType.DEFAULT" :noFooter="true">
          <template #header>
            <div class="input-group">
              <input v-model="search" type="text" class="form-control" :placeholder="'브랜드 검색'" @keypress.enter.prevent="onSearchAction" @change="onChangeAction" />
              <button type="button" @click.prevent="onSearchAction" class="btn w-25 btn-secondary">검색</button>
            </div>
          </template>
          <suspense>
            <InfinityScroll :search="search" :searchMode="searchMode" :to-show="30" :async-function="infFunc" @clickList="target => onChoice(target, true)" />
            <template #fallback>
              <p>Loading...</p>
            </template>
          </suspense>
        </CardContainer>
        <CardContainer :title="'선택된' + modalName" :noFooter="true">
          <ul class="list-group list-group-flush">
            <li v-for="c in choose" :key="JSON.stringify(c)" class="list-group-item list-group-item-action d-flex justify-content-between align-items-start border-bottom">
              {{ c.name }}
              <button type="button" class="btn btn-close" @click.prevent="() => onChoice(c, false)"></button>
            </li>
          </ul>
        </CardContainer>
      </div>
    </template>
    <template #footer>
      <button
        type="button"
        class="btn btn-secondary"
        data-bs-dismiss="modal"
        @click.prevent="
          () =>
            emits(
              'choice',
              choose.map(c => c),
            )
        ">
        적용
      </button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import type { IDynamicKeyValue } from '@/components/types';
import { ref, watch } from 'vue';
import { useCommonStore } from '@/stores/common';
import InfinityScroll from '@/components/comm/infinite/infinityScroll.vue';
import type { COLUMN_SELECTION, COLUMN_SELECTION_ID } from '@/components/modals/types';
import { IColumnType } from '@/components/modals/types';
import CardContainer from '@/components/modals/card/CardContainer.vue';

/**
 need to use commonStore getter name properties with array
 this library link with commonStore only.
 */
const infFunc = useCommonStore().reqInfBrands;
const choose = ref<IDynamicKeyValue[]>([]);

const props = defineProps<{ modalName: string; modalId: COLUMN_SELECTION_ID; parent: IDynamicKeyValue[]; selected: IDynamicKeyValue[]; type: COLUMN_SELECTION }>();

const searchMode = ref<boolean>(false);

const search = ref('');

watch(
  () => props.selected,
  select => {
    //@ts-ignore
    choose.value = select;
  },
);

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

const onChoice = (target: IDynamicKeyValue, isChoice: boolean) => {
  if (isChoice) {
    for (const c of choose.value) {
      if (c.id === target.id) return;
    }
    choose.value.push(target);
  } else {
    choose.value = choose.value.filter((c: IDynamicKeyValue) => {
      if (c.id !== target.id) return c;
    });
  }
  emits(
    'choice',
    choose.value.map(c => c),
  );
};
const resetAllState = () => {
  choose.value = props.parent.map(i => i);
};

const emits = defineEmits(['choice']);
</script>

<style scoped></style>
