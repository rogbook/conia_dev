<template>
  <div class="card">
    <div class="card-header">
      <div class="nav">
        <div class="nav-item">
          <h4 class="card-title">상품 공통 정보</h4>
          <small>상품 설명에 표시될 상품 공통정보를 선택합니다.</small>
        </div>
        <div class="nav-item ms-auto">
          <button type="button" class="btn btn-warning" @click.prevent="onRegExplainInfo">저장</button>
        </div>
      </div>
    </div>
    <div class="card-body h-100">
      <div class="row align-items-center mb-3">
        <div class="col-auto">
          <label>상품공통정보 선택</label>
        </div>
        <div class="col-auto">
          <div class="tom-select-custom col-auto">
            <select class="form-select" v-model="selectedCommonId" @change="commonIdChanged" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option value="0" disabled>상품공통정보를 선택해주세요</option>
              <option v-for="common in commonInfoList" :key="common.id" v-text="common.name" :value="common.id"></option>
            </select>
          </div>
        </div>
        <div class="d-md-none mt-1"></div>
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-info" @click.prevent="showModal('CreateCommonInfo')">신규생성</button>
        </div>
      </div>

      <CKEditorCustom @receiveData="receiveData" ref="ckeditorCustom" :remove-items="removeItems" :editorData="editorValue" :disabled="true" />
    </div>
  </div>

  <Modal :id="'CreateCommonInfo'" :title="'상품공통정보 신규 등록'" :xlarge="true">
    <template #body>
      <div class="card">
        <div class="card-body">
          <div class="row col mb-4 align-items-center" v-if="getUserClassStr.includes('CM')">
            <label class="col-md-2 col-form-label">공급자(PA)</label>
            <div class="col-md-4">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="상폼공통정보명을 입력해주세요." :value="`${props?.prodMember?.name} (${props?.prodMember?.company?.name})`" disabled />
              </div>
            </div>
          </div>
          <div class="row col mb-4 align-items-center">
            <label class="col-md-2 col-form-label">상폼공통정보명</label>
            <div class="col-md-4">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="상폼공통정보명 입력해주세요." v-model.trim="commonInfo.name" />
              </div>
            </div>
          </div>
          <div class="row col mb-4 align-items-center">
            <label class="col-md-2 col-form-label">템플릿 선택</label>
            <div class="col-auto">
              <div class="tom-select-custom col-auto">
                <select class="form-select" v-model="selectTemplate" @change="templateChange" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="0" disabled>템플릿을 선택해주세요</option>
                  <option v-for="template in templateList" :key="template.id" v-text="template.name" :value="template.id"></option>
                </select>
              </div>
            </div>
          </div>
          <div class="common-info-contents">
            <label class="col-2 col-form-label text-nowrap">상품공통정보 내용</label>
            <CKEditorCustom @receiveData="newReceiveData" ref="newCkeditorCustom" :removeItems="['imageUpload']" :editor-data="editorData" />
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-sm btn-white" data-bs-dismiss="modal" @click.prevent="cancelNewCommon">닫기</button>
      <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveClick">저장</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import apis from '@/apis';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import type { ProdCommonInfo } from 'ProdCommonInfoListModule';
import Modal from '@/components/comm/modal.vue';
import { useUserStore } from '@/stores/user';
import { apiResponseCheck, getUserClassStr, showAlert, showConfirm, showModal, hideModal } from '@/utils/common-utils';
import type { Member } from 'ProductListInfoModule';
const props = defineProps<{ productId: number; commonId: number | null; prodMemberId: number; prodMember: Member }>();
const emits = defineEmits(['saveFinish', 'changedProdInfo']);
const userClass = computed(() => {
  return useUserStore().user.admin === 'Y' ? 'CM' : `${useUserStore().user.member_class}`;
});

const commonInfoList = ref([] as ProdCommonInfo[]);
const templateList = ref([] as ProdCommonInfo[]);
const selectedCommonId = ref(0);

const commonInfo = ref({} as ProdCommonInfo);
const newCkeditorCustom = ref();
const removeItems = ref(['heading', '|', 'bold', 'italic', 'fontSize', 'fontColor', 'fontFamily', 'fontBackgroundColor', '|', 'bulletedList', 'numberedList', '|', 'imageUpload', 'mediaEmbed', 'insertTable', 'link', '|', 'undo', 'redo']);
const editorData = ref('');

const editorValue = ref('');
const ckeditorCustom = ref();

const selectTemplate = ref(0);

const updateStatus = ref(false);
const receiveData = (contents: string) => {};
const newReceiveData = (data: string) => {
  if (!commonInfo.value.name) {
    showAlert('상품공통정보명을 입력해주세요.', 'warning');
    return;
  }
  if (!data.trim()) {
    showAlert('상품공통정보 내용을 입력해주세요.', 'warning');
    return;
  }

  //등록
  showConfirm('상품공통정보를 등록하시겠습니까?', () => {
    const obj: any = { name: commonInfo.value.name, contents: data };
    if (!userClass.value.includes('CM')) {
      obj['member_id'] = useUserStore().user.id;
    } else {
      obj['member_id'] = props.prodMemberId;
    }
    apis.common.reg_prod_common_info(obj).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('등록 되었습니다.\n새로 등록한 상품공통정보를 꼭 선택해주세요.', 'success');
          getCommonInfoList();
          hideModal('CreateCommonInfo');
        },
        (num?: number) => {
          if (num === 403) {
            hideModal('CreateCommonInfo');
          }
        },
      );
    });
  });
};

const cancelNewCommon = () => {
  commonInfo.value.name = '';
  selectTemplate.value = 0;
  newCkeditorCustom.value.cancelEdit();
};

const onRegExplainInfo = () => {
  if (selectedCommonId.value === 0) {
    showAlert('상품 공통 정보를 선택해주세요.', 'warning');
    return;
  }
  showConfirm('상품 공통 정보를 저장하시겠습니까?', () => {
    apis.product.updateBaseInfo(props.productId, { common_info_id: selectedCommonId.value }).then(res => {
      apiResponseCheck(res, () => {
        showAlert('상품 공통 정보가 저장되었습니다.', 'success');
        emits('changedProdInfo');
        emits('saveFinish', 'common');
      });
    });
  });
};

const commonIdChanged = () => {
  commonInfoList.value.map(item => {
    if (item.id === selectedCommonId.value) {
      editorValue.value = item.contents;
      return;
    }
  });
};

const templateChange = () => {
  templateList.value.map(item => {
    if (item.id === selectTemplate.value) {
      editorData.value = item.contents;
      commonInfo.value.name = item.name;
      return;
    }
  });
};

watch(
  () => props.commonId,
  id => {
    if (id) {
      selectedCommonId.value = id;
    }
  },
);

const getCommonInfoList = () => {
  let query = '';
  query = query.concat(`?member_id=${props.prodMemberId}`);
  apis.common.get_prod_common_info_list(query).then(res => {
    apiResponseCheck(res, () => {
      commonInfoList.value = res;
      commonIdChanged();
    });
  });
};

const getTemplate = () => {
  apis.common.get_prod_common_info_template(props.prodMemberId).then(res => {
    apiResponseCheck(res, () => {
      templateList.value = res;
    });
  });
};

// 상품 공통정보 신규 등록
const saveClick = () => {
  newCkeditorCustom.value.saveClicked();
};

const onStepActive = () => {
  getTemplate();
  if (props.productId) {
    getCommonInfoList();
  }
  if (props.commonId) {
    selectedCommonId.value = props.commonId;
  }
};

defineExpose({ onStepActive });
</script>

<style scoped></style>
