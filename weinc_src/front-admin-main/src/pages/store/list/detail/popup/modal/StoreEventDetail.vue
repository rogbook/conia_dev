<template>
  <div class="row">
    <div class="card">
      <div class="card-header">
        <div class="text-start" v-if="!isMod">팝업 신규등록</div>
        <div class="text-start" v-else>팝업 수정</div>
      </div>
      <div class="card-body row">
        <div class="col-lg">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-labelr">
              팝업이미지
              <span style="font-size: 0.7rem" class="text-danger">(추천 가로 500px)</span>
              <div v-if="mStorePopup.img" class="mt-3">
                <button type="button" class="btn btn-outline-info btn-sm" @click="mStorePopup.img = ''">수정</button>
              </div>
            </label>
            <div class="col">
              <div v-if="!mStorePopup.img" id="basicExampleDropzone" class="js-dropzone row dz-dropzone dz-dropzone-card py-10 mx-auto">
                <label for="img-input-file" style="cursor: pointer">
                  <div class="dz-message">
                    <img class="avatar avatar-xl avatar-4x3 mb-3" src="@/assets/svg/illustrations/oc-browse.svg" alt="Image Description" />
                    <h5>이미지를 선택해 주세요.</h5>
                    <label class="btn btn-white btn-sm" for="img-input-file">이미지 선택</label>
                    <input type="file" id="img-input-file" class="visually-hidden" @change="onRegistComRegPhoto" accept="image/.JPEG, .jpg, .png" />
                  </div>
                </label>
              </div>
              <div v-else>
                <img class="img-fluid d-block mx-auto" :src="mStorePopup.img" alt="팝업 이미지" />
              </div>
            </div>
          </div>
        </div>
        <hr class="px-0 ms-2 me-2 d-none d-lg-block" />
        <div class="col-lg">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">제목</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control col" v-model.trim="mStorePopup.title" placeholder="제목을 입력해주세요." maxlength="20" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">내용</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control col" v-model.trim="mStorePopup.contents" placeholder="내용을 입력해주세요." maxlength="100" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">링크</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control col" v-model.trim="mStorePopup.link" placeholder="링크를 입력해주세요." maxlength="512" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">노출순서</label>
            <div class="col">
              <!-- Select -->
              <div class="tom-select-custom">
                <select class="form-select" v-model="mStorePopup.sort" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
                  <option v-for="i in 99" :key="i" :value="i">{{ i }}</option>
                </select>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">노출시작일</label>
            <div class="col">
              <div class="input-group">
                <div class="form-group">
                  <div id="startDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#startDatepicker","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                    <div class="input-group-prepend input-group-text" data-bs-toggle>
                      <i class="bi-calendar-week"></i>
                    </div>
                    <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="mStorePopup.view_start_date" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">노출종료일</label>
            <div class="col">
              <div class="input-group">
                <div class="form-group">
                  <div id="endDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#endDatepicker","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                    <div class="input-group-prepend input-group-text" data-bs-toggle>
                      <i class="bi-calendar-week"></i>
                    </div>
                    <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="mStorePopup.view_end_date" />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="isMod">
            <label class="col-md-2 col-form-label">노출여부</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_status_y" type="radio" class="form-check-input" name="radio_status" value="Y" v-model="mStorePopup.status" />
                <label class="form-check-label" for="radio_status_y">노출</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_status_n" type="radio" class="form-check-input" name="radio_status" value="N" v-model="mStorePopup.status" />
                <label class="form-check-label" for="radio_status_n">비노출</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">하위상점 표시여부</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_duplicate_y" type="radio" class="form-check-input" name="radio_duplicate" value="Y" v-model="mStorePopup.duplicate" />
                <label class="form-check-label" for="radio_duplicate_y">사용</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_duplicate_n" type="radio" class="form-check-input" name="radio_duplicate" value="N" v-model="mStorePopup.duplicate" />
                <label class="form-check-label" for="radio_duplicate_n">사용안함</label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-footer pb-2">
    <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    <button type="button" class="btn btn-primary" @click.prevent="addStorePopup" v-if="!isMod">등록</button>
    <button type="button" class="btn btn-warning" @click.prevent="modStorePopup" v-else>수정</button>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm } from '@/utils/common-utils';
import UploadImage from '@/components/comm/uploadImage.vue';

import type { Popup } from 'StorePopupInfoModule';
import { ErrorTypes } from 'vue-router';

const props = defineProps<{
  storeCode: string;
  selectedPopup: Popup | null;
}>();
const emits = defineEmits(['closePopupModal']);

const mStorePopup = ref({} as Popup);
const mOriginStorePopup = ref({} as Popup);
const sfp = ref();
const efp = ref();

const isMod = ref(false);

