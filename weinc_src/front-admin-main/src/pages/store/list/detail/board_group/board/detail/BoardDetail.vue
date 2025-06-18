<template>
  <PageNavigator :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세', '이벤트 관리'] : ['상점 관리', '상점관리 상세', '이벤트 관리']" :current="boardId ? '이벤트 상세' : '이벤트 생성'" />
  <div class="card">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">{{ boardId ? `이벤트 상세` : `이벤트 생성` }}</div>
          <span v-if="getUserClassStr.includes('CM')"><MobilePushLink :title="`이벤트 상세 [ ${mStoreBoard.title} ]`" :storeGroup="storeGroup" :nextValue="`board/${groupId}/detail/${mStoreBoard.id}`" :isStore="true" /></span>
        </div>
      </div>
    </div>
    <!-- 기본설정 영역 - [CM:읽기/수정, MC:읽기] -->
    <div class="card-body">
      <div class="row col mb-4 align-items-center">
        <label class="col-lg-1 col-form-label">제목</label>
        <div class="col-lg-4">
          <div class="input-group">
            <input type="text" class="form-control" placeholder="제목을 입력해주세요." v-model.trim="mStoreBoard.title" maxlength="20" />
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-lg-1 col-form-label">노출순서</label>
        <div class="col-lg-4">
          <div class="tom-select-custom">
            <select class="form-select" v-model="mStoreBoard.sort" autocomplete="off" data-hs-tom-select-options='{"hideSearch": true}'>
              <option v-for="i in 99" :key="i" :value="i">{{ i }}</option>
            </select>
          </div>
        </div>
      </div>

      <div class="row col mb-4 align-items-center">
        <label class="col-lg-1 col-form-label">상위고정</label>
        <div class="col">
          <div class="row form-control border-0">
            <div class="col-auto form-check form-check-inline">
              <input id="radio_duplicate_y" type="radio" class="form-check-input" name="radio_duplicate" value="Y" v-model="mStoreBoard.pin" />
              <label class="form-check-label" for="radio_duplicate_y">사용</label>
            </div>
            <div class="col-auto form-check form-check-inline">
              <input id="radio_duplicate_n" type="radio" class="form-check-input" name="radio_duplicate" value="N" v-model="mStoreBoard.pin" />
              <label class="form-check-label" for="radio_duplicate_n">사용안함</label>
            </div>
          </div>
        </div>
      </div>

      <!-- 기간설정 Datepicker START -->
      <div class="row mb-4 align-items-center">
        <label for="idLabel" class="col-lg-1 col-form-label">기간설정</label>
        <div class="col">
          <div class="row">
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="startDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#startDatepickerInput","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="startDatepickerInput" placeholder="날짜를 선택해주세요." v-model="mStoreBoard.start_date" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="endDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#endDatepickerInput","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="endDatepickerInput" placeholder="날짜를 선택해주세요." v-model="mStoreBoard.end_date" />
                </div>
              </div>
            </div>
            <div class="d-lg-none mt-2"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('three')">3일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('week')">7일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriod('month')">30일</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 기간설정 Datepicker END -->

      <!-- 노출기간 Datepicker START -->
      <div class="row mb-4 align-items-center">
        <label for="idLabel" class="col-lg-1 col-form-label">노출 기간 설정</label>
        <div class="col">
          <div class="row">
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="startDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#viewStartDatepickerInput","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="viewStartDatepickerInput" placeholder="날짜를 선택해주세요." v-model="mStoreBoard.view_start_date" />
                </div>
              </div>
            </div>
            <span class="col-auto align-items-center">~</span>
            <div class="col-lg-3">
              <!-- Form Group -->
              <div class="form-group">
                <div id="endDatepicker" class="js-flatpickr flatpickr-custom input-group" data-hs-flatpickr-options='{"appendTo": "#viewEndDatepickerInput","dateFormat": "Y-m-d H:i","enableTime": true,"time_24hr":true,"wrap": true}'>
                  <div class="input-group-prepend input-group-text" data-bs-toggle>
                    <i class="bi-calendar-week"></i>
                  </div>
                  <input type="text" class="flatpickr-custom-form-control form-control" id="viewEndDatepickerInput" placeholder="날짜를 선택해주세요." v-model="mStoreBoard.view_end_date" />
                </div>
              </div>
            </div>
            <div class="d-lg-none mt-2"></div>
            <div class="col">
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodView('today')">오늘</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodView('three')">3일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodView('week')">7일</button>
              <button type="button" class="btn btn-outline-info me-1 mb-1" @click.prevent="setSearchPeriodView('month')">30일</button>
            </div>
          </div>
        </div>
      </div>
      <!-- 노출기간 Datepicker END -->

      <div class="row col mb-4 align-items-center">
        <label class="col-lg-1 col-form-label"
          >이미지<br />
          <span style="font-size: 0.65rem" class="text-danger">
            [추천 가로 사이즈]<br />
            -썸네일타입 <br />
            299.5px,고정비율 1:1
            <br /><br />
            -배너타입 <br />
            402.66px,고정비율 2:1
          </span>
        </label>
        <div class="col-lg-4">
          <div class="input-group" v-if="!mStoreBoard.image">
            <UploadImage
              class="form-control"
              @change="
                () => {
                  uploadImg.check = uploadImg.value.length > 0;
                }
              "
              @upload="onRegistComRegPhoto"
              :btn="{ btnName: '이미지 선택', btnClass: 'btn btn-outline-secondary' }"
              :placeholder="'이미지를 선택해 주세요.'"
              disabled />
          </div>
          <div v-else>
            <img class="img-fluid img-thumbnail d-block" :src="mStoreBoard.image" alt="이미지" />
            <div class="mt-3">
              <button type="button" class="btn btn-outline-info me-2 btn-sm" @click="mStoreBoard.image = ''">수정</button>
            </div>
          </div>
        </div>
      </div>
      <div class="row col mb-4 align-items-center">
        <label class="col-lg-1 col-form-label"
          >내용<br />
          <span style="font-size: 0.65rem" class="text-danger"> (이미지 추천 가로 사이즈 915px) </span>
        </label>
        <div class="col">
          <CKEditorCustom @receiveData="receiveData" ref="ckeditorCustom" :editor-data="editorData" :url="'/store/photo'" />
        </div>
      </div>
      <div v-if="boardId">
        <router-link
          :to="{
            path: `/store/detail/board/detail/comment`,
            state: { code: storeCode, boardId: boardId, boardTitle: mStoreBoard.title },
          }">
          <button type="button" class="btn btn-sm btn-info">댓글 관리</button>
        </router-link>
      </div>
    </div>
    <div class="card-footer py-2">
      <div class="row align-items-center justify-content-end">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveClick" v-if="boardId">수정</button>
          <button type="button" class="btn btn-sm btn-danger ms-1" @click.prevent="deleteBoard()" v-if="boardId">삭제</button>
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="saveClick" v-else>생성</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import { apiResponseCheck, showAlert, showConfirm, getUserClassStr } from '@/utils/common-utils';
import UploadImage from '@/components/comm/uploadImage.vue';
import PageNavigator from '@/components/title/PageNavigator.vue';
import CKEditorCustom from '@/pages/settings/product/common/list/detail/CKEditorCustom.vue';
import type { Board } from 'StoreBoardInfoModule';
import MobilePushLink from '@/components/comm/MobilePushLink.vue';

