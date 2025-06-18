<template>
  <PageNavigator :before_link="['1:1문의 관리']" :current="'1:1문의 관리 상세'" />
  <div class="card col-lg-8">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">1:1 문의 내용</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card col" v-if="qnaInfo.id">
        <div class="card-header">[문의내용]</div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">제목</label>
            <div class="col">
              <div class="input-group">{{ qnaInfo.title }}</div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">질문 공개 여부</label>
            <div class="col-auto">
              {{ qnaInfo.secret === 'Y' ? '비공개' : '공개' }}
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">질문일시</label>
            <div class="col">
              <div class="input-group">
                {{ dateTimeFormatConverter(qnaInfo.reg_date) }}
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">문의내용</label>
            <div class="col">
              <div class="col">
                <div class="form-control" v-html="contentsReplaceNewLine(qnaInfo.contents)"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="card col mt-4">
        <div class="card-header">[답변내용]</div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">답변 제목</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="답변제목을 입력해주세요." v-model.trim="answerInfo.title" maxlength="80" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">답변 내용</label>
            <div class="col">
              <textarea class="form-control" placeholder="답변 내용을 입력해주세요.(최대 1000자)" v-model.trim="answerInfo.contents" style="min-height: 200px; max-height: 300px" maxlength="1000" />
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="answerInfo.id">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="modQnaAnswerInfo">답변 수정</button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="!answerInfo.id">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="addQnaAnswerInfo">답변 등록</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import type { QnaInfo } from 'BoardInfoModule';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showConfirm, showLogConsole } from '@/utils/common-utils';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const qnaId = ref();
const qnaInfo = ref<QnaInfo>({} as QnaInfo);
const answerInfo = ref<QnaInfo>({} as QnaInfo);

const originAnswer = ref({} as QnaInfo);

const a_member_id = useUserStore().user.id as number;

const contentsReplaceNewLine = (contents: string): string => {
  return contents.replace(/\n/gi, '<br />');
};

const getQnaInfo = () => {
  apis.community.get_qna(qnaId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      qnaInfo.value = res;
      if (qnaInfo.value.status === 'C') {
        getAnswerInfo();
      }
    });
  });
};

const getAnswerInfo = () => {
  apis.community.get_qna_answer(qnaId.value).then(res => {
    apiResponseCheck(res, () => {
      showLogConsole(res);
      originAnswer.value = JSON.parse(JSON.stringify(res));
      answerInfo.value = res;
    });
  });
};

const addQnaAnswerInfo = () => {
  if (!answerInfo.value.title) {
    showAlert('답변 제목을 입력해주세요.', 'warning');
    return;
  }

  if (!answerInfo.value.contents) {
    showAlert('답변 내용을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('답변을 등록하시겠습니까?', () => {
    const data: any = { title: answerInfo.value.title, contents: answerInfo.value.contents, qna_id: qnaId.value, q_member_id: qnaInfo.value.q_member_id, a_member_id: a_member_id, status: 'C' };
    apis.community.add_qna_answer(qnaId.value, data).then(res => {
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

const modQnaAnswerInfo = () => {
  if (!answerInfo.value.title) {
    showAlert('답변 제목을 입력해주세요.', 'warning');
    return;
  }

  if (!answerInfo.value.contents) {
    showAlert('답변 내용을 입력해주세요.', 'warning');
    return;
  }

  let data: any = {};
  if (answerInfo.value.title !== originAnswer.value.title) {
    data['title'] = answerInfo.value.title;
  }

  if (answerInfo.value.contents !== originAnswer.value.contents) {
    data['contents'] = answerInfo.value.contents;
  }

  if (Object.keys(data).length === 0) {
    showAlert('변경된 내용이 없습니다.', 'warning');
    return;
  }

  showConfirm('답변 내용을 수정하시겠습니까?', () => {
    apis.community.mod_qna(answerInfo.value.id, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('답변 내용이 수정되었습니다.', 'success', () => {
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

onMounted(() => {
  const id = history.state.id;
  if (id) {
    qnaId.value = id;
    getQnaInfo();
  }
});
</script>

<style scoped></style>
