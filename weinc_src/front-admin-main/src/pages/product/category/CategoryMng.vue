<template>
  <PageNavigator :before_link="[]" :current="'카테고리 설정'" />
  <div class="card col-md-6">
    <div class="card-header pb-1">
      <div class="form-control-borderless h2">카테고리 설정</div>
    </div>
    <div class="card-body ps-8">
      <div class="label h2">
        <i class="bi bi-folder2-open" style="font-size: 22px"></i>[카테고리]
        <button type="button" class="btn btn-white btn-sm border-0 p-0" @click.prevent="openModal()" v-if="checkPermission('write:category')">
          <i class="bi bi-plus-square text-primary" style="font-size: 14px"></i>
        </button>
      </div>
      <div class="node">
        <tree-view v-for="item in list" :key="item.id" :id="item.id" :label="item.label" :nodes="item.nodes" @openModal="openModal" @openModModal="openModModal"> </tree-view>
      </div>
    </div>
  </div>
  <Modal :id="'regNewCategoryModal'" :title="'카테고리 신규 등록'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">카테고리를 신규 등록합니다.</div>
        <div class="pCatagory-area mb-3" v-if="pCategory.pLabel">
          <span>
            <b>[{{ pCategory.pLabel }}]</b>
            하위에 신규카테고리로 추가됩니다.
          </span>
        </div>
        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label text-md-center">카테고리명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control text-center col" v-model.trim="newValue" maxlength="45" placeholder="카테고리명을 입력해주세요." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="regNewCategory">확인</button>
    </template>
  </Modal>
  <Modal :id="'reqModCategoryModal'" :title="'카테고리 수정'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">
          수정할 카테고리 명을 입력해주세요. <span v-if="getUserClassStr.includes('CM')" class="ms-2"><MobilePushLink :title="`카테고리 [ ${newValue} ]`" :nextValue="`category/${mCategory.id}`" /></span>
        </div>

        <div class="card">
          <div class="card-body">
            <div class="row col mb-2 align-items-center">
              <label class="col-md-3 col-form-label text-center">카테고리명</label>
              <div class="col">
                <div class="input-group">
                  <input type="text" class="form-control text-center col" v-model.trim="newValue" maxlength="45" placeholder="카테고리명을 입력해주세요." />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
      <button type="button" class="btn btn-primary" @click.prevent="reqModCategory">확인</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import type { Nodes } from '@/pages/product/category/TreeView.vue';
import TreeView from '@/pages/product/category/TreeView.vue';
import { onMounted, reactive, ref } from 'vue';
import apis from '@/apis';
import { AxiosError } from 'axios';
import { apiResponseCheck, checkPermission, showAlert, showConfirm, showLogConsole, getUserClassStr, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';
import router from '@/router';

const list = ref([] as Array<Nodes>);
const newValue = ref('');
const pCategory = reactive({
  pid: 0,
  pLabel: '',
});
const mCategory = reactive({
  id: 0,
  label: '',
});

const getCategoryList = () => {
  apis.common.getCategories().then(res => {
    apiResponseCheck(res, () => {
      list.value = [];
      showLogConsole(res);
      for (const c of res) {
        list.value.push({ id: c.id, label: c.name, depth: c.depth });
      }
    });
  });
};

const openModal = (pid?: number, pLabel?: string) => {
  pCategory.pid = 0;
  pCategory.pLabel = '';
  newValue.value = '';

  if (pid && pLabel) {
    pCategory.pid = pid;
    pCategory.pLabel = pLabel;
  }
  showModal('regNewCategoryModal');
};

const closeModal = () => {
  hideModal('regNewCategoryModal');
  pCategory.pid = 0;
  pCategory.pLabel = '';
  newValue.value = '';
};

const openModModal = (cateId: number, label: string) => {
  mCategory.id = cateId;
  mCategory.label = label;
  newValue.value = JSON.parse(JSON.stringify(label));

  showModal('reqModCategoryModal');
};

const closeModModal = () => {
  mCategory.id = 0;
  mCategory.label = '';
  newValue.value = '';

  hideModal('reqModCategoryModal');
};

const reqModCategory = () => {
  if (newValue.value === mCategory.label) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('카테고리명을 변경하시겠습니까?', () => {
    apis.common.modCategory(mCategory.id, { name: newValue.value }).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('카테고리가 변경되었습니다.', 'success');
          closeModModal();
          getCategoryList();
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('reqModCategoryModal');
          }
        },
      );
    });
  });
};

const regNewCategory = () => {
  if (!newValue.value) {
    showAlert('신규 카테고리명을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('신규 카테고리를 등록하시겠습니까?', () => {
    const data: { pid?: number; name: string } = { name: newValue.value };
    if (pCategory.pLabel) {
      data['pid'] = pCategory.pid;
    }
    apis.common.addCategory(data).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('카테고리가 등록되었습니다.', 'success');
          closeModal();
          // getCategoryList();
          router.go(0);
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('regNewCategoryModal');
          }
        },
      );
    });
  });
};

onMounted(() => {
  getCategoryList();
});
</script>

<style scoped>
.node {
  margin-left: 20px;
}
</style>
