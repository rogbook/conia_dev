<template>
  <PageNavigator :before_link="[]" :current="'상품배지관리'" />
  <div class="card col-md-8">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">상품배지관리</div>
    </div>
    <div class="card-body">
      <div class="text-end mb-3">
        <button type="button" class="btn btn-sm btn-primary" @click.prevent="showModal('BadgeCreateModal')">상품배지생성</button>
      </div>
      <div class="table-responsive">
        <table class="table table-nowrap table-align-middle border card-table table-vertical-border-striped table-bordered">
          <thead class="thead-light">
            <tr class="text-center">
              <th>배지명</th>
              <th>형태</th>
              <th>색상</th>
              <th style="width: 10%">수정</th>
            </tr>
          </thead>
          <tbody>
            <tr class="text-center" v-for="(item, i) in badgeList" :key="item.id">
              <td>{{ item.name }}</td>
              <td>{{ item.shape }}</td>
              <td class="text-center">
                <div class="badge" style="width: 30%" :style="{ 'background-color': item.color }">&nbsp;</div>
              </td>
              <td>
                <button type="button" class="btn btn-sm btn-outline-info" @click.prevent="badgeDetail(i)">수정</button>
              </td>
            </tr>
            <tr v-if="badgeList.length === 0">
              <td colspan="4" class="text-center">표시항 항목이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- 옵션 생성 Modal -->
  <Modal :id="'BadgeCreateModal'" :title="selectedBadge.id === 0 ? `상품배지생성` : '상품배지수정'" :xlarge="false">
    <template #body>
      <div class="row col mb-3 align-items-center">
        <label class="col-md-2 col-form-label">배지명</label>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control col" v-model.trim="selectedBadge.name" placeholder="상품 배지명을 입력해주세요.(최대 8자)" maxlength="8" />
          </div>
        </div>
      </div>
      <div class="row col mb-3 align-items-center">
        <label class="col-md-2 col-form-label">배지색상</label>
        <div class="col-auto">
          <ColorInput v-model="colors" format="hex string" />
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-info" @click.prevent="selectColor">선택완료</button>
        </div>
      </div>
      <div class="row col mb-3 align-items-center">
        <label class="col-md-2 col-form-label">배지형태</label>
        <div class="col-md-4">
          <!-- Select -->
          <div class="tom-select-custom">
            <select class="form-select" v-model="selBadgeShape.selectedItem" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="detail in selBadgeShape.items" :key="JSON.stringify(detail)" v-text="detail.name" :value="detail.value"></option>
            </select>
          </div>
          <!-- End Select -->
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-primary" @click.prevent="createBadge" v-if="selectedBadge.id === 0">생성</button>
      <button type="button" class="btn btn-primary" @click.prevent="modBadge" v-if="selectedBadge.id !== 0">수정</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/comm/modal.vue';
import { onMounted, reactive, Ref, ref } from 'vue';
import type { BadgeInfo } from 'ProdBadgeInfo';
import ColorInput from 'vue-color-input/dist/color-input.esm';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import apis from '@/apis';
import { AxiosError } from 'axios';
import PageNavigator from '@/components/title/PageNavigator.vue';

const colors = ref('#000000');

const selectedBadge = reactive({
  id: 0,
  name: '',
  img: '',
  color: '',
  shape: 'rect',
  listIdx: -1,
});

const selBadgeShape = reactive({
  items: [{ name: '사각형', value: 'rect' }],
  selectedItem: 'rect',
});

const badgeList: Ref<BadgeInfo[]> = ref([]);

const createBadge = () => {
  if (!selectedBadge.name) {
    showAlert('배지명을 입력해주세요', 'warning');
    return;
  }

  showConfirm('상품 배지를 등록하시겠습니까?', () => {
    apis.product.add_prod_badge({ name: selectedBadge.name, color: colors.value, shape: selBadgeShape.selectedItem }).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('상품 배지가 등록되었습니다.', 'success');
          hideModal('BadgeCreateModal');
          getBadgeList();
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('BadgeCreateModal');
          }
        },
      );
    });
  });
};

const modBadge = () => {
  if (selectedBadge.id === 0 || selectedBadge.listIdx < 0) {
    return;
  }
  if (!selectedBadge.name) {
    showAlert('배지명을 입력해주세요', 'warning');
    return;
  }

  let data: any = {};
  const origin = badgeList.value[selectedBadge.listIdx];

  if (selectedBadge.name !== origin.name) {
    data['name'] = selectedBadge.name;
  }

  if (origin.color !== colors.value) {
    data['color'] = colors.value;
  }

  if (selBadgeShape.selectedItem !== origin.shape) {
    data['shape'] = selBadgeShape.selectedItem;
  }

  showConfirm('상품 배지를 수정하시겠습니까?', () => {
    apis.product.mod_prod_badge(selectedBadge.id, data).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('상품 배지가 수정되었습니다.', 'success');
          hideModal('BadgeCreateModal');
          getBadgeList();
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('BadgeCreateModal');
          }
        },
      );
    });
  });
};

const getBadgeList = () => {
  apis.product.get_prod_badge_list().then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      badgeList.value = res;
    });
  });
};

const clearSelectBadgeInfo = () => {
  selectedBadge.id = 0;
  selectedBadge.listIdx = -1;
  selectedBadge.name = '';
  selectedBadge.img = '';
  selectedBadge.color = '';
  selectedBadge.shape = 'rect';
  colors.value = '#000000';
};

const badgeDetail = (idx: number) => {
  const badge = badgeList.value[idx];
  selectedBadge.listIdx = idx;
  selectedBadge.id = badge.id;
  selectedBadge.name = badge.name;
  selectedBadge.img = badge.img;
  selectedBadge.color = badge.color;
  colors.value = selectedBadge.color;
  selectedBadge.shape = badge.shape;
  selBadgeShape.selectedItem = badge.shape;

  showModal('BadgeCreateModal');
};

const selectColor = () => {};

onMounted(() => {
  getBadgeList();

  //@ts-ignore
  document.getElementById('BadgeCreateModal').addEventListener('show.bs.modal', function (event) {});

  //@ts-ignore
  document.getElementById('BadgeCreateModal').addEventListener('hide.bs.modal', function (event) {
    clearSelectBadgeInfo();
  });
});
</script>

<style scoped>
.color-input {
  display: inherit !important;
}
</style>
