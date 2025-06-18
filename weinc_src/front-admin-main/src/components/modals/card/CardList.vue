<template>
  <CardContainer :title="modalName" :columnType="props.columnType" :noFooter="true">
    <template #header>
      <input v-model="search" @keyup="onSearchKeyDown" type="text" class="form-control" placeholder="검색" />
    </template>
    <ul class="list-group list-group-sm list-group-flush overflow-auto" style="height: 26vh">
      <li @click.prevent="() => onChoice(c)" v-for="c in canChoice" :key="JSON.stringify(c)" class="list-group-item list-group-item-action d-flex justify-content-between align-items-start">
        {{ c.name }}
      </li>
    </ul>
    <template #footer>{{}}</template>
  </CardContainer>
</template>

<script setup lang="ts">
import CardContainer from '@/components/modals/card/CardContainer.vue';
import type { IDynamicKeyValue } from '@/components/types';
import { ref, watch } from 'vue';
import type { COLUMN_SELECTION, IColumnType, MULTI_COLUMN_ORDER } from '@/components/modals/types';

const props = defineProps<{ sId?: number; currentOrder: MULTI_COLUMN_ORDER | undefined; myOrder: MULTI_COLUMN_ORDER; asyncFunction: (params: { pid?: number }) => Promise<unknown[]>; modalName: string; type: COLUMN_SELECTION; columnType: IColumnType }>();

const emits = defineEmits(['choice']);

const storedData = ref();
const search = ref('');
const canChoice = ref();

watch(
  () => [props.currentOrder, props.sId],
  ([co, id]) => {
    if (co === props.myOrder) {
      getData(id);
    } else if (co < props.myOrder) {
      canChoice.value = null;
    }
  },
);

const getData = async (pid = 0) => {
  storedData.value = await props.asyncFunction({ pid });
  canChoice.value = storedData.value;
};

const onChoice = (target: IDynamicKeyValue) => {
  emits('choice', { target, order: props.myOrder });
};
const onSearchKeyDown = () => {
  canChoice.value = storedData.value.filter((item: { [key: string]: unknown; name: string }) => item.name.includes(search.value) && item);
};
</script>

<style scoped></style>
