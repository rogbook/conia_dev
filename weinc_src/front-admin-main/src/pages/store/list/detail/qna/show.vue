<template>
  <PageNavigator v-if="isTotal" :before_link="['통합 고객 문의 관리']" :current="'고객 문의 상세'" />
  <PageNavigator v-else :before_link="!getUserClassStr.includes('CM') ? ['상점관리 상세', '고객 문의 관리'] : ['상점 관리', '상점관리 상세', '고객 문의 관리']" :current="'고객 문의 상세'" />
  <div class="card col-md-8">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">고객 문의 내용</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card col" v-if="storeQna.id">
        <div class="card-header">문의내용</div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[제목]</label>
            <div class="col">
              <div class="input-group">{{ storeQna.title }}</div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[문의유형]</label>
            <div class="col">
              <div class="input-group">{{ storeQna.type ? storeQna.type : '없음' }}</div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[이용 상점명]</label>
            <div class="col-auto">{{ storeQna.store.title }} ({{ storeQna.store.code }})</div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[질문 공개 여부]</label>
            <div class="col-auto">
              {{ storeQna.secret === 'Y' ? '비공개' : '공개' }}
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[질문일시]</label>
            <div class="col">
              <div class="input-group">
                {{ dateTimeFormatConverter(storeQna.reg_date) }}
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">[문의내용]</label>
            <div class="col">
              <div v-html="contentsReplaceNewLine(storeQna.contents)"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="card col mt-4">
        <div class="card-header">답변내용</div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[답변 제목]</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="답변제목을 입력해주세요." v-model.trim="answer.title" maxlength="128" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">[답변 내용]</label>
            <div class="col">
              <textarea class="form-control" placeholder="답변 내용을 입력해주세요. (최대 1000자)" style="min-height: 200px; max-height: 300px" maxlength="1000" v-model.trim="answer.contents" />
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="storeQna.status == 'C'">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="modStoreQnaAnswerInfo">답변 수정</button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="storeQna.status == 'R'">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="addStoreQnaAnswerInfo">답변 등록</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import type { storeQna as StoreQna, Answer } from 'StoreQnaInfoMOdule';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, getUserClassStr, showAlert, showConfirm } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const qnaId = ref(parseInt(history.state.show.toString()));
const isTotal = ref(false);
const a_member_id = useUserStore().user.id as number;
const storeQna = ref({} as StoreQna);
const answer = ref({} as Answer);
const originAnswer = ref({} as Answer);

onMounted(async () => {
  getStoreQnaInfo();
  if (history.state.isTotal) {
    isTotal.value = history.state.isTotal;
  }
});

const contentsReplaceNewLine = (contents: string): string => {
  if (!contents) {
    return '';
  }
  return contents.replace(/\n/gi, '<br />');
};

const getStoreQnaInfo = async () => {
  apis.store.get_store_qna(qnaId.value).then(res => {
    apiResponseCheck(res, () => {
      storeQna.value = res;
      if (res.answer) {
        answer.value = res.answer;
        originAnswer.value = { ...answer.value };
      }
    });
  });
};

const addStoreQnaAnswerInfo = () => {
  if (!checkValidation()) return;

  showConfirm('답변을 등록하시겠습니까?', () => {
    const params: any = {
      qna_id: qnaId.value,
      title: answer.value.title,
      contents: answer.value.contents,
      a_member_id: a_member_id,
    };

    apis.store.add_store_qna_answer(qnaId.value, params).then(res => {
      apiResponseCheck(res, () => {
        showAlert('답변이 등록되었습니다.', 'success', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
      });
    });
  });
};

const modStoreQnaAnswerInfo = () => {
  if (!answer.value?.id) return;
  if (!checkValidation()) return;
  if (!checkIsChange()) return;

  showConfirm('답변을 수정하시겠습니까?', () => {
    const params: any = {
      title: answer.value.title,
      contents: answer.value.contents,
    };

    apis.store.mod_store_qna_answer(answer.value?.id, params).then(res => {
      apiResponseCheck(res, () => {
        showAlert('답변이 수정되었습니다.', 'success', () => {
          if (window.history.length > 1) {
            router.back();
          } else {
            router.replace('/');
          }
        });
      });
    });
  });
};

const checkValidation = () => {
  if (!answer.value.title) {
    showAlert('답변제목을 입력해주세요.', 'warning');
    return;
  }
  if (!answer.value.contents) {
    showAlert('답변내용을 입력해주세요.', 'warning');
    return;
  }
  return true;
};

const checkIsChange = () => {
  if (answer.value.title !== originAnswer.value.title) {
    return true;
  }
  if (answer.value.contents !== originAnswer.value.contents) {
    return true;
  }
  showAlert('변경된 내용이 없습니다.', 'warning');
  return false;
};
</script>

<style scoped></style>
