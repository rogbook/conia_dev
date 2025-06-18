<template>
  <div class="card">
    <div class="card-body">
      <!-- 세부검색어 입력 -->
      <div class="row col mb-2">
        <label class="col-2 col-form-label">세부검색</label>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" id="q" v-model="q" placeholder="검색할 배지명을 입력해주세요" />
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="text-end">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="getBadgeList">검색</button>
      </div>
    </div>
  </div>

  <span class="divider-center py-4">검색결과</span>

  <div class="row mb-2 align-items-center justify-content-between">
    <div class="col-auto">
      <span v-if="mBadgeList.length > 0">총 : {{ mBadgeList.length }}개</span>
    </div>
    <div class="col-auto">
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="addBadgeToProd">선택배지추가</button>
    </div>
  </div>
  <table class="table table-borderless table-thead-bordered table-align-middle card-table">
    <thead class="thead-light">
      <tr class="text-center">
        <th>선택</th>
        <th>배지명</th>
        <th>배지형태(예시)</th>
      </tr>
    </thead>
    <tbody>
      <tr class="text-center" v-for="s in mBadgeList" :key="s.id">
        <td>
          <input type="checkbox" class="form-check-input" name="cb_add_product" v-bind:id="`cb_p_${s.id}`" :value="s" v-model="mSelBadgeList" />
        </td>
        <td>
          {{ s.name }}
        </td>
        <td style="text-align: center">
          <span class="badge" :style="{ 'background-color': `${s.color} !important` }">{{ s.name }}</span>
        </td>
      </tr>
      <tr class="text-center" v-if="mBadgeList.length === 0">
        <td colspan="3">검색 결과가 없습니다.</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { computed, onMounted, PropType, ref } from 'vue';
import apis from '@/apis';
import type { BadgeInfo } from 'ProdBadgeInfo';
import { AxiosError } from 'axios';
import { apiResponseCheck, showAlert, showLogConsole } from '@/utils/common-utils';

const props = defineProps({
  currentList: {
    type: Array as PropType<BadgeInfo[]>,
    required: true,
    default: [] as BadgeInfo[],
  },
  previewList: {
    type: Array as PropType<BadgeInfo[]>,
    required: true,
    default: [] as BadgeInfo[],
  },
});

const emits = defineEmits(['addBadgeList']);

const q = ref('');
const mBadgeList = ref([] as BadgeInfo[]);

const mSelBadgeList = ref([] as BadgeInfo[]);

const availableCount = computed(() => {
  return 3 - props.currentList.length;
});

const getBadgeList = () => {
  let query = '';
  if (q.value) {
    query = query.concat(`name=${q.value}`);
  }

  apis.product.get_prod_badge_list(query).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      mBadgeList.value = res;
    });
  });
};

const addBadgeToProd = () => {
  if (mSelBadgeList.value.length === 0) {
    showAlert('선택한 배지가 없습니다.', 'warning');
    return;
  }
  if (mSelBadgeList.value.length > availableCount.value) {
    showAlert(`현재 최대 ${availableCount.value}개 까지만 추가할 수 있습니다.`, 'warning');
    return;
  }
  emits('addBadgeList', mSelBadgeList.value);
};

onMounted(() => {
  getBadgeList();

  //@ts-ignore
  document.getElementById('addBadgeModal').addEventListener('show.bs.modal', function (event) {
    mSelBadgeList.value = props.previewList;
  });

  //@ts-ignore
  document.getElementById('addBadgeModal').addEventListener('hide.bs.modal', function (event) {});
});
</script>

<style scoped></style>
