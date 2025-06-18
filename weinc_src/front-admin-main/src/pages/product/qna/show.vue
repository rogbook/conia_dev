<template>
  <PageNavigator :before_link="['상품문의관리']" :current="'상품문의 상세'" />
  <div class="card col-md-8">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center">
        <div class="col-auto">
          <div class="form-control-borderless h2">상품 문의 내용</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card col">
        <div class="card-header">[상품정보]</div>
        <div style="padding: 0 21px">
          <div class="row col align-items-center">
            <label class="col-2 col-form-label"><img class="avatar-img" :src="photo.uri" /></label>
            <div class="col">
              <div class="input-group mb-2">상품명 : {{ product.name }}</div>
              <div class="input-group">
                상품코드 : &nbsp;<RouterLink :to="{ path: '/product/detail', state: { id: product.id } }">{{ product.code }}</RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card col mt-4" v-if="prodQnaInfo.id">
        <div class="card-header">[문의내용]</div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[제목]</label>
            <div class="col">
              <div class="input-group">{{ prodQnaInfo.title }}</div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center" v-if="getUserClassStr.includes('CM')">
            <label class="col-md-2 col-form-label">[작성자]</label>
            <div class="col">
              <RouterLink :to="{ path: '/customer/detail', state: { id: prodQnaInfo.customer.id } }">{{ prodQnaInfo.customer.name }}</RouterLink>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[질문 공개 여부]</label>
            <div class="col-auto">
              {{ prodQnaInfo.secret === 'Y' ? '비공개' : '공개' }}
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">[질문일시]</label>
            <div class="col">
              <div class="input-group">
                {{ dateTimeFormatConverter(prodQnaInfo.reg_date) }}
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">[문의내용]</label>
            <div class="col">
              <div v-html="contentsReplaceNewLine(prodQnaInfo.contents)"></div>
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
                <input type="text" class="form-control" placeholder="답변제목을 입력해주세요." v-model.trim="answer.title" maxlength="80" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">답변 내용</label>
            <div class="col">
              <textarea class="form-control" placeholder="답변 내용을 입력해주세요. (최대 1000자)" style="min-height: 200px; max-height: 300px" maxlength="1000" v-model="answer.contents" />
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="prodQnaInfo.status == 'C'">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="modProdQnaAnswerInfo">답변 수정</button>
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="prodQnaInfo.status == 'R'">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="addProdQnaAnswerInfo">답변 등록</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { apiResponseCheck, showAlert, showConfirm, showLogConsole, dateTimeFormatConverter, getUserClassStr } from '@/utils/common-utils';
import apis from '@/apis';
import { useUserStore } from '@/stores/user';
import { AxiosError } from 'axios';
import type { ProdQnaInfo, Answer, Product, Photo } from 'ProdQnaInfoModule';
import PageNavigator from '@/components/title/PageNavigator.vue';
const router = useRouter();

const qnaId = ref(parseInt(history.state.id.toString()));
const prodQnaInfo = ref({} as ProdQnaInfo);
const a_member_id = useUserStore().user.id as number;
const answer = ref({} as Answer);
const originAnswer = ref({} as Answer);
const product = ref({} as Product);
const photo = ref({} as Photo);

onMounted(async () => {
  getProdQnaInfo();
});

const contentsReplaceNewLine = (contents: string): string => {
  if (!contents) {
    return '';
  }
  return contents.replace(/\n/gi, '<br />');
};

const getProdQnaInfo = async () => {
  apis.product.getProdQna(qnaId.value).then(res => {
    apiResponseCheck(res, () => {
      prodQnaInfo.value = res;
      showLogConsole(res);
      if (res.answer) {
        answer.value = res.answer;
        originAnswer.value = { ...answer.value };
      }
      if (res.product) product.value = res.product;
      if (res.product && res.product.photos.length) photo.value = res.product.photos[0];
    });
  });
};

const addProdQnaAnswerInfo = () => {
  if (!checkValidation()) return;

  showConfirm('답변을 등록하시겠습니까?', () => {
    const params: object = {
      title: answer.value.title,
      contents: answer.value.contents,
      a_member_id: a_member_id,
    };

    apis.product.addProdQnaAnswer(qnaId.value, params).then(res => {
      apiResponseCheck(res, () => {
        showAlert('답변이 등록되었습니다.', 'success');
        if (window.history.length > 1) {
          router.back();
        } else {
          router.replace('/');
        }
      });
    });
  });
};

const modProdQnaAnswerInfo = () => {
  if (!answer.value?.id) return;
  if (!checkValidation()) return;
  if (!checkIsChange()) return;

  showConfirm('답변을 수정하시겠습니까?', () => {
    const params: object = {
      title: answer.value.title,
      contents: answer.value.contents,
      a_member_id: a_member_id,
    };

    apis.product.modProdQnaAnswer(answer.value?.id, params).then(res => {
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
    showAlert('답변 제목을 입력해주세요.', 'warning');
    return;
  }
  if (!answer.value.contents) {
    showAlert('답변 내용을 입력해주세요.', 'warning');
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
