<template>
  <Modal :id="modalId" :title="modalName + ' 검색'" :xxlarge="true">
    <template #body>
      <div class="row">
        <CardList @choice="onChoice" :my-order="MULTI_COLUMN_ORDER.FIRST" :s-id="currentId" :current-order="currentOrder" :asyncFunction="reqCategories" :modal-name="'1차 ' + modalName" :columnType="IColumnType.FOUR" :type="props.type" />
        <CardList @choice="onChoice" :my-order="MULTI_COLUMN_ORDER.SECOND" :s-id="currentId" :current-order="currentOrder" :asyncFunction="reqCategories" :modal-name="'2차 ' + modalName" :columnType="IColumnType.FOUR" :type="props.type" />
        <CardList @choice="onChoice" :my-order="MULTI_COLUMN_ORDER.THIRD" :s-id="currentId" :current-order="currentOrder" :asyncFunction="reqCategories" :modal-name="'3차 ' + modalName" :columnType="IColumnType.FOUR" :type="props.type" />
        <CardList @choice="onChoice" :my-order="MULTI_COLUMN_ORDER.FOURTH" :s-id="currentId" :current-order="currentOrder" :asyncFunction="reqCategories" :modal-name="'4차 ' + modalName" :columnType="IColumnType.FOUR" :type="props.type" />
        <CardContainer :title="'선택된 ' + modalName" :columnType="IColumnType.DEFAULT" :noFooter="true">
          <template #header>
            <div class="row align-items-center border-bottom py-2 mb-2" v-if="choose.length > 0">
              <div class="col-auto text-primary h4 bold">{{ arrayToStringWithComma(choose, 'name', ' > ') }}</div>
              <div class="col-auto">
                <button type="button" @click="selectCategory" class="btn btn-sm badge btn-info">카테고리 목록 추가</button>
              </div>
            </div>
            <small class="">모든 카테고리를 선택하지 않아도 카테고리로 지정할 수 있습니다.</small>
          </template>
          <small>[추가할 카테고리 목록]</small>
          <ul class="list-group list-group-sm list-group-flush overflow-auto mb-0 mt-2" style="height: 16vh">
            <li selectedCategories @click.prevent="" v-for="(cate, selectedIdx) in selectedCategories" :key="JSON.stringify(cate)" class="list-group-item list-group-item-action d-flex justify-content-between align-items-start border-bottom">
              <span class="h4 bold">{{ arrayToStringWithComma(cate, 'name', ' > ') }}</span>
              <button type="button" @click.prevent="() => onCancelSelected(selectedIdx)" class="btn btn-close text-danger"></button>
            </li>
          </ul>
          <template #footer> </template>
        </CardContainer>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-success col-1" data-bs-dismiss="modal" @click.prevent="() => emits('choice', selectedCategories)">적용</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import type { IDynamicKeyValue } from '@/components/types';
import { onMounted, ref, watch } from 'vue';
import { useCommonStore } from '@/stores/common';
import { IColumnType, MULTI_COLUMN_ORDER } from '@/components/modals/types';
import type { COLUMN_SELECTION, COLUMN_SELECTION_ID } from '@/components/modals/types';
import CardContainer from '@/components/modals/card/CardContainer.vue';
import CardList from '@/components/modals/card/CardList.vue';
import { arrayToStringWithComma } from '@/utils/arrayParser';

/**
 need commonStore getter name properties with array
 */

const reqCategories = useCommonStore().reqCategories;
const choose = ref<IDynamicKeyValue[]>([]);

const currentOrder = ref<MULTI_COLUMN_ORDER>();
const currentId = ref(0);
const selectedCategories = ref<IDynamicKeyValue[][]>([]);

onMounted(() => {
  currentOrder.value = MULTI_COLUMN_ORDER.FIRST;
});

const props = defineProps<{ modalName: string; modalId: COLUMN_SELECTION_ID; parent: IDynamicKeyValue[]; selected: IDynamicKeyValue[]; type: COLUMN_SELECTION }>();
// const commonStore = useCommonStore();

const search = ref('');

const onChoice = ({ target, order }: { target: { id: number } & IDynamicKeyValue; order: MULTI_COLUMN_ORDER }) => {
  currentId.value = target.id;
  choose.value.splice(order);
  choose.value.push(target);
  if (order === MULTI_COLUMN_ORDER.FOURTH) {
    selectCategory();
  } else {
    currentOrder.value = order + 1;
  }
};

const selectCategory = () => {
  for (let i = 0; i < choose.value.length; i++) {
    const tmp = [];
    for (let j = 0; j <= i; j++) {
      // tmp.push(choose.value[j]);
      tmp.push({ id: choose.value[j].id, name: choose.value[j].name });
    }
    selectedCategories.value.push(tmp);
  }
  selectedCategories.value = Array.from(new Set(selectedCategories.value.map(a => JSON.stringify(a))), json => JSON.parse(json));
  // selectedCategories.value.push(choose.value);
  choose.value = [];
  currentOrder.value = MULTI_COLUMN_ORDER.FIRST;
  currentId.value = 0;
};

const onCancelSelected = (selectedIdx: number) => {
  selectedCategories.value = selectedCategories.value.filter((sc, idx) => {
    if (selectedIdx !== idx) return sc;
  });
};

const emits = defineEmits(['choice']);

watch(
  () => props.selected,
  select => {
    //@ts-ignore
    selectedCategories.value = select;
  },
);
</script>

<style scoped></style>
