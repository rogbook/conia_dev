<template>
  <PageNavigator :before_link="['1:1문의']" :current="'1:1문의 상세'" />
  <div class="card col-lg-8">
    <div class="card-header pb-1">
      <div class="row justify-content-between align-items-center" v-if="qnaId">
        <div class="col-auto">
          <div class="form-control-borderless h2">1:1 문의 내용</div>
        </div>
      </div>
      <div class="row justify-content-between align-items-center" v-else>
        <div class="col-auto">
          <div class="form-control-borderless h2">1:1 문의 등록</div>
        </div>
      </div>
    </div>
    <div class="card-body">
      <div class="card col">
        <div class="card-header">
          [문의내용]<br />
          <span class="text-danger" v-if="qnaInfo.status === 'C'">답변이 완료된 문의사항은 공개여부만 수정할 수 있습니다.</span>
        </div>
        <div class="card-body">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">제목</label>
            <div class="col">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="제목을 입력해주세요." v-model.trim="qnaInfo.title" :disabled="qnaInfo.status === 'C'" maxlength="80" />
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">질문 공개 여부</label>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_y" type="radio" class="form-check-input" name="radio_store_open" value="N" v-model="qnaInfo.secret" />
                <label class="form-check-label" for="radio_open_y">공개</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-check form-check-inline">
                <input id="radio_open_n" type="radio" class="form-check-input" name="radio_store_open" value="Y" v-model="qnaInfo.secret" />
                <label class="form-check-label" for="radio_open_n">비공개</label>
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">문의내용</label>
            <div class="col">
              <textarea class="form-control" placeholder="문의 내용을 입력해주세요. (최대 1000자)" v-model.trim="qnaInfo.contents" style="min-height: 200px; max-height: 300px" maxlength="1000" :disabled="qnaInfo.status === 'C'" />
            </div>
          </div>
        </div>
        <div class="card-footer py-2" v-if="qnaId">
          <div class="text-end">
            <button type="button" class="btn btn-sm btn-primary" @click.prevent="modQnaInfo">1:1문의 수정</button>
          </div>
        </div>
      </div>
      <div class="card col mt-4">
        <div class="card-header">[답변내용]</div>
        <div class="card-body" v-if="answerInfo">
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">답변 제목</label>
            <div class="col">
              <div class="input-group">
                {{ answerInfo.title }}
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">답변자</label>
            <div class="col">
              <div class="input-group">
                {{ answerInfo.a_member?.name }}
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-center">
            <label class="col-md-2 col-form-label">답변일시</label>
            <div class="col">
              <div class="input-group">
                {{ dateTimeFormatConverter(answerInfo.reg_date) }}
              </div>
            </div>
          </div>
          <div class="row col mb-2 align-items-baseline">
            <label class="col-md-2 col-form-label">답변 내용</label>
            <div class="col">
              <div class="form-control" v-html="contentsReplaceNewLine(answerInfo.contents)"></div>
            </div>
          </div>
        </div>
        <div class="card-body" v-else>답변 내용을 준비중입니다.</div>
      </div>
    </div>
    <div class="card-footer py-2" v-if="!qnaId">
      <div class="row align-items-center justify-content-center">
        <div class="col-auto">
          <button type="button" class="btn btn-sm btn-primary" @click.prevent="addQnaInfo">1:1문의 등록</button>
        </div>
      </div>
    </div>
  </div>

  <!-- 상점검색 Modal -->
  <Modal :id="'findStoreModal'" :title="'상점 검색'">
    <template #body>
      <div class="row">
        <div class="text-start mb-4">상점을 검색해주세요.</div>
        <div class="card">
          <div class="card-body">
            <!-- Modal Search Form -->
            <div class="mb-6">
              <div class="row col align-items-center">
                <label class="col-md-1 col-form-label text-nowrap">상점검색</label>
                <div class="col-md-2"></div>
                <div class="col">
                  <div class="input-group">
                    <input type="text" class="form-control" id="store_title" v-model="store_title" placeholder="검색할 상점의 이름을 입력해주세요." @submit.stop.prevent="reqStoreList()" @keypress.enter.prevent="reqStoreList()" />
                    <button type="button" class="btn btn-outline-info" @click.prevent="reqStoreList()">검색</button>
                  </div>
                </div>
              </div>
            </div>
            <!-- Member List Table -->
            <table class="table table-lg table-borderless table-thead-bordered table-nowrap table-align-middle card-table">
              <thead class="thead-light">
                <tr class="text-center">
                  <th>상점</th>
                  <th style="width: 10%">선택</th>
                </tr>
              </thead>
              <tbody>
                <tr class="text-center" v-for="(store, i) in storeList.datas" :key="JSON.stringify(store)">
                  <td>{{ store.title }}</td>
                  <td>
                    <button type="button" class="btn btn-sm btn-info" @click.prevent="setStore(store.title as string, store.code as string)">선택</button>
                  </td>
                </tr>
                <tr v-if="!storeList.datas || storeList.datas.length === 0">
                  <td colspan="2" class="text-center">검색 결과가 없습니다.</td>
                </tr>
              </tbody>
            </table>
            <!-- Member List Table End-->
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <button type="button" class="btn btn-white" data-bs-dismiss="modal">닫기</button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apis from '@/apis';
import type { QnaInfo } from 'BoardInfoModule';
import { AxiosError } from 'axios';
import { apiResponseCheck, dateTimeFormatConverter, showAlert, showConfirm, showLogConsole, showModal, hideModal } from '@/utils/common-utils';
import Modal from '@/components/comm/modal.vue';
import type { StoreList } from 'StoreListInfoModule';
import { useUserStore } from '@/stores/user';
import PageNavigator from '@/components/title/PageNavigator.vue';

