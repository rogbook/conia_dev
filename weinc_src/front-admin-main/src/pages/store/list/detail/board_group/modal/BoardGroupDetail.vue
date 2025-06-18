<template>
  <div class="row">
    <div class="card">
      <div class="card-header">
        <div class="text-start" v-if="!isMod">게시판 신규등록</div>
        <div class="text-start" v-else>게시판 수정</div>
      </div>
      <div class="card-body row">
        <div class="col">
          <div class="row col mb-2 align-items-center">
            <label class="col-2 col-form-label">제목</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control col" v-model="mStoreBoardGroup.name" placeholder="제목을 입력해주세요." />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-2 col-form-label">노출타입</label>
            <div class="col">
              <div class="tom-select-custom">
                <select class="form-select" v-model="mStoreBoardGroup.view_type" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option value="">노출타입을 선택해 주세요.</option>
                  <option value="thumbnail">썸네일</option>
                  <option value="banner">배너</option>
                </select>
              </div>
            </div>
          </div>

          <div class="row col mb-2 align-items-center">
            <label class="col-2 col-form-label">순서</label>
            <div class="col">
              <div class="tom-select-custom">
                <select class="form-select" v-model="mStoreBoardGroup.sort" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option v-for="i in 99" :key="i" :value="i">{{ i }}</option>
                </select>
              </div>
            </div>
          </div>

          <div class="row col mb-2 align-items-center">
            <label class="col-2 col-form-label">메뉴 노출여부</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_menu_visible_y" type="radio" class="form-check-input" name="radio_menu_visible" value="Y" v-model="mStoreBoardGroup.menu_visible" />
                <label class="form-check-label" for="radio_menu_visible_y">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_menu_visible_n" type="radio" class="form-check-input" name="radio_menu_visible" value="N" v-model="mStoreBoardGroup.menu_visible" />
                <label class="form-check-label" for="radio_menu_visible_n">사용안함</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-2 col-form-label">기간지난 컨텐츠 노출여부</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_view_end_content_y" type="radio" class="form-check-input" name="radio_view_end_content" value="Y" v-model="mStoreBoardGroup.view_end_content" />
                <label class="form-check-label" for="radio_view_end_content_y">노출</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_view_end_content_n" type="radio" class="form-check-input" name="radio_view_end_content" value="N" v-model="mStoreBoardGroup.view_end_content" />
                <label class="form-check-label" for="radio_view_end_content_n">비노출</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-footer pb-2">
    <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    <button type="button" class="btn btn-primary" @click.prevent="addStoreBoardGroup" v-if="!isMod">등록</button>
    <button type="button" class="btn btn-warning" @click.prevent="modStoreBoardGroup" v-else>수정</button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import type { BoardGroup } from 'StoreBoardGroupInfoModule';

const props = defineProps<{
  storeCode: string;
  selectedBoardGroup: BoardGroup | null;
}>();
const emits = defineEmits(['closeBoardGroupModal']);

const mStoreBoardGroup = ref({} as BoardGroup);
const mOriginStoreBoardGroup = ref({} as BoardGroup);
const isMod = ref(false);

onMounted(() => {
  //@ts-ignore
  document.getElementById('addBoardGroupModal').addEventListener('show.bs.modal', function (event) {
    if (props.storeCode) {
      if (props.selectedBoardGroup) {
        isMod.value = true;
        mStoreBoardGroup.value = JSON.parse(JSON.stringify(props.selectedBoardGroup));
        mOriginStoreBoardGroup.value = JSON.parse(JSON.stringify(props.selectedBoardGroup));
      } else {
        isMod.value = false;
        mStoreBoardGroup.value.name = '';
        mStoreBoardGroup.value.view_type = '';
        mStoreBoardGroup.value.menu_visible = 'N';
        mStoreBoardGroup.value.view_end_content = 'N';
        mStoreBoardGroup.value.sort = 99;
      }
    }
  });
});

const checkValidation = () => {
  if (!mStoreBoardGroup.value.name) {
    showAlert('제목을 입력해주세요.', 'warning');
    return;
  }
  if (!mStoreBoardGroup.value.view_type) {
    showAlert('노출타입을 선택해주세요.', 'warning');
    return;
  }
  return true;
};

const addStoreBoardGroup = () => {
  if (!checkValidation()) return;
  mStoreBoardGroup.value.store_code = props.storeCode;
  showConfirm('게시판을 생성하시겠습니까?', () => {
    apis.store.reg_store_board_group(mStoreBoardGroup.value.store_code, mStoreBoardGroup.value).then(res => {
      apiResponseCheck(
        res,
        () => {
          if (res.msg === 'success') {
            showAlert('게시판이 생성되었습니다.', 'success');
            emits('closeBoardGroupModal');
          }
        },
        (num?: number) => {
          if (num === 403) {
            emits('closeBoardGroupModal');
          }
        },
      );
    });
  });
};

const modStoreBoardGroup = () => {
  if (!checkValidation()) return;
  let data = {} as any;

  if (mStoreBoardGroup.value.name !== mOriginStoreBoardGroup.value.name) {
    data['name'] = mStoreBoardGroup.value.name;
  }
  if (mStoreBoardGroup.value.view_type !== mOriginStoreBoardGroup.value.view_type) {
    data['view_type'] = mStoreBoardGroup.value.view_type;
  }
  if (mStoreBoardGroup.value.sort !== mOriginStoreBoardGroup.value.sort) {
    data['sort'] = mStoreBoardGroup.value.sort;
  }
  if (mStoreBoardGroup.value.menu_visible !== mOriginStoreBoardGroup.value.menu_visible) {
    data['menu_visible'] = mStoreBoardGroup.value.menu_visible;
  }
  if (mStoreBoardGroup.value.view_end_content !== mOriginStoreBoardGroup.value.view_end_content) {
    data['view_end_content'] = mStoreBoardGroup.value.view_end_content;
  }
  if (Object.keys(data).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }
  showConfirm('게시판 정보를 수정하시겠습니까?', () => {
    apis.store.mod_store_board_group(props.storeCode, mStoreBoardGroup.value.id, data).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('게시판 정보가 수정되었습니다.', 'success', () => {
            emits('closeBoardGroupModal');
          });
        },
        (num?: number) => {
          if (num === 403) {
            emits('closeBoardGroupModal');
          }
        },
      );
    });
  });
};
</script>