const router = useRouter();
const groupId = ref();
const groupName = ref();
const storeGroup = ref();
const boardId = ref();
const storeCode = ref();
const mStoreBoard = ref({} as Board);
const mOriginStoreBoard = ref({} as Board);
const ckeditorCustom = ref();
const editorData = ref('');
const sdfp = ref();
const edfp = ref();
const vsdfp = ref();
const vedfp = ref();

// 이미지
const uploadImg = reactive<{ value: string; fileData: File | undefined; check: boolean; err_msg: string }>({
  value: '',
  fileData: undefined,
  check: false,
  err_msg: '이미지를 업로드해주세요.',
});

onMounted(() => {
  const code = history.state.code;
  if (code) {
    storeCode.value = code;
    boardId.value = history.state.boardId;
    groupId.value = history.state.groupId;
    groupName.value = history.state.groupName;
    storeGroup.value = history.state.storeGroup;
    mStoreBoard.value.store_board_group_id = groupId.value;
    mStoreBoard.value.sort = 99;
    mStoreBoard.value.pin = 'N';

    //@ts-ignore
    sdfp.value = flatpickr(document.querySelector('#startDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => sDateChangeStartDate() });
    //@ts-ignore
    edfp.value = flatpickr(document.querySelector('#endDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => eDateChangeStartDate() });

    //@ts-ignore
    vsdfp.value = flatpickr(document.querySelector('#viewStartDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => sDateChangeViewStartDate() });
    //@ts-ignore
    vedfp.value = flatpickr(document.querySelector('#viewEndDatepickerInput'), { enableTime: true, time_24hr: true, onClose: () => eDateChangeViewStartDate() });

    checkIsMod();
  } else {
    showAlert('비정상적인 접근입니다.');
    useRouter().back();
  }
});

const checkIsMod = () => {
  if (boardId.value) {
    mStoreBoard.value = JSON.parse(history.state.mStoreBoard);
    mOriginStoreBoard.value = JSON.parse(history.state.mStoreBoard);
    editorData.value = mStoreBoard.value.contents;

    if (mStoreBoard.value.start_date) {
      mStoreBoard.value.start_date = mStoreBoard.value.start_date.replace('T', ' ').slice(0, -3);
      mOriginStoreBoard.value.start_date = mOriginStoreBoard.value.start_date.replace('T', ' ').slice(0, -3);
      sdfp.value.jumpToDate(mOriginStoreBoard.value.start_date);
      sdfp.value.setDate(mOriginStoreBoard.value.start_date);
    }

    if (mStoreBoard.value.end_date) {
      mStoreBoard.value.end_date = mStoreBoard.value.end_date.replace('T', ' ').slice(0, -3);
      mOriginStoreBoard.value.end_date = mOriginStoreBoard.value.end_date.replace('T', ' ').slice(0, -3);
      edfp.value.jumpToDate(mOriginStoreBoard.value.end_date);
      edfp.value.setDate(mOriginStoreBoard.value.end_date);
    }

    if (mStoreBoard.value.view_start_date) {
      mStoreBoard.value.view_start_date = mStoreBoard.value.view_start_date.replace('T', ' ').slice(0, -3);
      mOriginStoreBoard.value.view_start_date = mOriginStoreBoard.value.view_start_date.replace('T', ' ').slice(0, -3);
      vsdfp.value.jumpToDate(mOriginStoreBoard.value.view_start_date);
      vsdfp.value.setDate(mOriginStoreBoard.value.view_start_date);
    }

    if (mStoreBoard.value.view_end_date) {
      mStoreBoard.value.view_end_date = mStoreBoard.value.view_end_date.replace('T', ' ').slice(0, -3);
      mOriginStoreBoard.value.view_end_date = mOriginStoreBoard.value.view_end_date.replace('T', ' ').slice(0, -3);
      vedfp.value.jumpToDate(mOriginStoreBoard.value.view_end_date);
      vedfp.value.setDate(mOriginStoreBoard.value.view_end_date);
    }
  }
};

const saveClick = () => {
  ckeditorCustom.value.saveClicked();
};
const receiveData = (contentsData: string) => {
  mStoreBoard.value.contents = contentsData;

  if (!checkValidation()) return;

  if (boardId.value) {
    modStoreBoard(contentsData);
  } else {
    regStoreBoard();
  }
};

const regStoreBoard = () => {
  showConfirm('이벤트를 생성하시겠습니까?', () => {
    apis.store.reg_store_board(storeCode.value, mStoreBoard.value).then(res => {
      apiResponseCheck(res, () => {
        if (res.msg === 'success') {
          showAlert('이벤트가 등록되었습니다.', 'success', () => {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.replace('/');
            }
          });
          // router.replace({ path: `/store/detail/board`, state: { groupName: groupName.value, code: storeCode.value } });
        }
      });
    });
  });
};
const modStoreBoard = (contentsData: string) => {
  let modData = {} as any;
  if (mStoreBoard.value.title !== mOriginStoreBoard.value.title) {
    modData['title'] = mStoreBoard.value.title;
  }
  if (mStoreBoard.value.sort !== mOriginStoreBoard.value.sort) {
    modData['sort'] = mStoreBoard.value.sort;
  }
  if (mStoreBoard.value.pin !== mOriginStoreBoard.value.pin) {
    modData['pin'] = mStoreBoard.value.pin;
  }
  if (mStoreBoard.value.start_date !== mOriginStoreBoard.value.start_date) {
    modData['start_date'] = mStoreBoard.value.start_date;
  }
  if (mStoreBoard.value.end_date !== mOriginStoreBoard.value.end_date) {
    modData['end_date'] = mStoreBoard.value.end_date;
  }
  if (mStoreBoard.value.view_start_date !== mOriginStoreBoard.value.view_start_date) {
    modData['view_start_date'] = mStoreBoard.value.view_start_date;
  }
  if (mStoreBoard.value.view_end_date !== mOriginStoreBoard.value.view_end_date) {
    modData['view_end_date'] = mStoreBoard.value.view_end_date;
  }
  if (mStoreBoard.value.image !== mOriginStoreBoard.value.image) {
    modData['img'] = mStoreBoard.value.image;
  }
  if (mStoreBoard.value.contents !== mOriginStoreBoard.value.contents) {
    modData['contents'] = contentsData;
  }
  if (Object.keys(modData).length === 0) {
    showAlert('변경사항이 없습니다.', 'warning');
    return;
  }

  showConfirm('이벤트를 수정하시겠습니까?', () => {
    apis.store.mod_store_board(storeCode.value, boardId.value, mStoreBoard.value).then(res => {
      apiResponseCheck(res, () => {
        if (res.msg === 'success') {
          showAlert('이벤트가 수정되었습니다.', 'success', () => {
            if (window.history.length > 1) {
              router.back();
            } else {
              router.replace('/');
            }
          });
          // router.replace({ path: `/store/detail/board`, state: { groupName: groupName.value, code: storeCode.value } });
        }
      });
    });
  });
};

const deleteBoard = () => {
  showConfirm(`이벤트를 삭제하시겠습니까?`, () => {
    apis.store.delete_store_board(storeCode.value, boardId.value).then(res => {
      apiResponseCheck(res, () => {
        showAlert('이벤트가 삭제되었습니다.', 'success', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
          // router.replace({ path: `/store/detail/board`, state: { groupName: groupName.value, code: storeCode.value } });
        });
      });
    });
  });
};

const checkValidation = () => {
  if (!mStoreBoard.value.title) {
    showAlert('제목을 입력해주세요.', 'warning');
    return;
  }
  if (!mStoreBoard.value.start_date) {
    showAlert('이벤트기간을 입력해주세요.', 'warning');
    return;
  }
  if (!mStoreBoard.value.end_date) {
    showAlert('이벤트기간을 입력해주세요.', 'warning');
    return;
  }
  if (!mStoreBoard.value.view_start_date) {
    showAlert('노출시작일을 입력해주세요.', 'warning');
    return;
  }
  if (!mStoreBoard.value.view_end_date) {
    showAlert('노출종료일을 입력해주세요.', 'warning');
    return;
  }
  if (!mStoreBoard.value.contents.trim()) {
    showAlert('내용을 입력해주세요.', 'warning');
    return;
  }
  return true;
};

const onRegistComRegPhoto = (files: File) => {
  apis.common.upload_photo(files, 'store/board/').then(res => {
    apiResponseCheck(res, () => {
      mStoreBoard.value.image = res.uri;
      uploadImg.value = files.name;
      uploadImg.fileData = files;
    });
  });
};
const setSearchPeriod = (period: string, time: boolean = false) => {
  const today = new Date();
  switch (period) {
    case 'today':
      // @ts-ignore
      sdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      edfp.value.setDate(today.setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'three':
      // @ts-ignore
      sdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      edfp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 3).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'week':
      // @ts-ignore
      sdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      edfp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'month':
      // @ts-ignore
      sdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      edfp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 30).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
  }
};

const setSearchPeriodView = (period: string, time: boolean = false) => {
  const today = new Date();
  switch (period) {
    case 'today':
      // @ts-ignore
      vsdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      vedfp.value.setDate(today.setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'three':
      // @ts-ignore
      vsdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      vedfp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 3).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'week':
      // @ts-ignore
      vsdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      vedfp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 7).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
    case 'month':
      // @ts-ignore
      vsdfp.value.setDate(today.setHours(0, 0, 0, 0), true, 'Y-m-d H:i');
      // @ts-ignore
      vedfp.value.setDate(new Date(today.getTime() + 1000 * 60 * 60 * 24 * 30).setHours(23, 59, 0, 0), true, 'Y-m-d H:i');
      break;
  }
};

const sDateChangeStartDate = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      sdfp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};
const eDateChangeStartDate = () => {
  // @ts-ignore
  const sDate = window.$('#startDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#endDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      edfp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};

const sDateChangeViewStartDate = () => {
  // @ts-ignore
  const sDate = window.$('#viewStartDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#viewEndDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('시작 시간이 종료시간보다 이후 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      sdfp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};
const eDateChangeViewStartDate = () => {
  // @ts-ignore
  const sDate = window.$('#viewStartDatepickerInput').val() as string;
  // @ts-ignore
  const eDate = window.$('#viewEndDatepickerInput').val() as string;

  if (sDate === eDate || !sDate || !eDate) {
    return;
  } else {
    if (sDate > eDate) {
      showAlert('종료 시간이 시작시간보다 이전 시간일 수 없습니다.', 'warning');
      // @ts-ignore
      edfp.value.setDate(new Date(), true, 'Y-m-d H:i');
    }
  }
};
</script>
