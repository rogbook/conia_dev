<template>
  <div class="card">
    <div class="card-body">
      <div class="row col mb-2 align-items-center">
        <label class="col-md-3 col-form-label">이름</label>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="이름을 입력해주세요." maxlength="8" v-model.trim="info.name" />
          </div>
        </div>
      </div>
      <div class="row col mb-2 align-items-center">
        <label class="col-md-3 col-form-label">전화번호</label>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="연락처를 입력해주세요. (숫자만 입력)" oninput="this.value = this.value.replace(/[^0-9]/g,'')" maxlength="20" v-model.trim="info.mobile" />
          </div>
        </div>
      </div>
      <div class="row col mb-2 align-items-center">
        <label class="col-md-3 col-form-label">회원식별값</label>
        <div class="col">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="식별값을 입력해주세요. (예: 사번)" maxlength="8" v-model.trim="info.unique_value" />
          </div>
        </div>
      </div>
      <div class="row col mb-2 align-items-center" v-if="isMod">
        <label class="col-md-3 col-form-label">사용여부</label>
        <div class="col">
          <div class="row">
            <div class="col-auto">
              <input type="radio" id="radio_used_y" class="form-check-input" name="used_yn" value="Y" v-model="info.used" />
              <label class="form-check-label px-1" for="radio_used_y">사용</label>
            </div>
            <div class="col-auto">
              <input type="radio" id="radio_used_n" class="form-check-input" name="used_yn" value="N" v-model="info.used" />
              <label class="form-check-label px-1" for="radio_used_n">미사용</label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import type { AbleTarget } from 'StoreAbleTargetModule';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import apis from '@/apis';
const props = defineProps<{ ableTarget: AbleTarget; store_code: string }>();
const emits = defineEmits(['closeAbleTargetPopup']);

const info = reactive({
  id: 0,
  name: '',
  mobile: '',
  unique_value: '',
  store_code: '',
  used: '',
});

const isMod = ref(false);
const oneRegAvailable = () => {
  showConfirm('상점이용가능자 정보를 등록하시겠습니까?', () => {
    apis.store.add_able_target_one(info.store_code, { name: info.name, mobile: info.mobile, unique_value: info.unique_value }).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('등록되었습니다.', 'success', () => {
            emits('closeAbleTargetPopup');
          });
        },
        (num?: number) => {
          if (num === 403) {
            emits('closeAbleTargetPopup');
          }
        },
      );
    });
  });
};

const modAbleTarget = () => {
  showConfirm('상점이용가능자 정보를 수정하시겠습니까?', () => {
    apis.store.mod_able_target(info.store_code, info.id, { name: info.name, mobile: info.mobile, unique_value: info.unique_value, used: info.used }).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('수정되었습니다.', 'success', () => {
            emits('closeAbleTargetPopup');
          });
        },
        (num?: number) => {
          if (num === 403) {
            emits('closeAbleTargetPopup');
          }
        },
      );
    });
  });
};

const clearInfo = () => {
  isMod.value = false;
  info.store_code = '';
  info.id = 0;
  info.name = '';
  info.mobile = '';
  info.unique_value = '';
  info.used = '';
};

onMounted(() => {
  //@ts-ignore
  document.getElementById('oneRegModal').addEventListener('show.bs.modal', () => {
    clearInfo();
    info.store_code = props.store_code;
    if (props.ableTarget.id) {
      isMod.value = true;
      info.id = props.ableTarget.id;
      info.store_code = props.ableTarget.store_code;
      info.name = props.ableTarget.name;
      info.mobile = props.ableTarget.mobile;
      info.unique_value = props.ableTarget.unique_value;
      info.used = props.ableTarget.used;
    }
  });
  //@ts-ignore
  document.getElementById('oneRegModal').addEventListener('hide.bs.modal', () => {});
});

defineExpose({ oneRegAvailable, modAbleTarget });
</script>

<style scoped></style>