onMounted(() => {
  //@ts-ignore
  document.getElementById('addPopupModal').addEventListener('show.bs.modal', function (event) {
    //@ts-ignore
    sfp.value = flatpickr(document.querySelector('#startDatepickerInput'), { enableTime: true, time_24hr: true, static: true, onClose: () => sDateChange() });
    //@ts-ignore
    efp.value = flatpickr(document.querySelector('#endDatepickerInput'), { enableTime: true, time_24hr: true, static: true, onClose: () => eDateChange() });
    if (props.storeCode) {
      sfp.value.clear();
      efp.value.clear();

      if (props.selectedPopup) {
        isMod.value = true;
        mStorePopup.value = JSON.parse(JSON.stringify(props.selectedPopup));
        mOriginStorePopup.value = JSON.parse(JSON.stringify(props.selectedPopup));

        mStorePopup.value.view_start_date = mStorePopup.value.view_start_date.replace('T', ' ').slice(0, -3);
        mStorePopup.value.view_end_date = mStorePopup.value.view_end_date.replace('T', ' ').slice(0, -3);
        mOriginStorePopup.value.view_start_date = mOriginStorePopup.value.view_start_date.replace('T', ' ').slice(0, -3);
        mOriginStorePopup.value.view_end_date = mOriginStorePopup.value.view_end_date.replace('T', ' ').slice(0, -3);

        sfp.value.jumpToDate(mOriginStorePopup.value.view_start_date);
        sfp.value.setDate(mOriginStorePopup.value.view_start_date);
        efp.value.jumpToDate(mOriginStorePopup.value.view_end_date);
        efp.value.setDate(mOriginStorePopup.value.view_end_date);
      } else {
        sfp.value.jumpToDate(new Date());
        sfp.value.setDate(new Date());
        efp.value.jumpToDate(new Date());
        efp.value.setDate(new Date());

        isMod.value = false;
        mStorePopup.value = {} as Popup;
        mStorePopup.value.duplicate = 'N';
        mStorePopup.value.sort = 99;
      }
    }
  });
});
const sDateChange = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning', () => {
        sfp.value.setDate(new Date(eDate), true, 'Y-m-d');
      });
    }
  }
};
const eDateChange = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning', () => {
        efp.value.setDate(new Date(sDate), true, 'Y-m-d');
      });
    }
  }
};

const checkValidation = () => {
  if (!mStorePopup.value.img) {
    showAlert('이미지를 선택해주세요.', 'warning');
    return;
  }
  if (!mStorePopup.value.title) {
    showAlert('제목을 입력해주세요.', 'warning');
    return;
  }
  if (!mStorePopup.value.contents) {
    showAlert('내용을 입력해주세요.', 'warning');
    return;
  }
  if (!mStorePopup.value.link) {
    showAlert('링크를 입력해주세요.', 'warning');
    return;
  }
  if (mStorePopup.value.sort < 1 || mStorePopup.value.sort > 99) {
    showAlert('순서는 1부터 99까지만 가능합니다.', 'warning');
    return;
  }
  if (!mStorePopup.value.view_start_date) {
    showAlert('노출시작일을 입력해주세요.', 'warning');
    return;
  }
  if (!mStorePopup.value.view_end_date) {
    showAlert('노출종료일을 입력해주세요.', 'warning');
    return;
  }
  if (mStorePopup.value.view_start_date > mStorePopup.value.view_end_date) {
    showAlert('시작일이 종료일보다 큽니다.', 'warning');
    return;
  }
  return true;
};

const onRegistComRegPhoto = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target && target.files) {
    apis.common.upload_photo(target.files[0], 'store/popup/').then(res => {
      apiResponseCheck(res, () => {
        mStorePopup.value.img = res.uri;
      });
    });
  }
};

const addStorePopup = () => {
  if (!checkValidation()) return;
  mStorePopup.value.store_code = props.storeCode;
  showConfirm('팝업을 등록하시겠습니까?', () => {
    apis.store.reg_store_popup(mStorePopup.value.store_code, mStorePopup.value).then(res => {
      apiResponseCheck(
        res,
        () => {
          if (res.msg === 'success') {
            showAlert('팝업이 등록되었습니다.', 'success');
            emits('closePopupModal');
          }
        },
        (num?: number) => {
          if (num === 403) {
            emits('closePopupModal');
          }
        },
      );
    });
  });
};

const modStorePopup = () => {
  let data = {} as any;

  if (mStorePopup.value.img !== mOriginStorePopup.value.img) {
    data['img'] = mStorePopup.value.img;
  }
  if (mStorePopup.value.title !== mOriginStorePopup.value.title) {
    data['title'] = mStorePopup.value.title;
  }
  if (mStorePopup.value.contents !== mOriginStorePopup.value.contents) {
    data['contents'] = mStorePopup.value.contents;
  }
  if (mStorePopup.value.link !== mOriginStorePopup.value.link) {
    data['link'] = mStorePopup.value.link;
  }
  if (mStorePopup.value.sort !== mOriginStorePopup.value.sort) {
    data['sort'] = mStorePopup.value.sort;
  }
  if (mStorePopup.value.view_start_date !== mOriginStorePopup.value.view_start_date) {
    data['view_start_date'] = mStorePopup.value.view_start_date;
  }
  if (mStorePopup.value.view_end_date !== mOriginStorePopup.value.view_end_date) {
    data['view_end_date'] = mStorePopup.value.view_end_date;
  }
  if (mStorePopup.value.duplicate !== mOriginStorePopup.value.duplicate) {
    data['duplicate'] = mStorePopup.value.duplicate;
  }
  if (mStorePopup.value.status !== mOriginStorePopup.value.status) {
    data['status'] = mStorePopup.value.status;
  }
  if (Object.keys(data).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('팝업 정보를 수정하시겠습니까?', () => {
    apis.store.mod_store_popup(props.storeCode, mStorePopup.value.id, data).then(res => {
      apiResponseCheck(
        res,
        () => {
          showAlert('팝업 정보가 수정되었습니다.', 'success', () => {
            emits('closePopupModal');
          });
        },
        (num?: number) => {
          if (num === 403) {
            emits('closePopupModal');
          }
        },
      );
    });
  });
};
</script>

<style scoped>
hr {
  border: none;
  border-left: 1px solid hsla(200, 10%, 50%, 100);
  height: 47vh;
  width: 1px;
}

.flatpickr-wrapper {
  display: block !important;
}
</style>