const router = useRouter();

const qnaId = ref();
const qnaInfo = ref({} as QnaInfo);
const answerInfo = ref<QnaInfo>();

const originQna = ref({} as QnaInfo);

const q_member_id = useUserStore().user.id as number;

const selectedStoreInfo = reactive({
  name: '',
  code: '',
});

const store_title = ref('');
const storeList = ref({} as StoreList);

const setStore = (title: string, code: string) => {
  hideModal('findStoreModal');
  selectedStoreInfo.name = title;
  selectedStoreInfo.code = code;
  qnaInfo.value.store_code = code;

  store_title.value = '';
  storeList.value = {} as StoreList;
};

const reqStoreList = () => {
  if (!store_title.value) {
    //검색어 입력안함.
    showAlert('검색할 상점의 이름을 입력해주세요.', 'warning');
  } else {
    //검색어 입력함.
    apis.store.get_list(`title=${store_title.value}&`).then(res => {
      apiResponseCheck(res, () => {
        showLogConsole(res);
        storeList.value = res;
      });
    });
  }
};

const newCkeditorCustom = ref();
const removeItems = ref(['imageUpload', 'insertTable']);
const editorData = ref('');

const newReceiveData = (data: string) => {
  qnaInfo.value.contents = data;
};

const contentsReplaceNewLine = (contents: string): string => {
  return contents.replace(/\n/gi, '<br />');
};

const getQnaInfo = () => {
  apis.community.get_qna(qnaId.value).then(res => {
    apiResponseCheck(res, () => {
      originQna.value = JSON.parse(JSON.stringify(res));
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
      answerInfo.value = res;
    });
  });
};

const addQnaInfo = () => {
  if (!qnaInfo.value.title) {
    showAlert('제목(질문내용)을 입력해주세요.', 'warning');
    return;
  }

  if (!qnaInfo.value.contents) {
    showAlert('내용(질문답변)을 입력해주세요.', 'warning');
    return;
  }

  showConfirm('1:1 문의사항을 등록하시겠습니까?', () => {
    const data: any = { title: qnaInfo.value.title, contents: qnaInfo.value.contents, q_member_id: q_member_id, status: 'R', secret: qnaInfo.value.secret };
    apis.community.add_qna(data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('1:1문의사항이 등록되었습니다.', 'success', () => {
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

const modQnaInfo = () => {
  if (!qnaInfo.value.title) {
    showAlert('제목(질문내용)을 입력해주세요.', 'warning');
    return;
  }

  if (!qnaInfo.value.contents) {
    showAlert('내용(질문답변)을 입력해주세요.', 'warning');
    return;
  }

  let data: any = {};
  if (qnaInfo.value.title !== originQna.value.title) {
    data['title'] = qnaInfo.value.title;
  }

  if (qnaInfo.value.secret !== originQna.value.secret) {
    data['secret'] = qnaInfo.value.secret;
  }

  if (qnaInfo.value.contents !== originQna.value.contents) {
    data['contents'] = qnaInfo.value.contents;
  }

  if (Object.keys(data).length === 0) {
    showAlert('변경된 내용이 없습니다.', 'warning');
    return;
  }

  showConfirm('1:1 문의사항을 수정하시겠습니까?', () => {
    apis.community.mod_qna(qnaId.value, data).then(res => {
      apiResponseCheck(res, () => {
        showAlert('1:1 문의사항이 수정되었습니다.', 'success', () => {
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
  } else {
    qnaInfo.value.secret = 'N';
  }
});
</script>

<style scoped></style>
